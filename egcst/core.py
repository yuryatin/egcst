from sys import stdout
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors
from shapely.geometry import Polygon as sly_Polygon
from shapely.geometry import Point as sly_Point

from ground.base import get_context
from sect.triangulation import Triangulation
context = get_context()
Contour, Point, sect_Polygon = context.contour_cls, context.point_cls, context.polygon_cls


class CrossSection():
    def __init__(self,
                 min_step=0.04,
                 input_file_name='input.txt'):
        self.min_step = min_step
        self.input_file_name = input_file_name
        with open(self.input_file_name) as f:
            self.data = f.readlines()

        self.polygons = list()
        for p_n, row in enumerate(self.data):
            self.polygons.append(list())
            for item in row.strip().split('\t'):
                items = item.split(',')
                self.polygons[p_n].append([float(items[0]), float(items[1])])

        for i_p, p in enumerate(self.polygons):
            self.polygons[i_p].append(p[0])

        self.n_polygons = len(self.polygons)
        self.nesting_matrix = np.zeros(
            (self.n_polygons, self.n_polygons), dtype=np.int64)

        for n_p in range(1, self.n_polygons):
            for n_p2 in range(n_p):
                if sly_Polygon(self.polygons[n_p]).contains(sly_Polygon(self.polygons[n_p2])):
                    self.nesting_matrix[n_p, n_p2] = 1
                    self.nesting_matrix[n_p2, n_p] = -1
                else:
                    if sly_Polygon(self.polygons[n_p2]).contains(sly_Polygon(self.polygons[n_p])):
                        self.nesting_matrix[n_p2, n_p] = 1
                        self.nesting_matrix[n_p, n_p2] = -1

        self.nesting_dict = dict(
            zip(np.arange(self.nesting_matrix.shape[0]), self.nesting_matrix.sum(axis=1)))

        self.polygons_initial = self.polygons.copy()
        for i_p, p in enumerate(self.polygons_initial):
            entended_p = list()
            for node_i, node in enumerate(p):
                if node_i:
                    entended_p.append(p[node_i-1])
                    x_0 = p[node_i-1][0]
                    x_1 = node[0]
                    y_0 = p[node_i-1][1]
                    y_1 = node[1]
                    delta_x = x_1 - x_0
                    delta_y = y_1 - y_0
                    if (np.abs(delta_x) <= min_step) and (np.abs(delta_y) <= min_step):
                        continue
                    if delta_x:
                        slope = delta_y / delta_x
                        if np.abs(delta_x) > np.abs(delta_y):
                            n_steps = int(np.abs(delta_x) / min_step) + 1
                            i_step = delta_x / n_steps
                            for i in range(n_steps):
                                x_2 = x_0 + (i + 1) * i_step
                                y_2 = y_0 + (x_2 - x_0) * slope
                                entended_p.append([x_2, y_2])
                        else:
                            n_steps = int(np.abs(delta_y) / min_step) + 1
                            i_step = delta_y / n_steps
                            for i in range(n_steps):
                                y_2 = y_0 + (i + 1) * i_step
                                x_2 = x_0 + (y_2 - y_0) / slope
                                entended_p.append([x_2, y_2])
                    else:
                        n_steps = int(np.abs(delta_y) / min_step) + 1
                        i_step = delta_y / n_steps
                        for i in range(n_steps):
                            y_2 = y_0 + (i + 1) * i_step
                            if y_2 == y_1:
                                continue
                            entended_p.append([x_0, y_2])
            entended_p.append(p[-1])
            self.polygons[i_p] = entended_p.copy()

        self.all_points = np.array(
            list({tuple(i) for p in self.polygons for i in p}))
        self.all_x = np.array([i[0] for i in self.all_points])
        self.all_y = np.array([i[1] for i in self.all_points])

        self.min_x = self.all_x.min()
        self.max_x = self.all_x.max()
        self.min_y = self.all_y.min()
        self.max_y = self.all_y.max()

        self.new_points = list()
        x_count = 0
        for i_x in np.arange(self.min_x + self.min_step, self.max_x, self.min_step):
            x_count += 1
            for i_y in np.arange(self.min_y + self.min_step, self.max_y, self.min_step):
                odd_shift = x_count % 2
                right_distance = True
                for all_p in self.all_points:
                    new_point = sly_Point(
                        [i_x, i_y+(self.min_step/9.0)*odd_shift])
                    if new_point.distance(sly_Point(all_p)) < (0.8 * self.min_step):
                        right_distance = False
                if right_distance:
                    self.new_points.append(
                        [i_x, i_y+(self.min_step/9.0)*odd_shift])

        self.new_x = np.array([i[0] for i in self.new_points])
        self.new_y = np.array([i[1] for i in self.new_points])

        self.new_point_attribution = dict()
        for i_p in range(self.n_polygons):
            self.new_point_attribution[i_p] = list()

        for point in self.new_points:
            p_attribution = list()
            for i_p, p in enumerate(self.polygons):
                if sly_Polygon(p).contains(sly_Point(point)):
                    p_attribution.append(i_p)
            try:
                self.new_point_attribution[min(p_attribution, key=self.nesting_dict.get)].append(
                    Point(point[0], point[1]))
            except:
                pass

    def draw_blank(self, fig_blank_file_name='output_blank.png'):
        self.color_indeces = list(range(len(mcolors.CSS4_COLORS)))
        fig, ax = plt.subplots()
        for i_c, p in enumerate(self.polygons):
            ax.add_patch(Polygon(np.array(p), alpha=0.2, facecolor=list(
                mcolors.CSS4_COLORS.values())[self.color_indeces[i_c+12]], label="%2d" % (i_c+1)))
        ax.scatter(self.all_x, self.all_y, s=6, c='k')
        ax.scatter(self.new_x, self.new_y, s=3, c='g')
        ax.axis('equal')
        ax.legend(loc='lower center', ncol=self.n_polygons)
        dpi = fig.get_dpi()
        plt.savefig(fig_blank_file_name, dpi=dpi*3)

    def triangulate(self):
        for i_p in range(self.n_polygons):
            if 1 in self.nesting_matrix[i_p, :] and -1 in self.nesting_matrix[i_p, :]:
                for j_p in np.where(self.nesting_matrix[i_p, :] == 1)[0]:
                    for k_p in np.where(self.nesting_matrix[i_p, :] == -1)[0]:
                        self.nesting_matrix[j_p,
                                            k_p] = self.nesting_matrix[k_p, j_p] = 0

        self.c_list = list()
        for p in self.polygons:
            p_list = list()
            for point in p:
                p_list.append(Point(point[0], point[1]))
            self.c_list.append(Contour(p_list[:-1]))

        self.p_list = list()
        for i_c, c in enumerate(self.c_list):
            nested = list()
            for k_p in np.where(self.nesting_matrix[i_c, :] == 1)[0]:
                nested.append(self.c_list[k_p])
            self.p_list.append(sect_Polygon(c, nested))

        self.tri_sect = dict()
        print("Process of triangulation:")
        stdout.flush()
        for i_p, p in enumerate(self.p_list):
            self.tri_sect[i_p] = Triangulation.constrained_delaunay(
                p, extra_points=self.new_point_attribution[i_p], context=context).triangles()
            print("The polygon #%2d has been triangulated" % (i_p + 1))
            stdout.flush()

    def save_triangles(self,
                       output_file_name_triangles='triangles.txt',
                       output_file_name_points='points.txt',
                       output_file_name='output.txt'):
        self.the_all_points = np.concatenate(
            (self.all_points, self.new_points))
        self.new_array = list()
        count = -1
        with open(output_file_name, 'w') as f:
            for i_z, z in self.tri_sect.items():
                for _tri in z:
                    count += 1
                    f.write("%d\t" % (count + 1))
                    self.new_array.append(list())
                    for i_v, v in enumerate(_tri.vertices):
                        self.new_array[count].append(
                            np.where(np.all(self.the_all_points == np.array([v.x, v.y]), axis=1))[0][0])
                        if i_v:
                            f.write("\t%.12f,%.12f" % (v.x, v.y))
                        else:
                            f.write("%.12f,%.12f" % (v.x, v.y))
                    f.write("\t%d\n" % (i_z + 1))

        with open(output_file_name_points, 'w') as f:
            for i_p, p in enumerate(self.the_all_points):
                f.write("%d\t%.11f\t%.11f\n" % (i_p + 1, p[0], p[1]))

        with open(output_file_name_triangles, 'w') as f:
            for i_tri, _tri in enumerate(self.new_array):
                f.write("%d\t%d\t%d\t%d\n" %
                        (i_tri + 1, _tri[0] + 1, _tri[1] + 1, _tri[2] + 1))

    def draw_triangles(self, fig_triangles_file_name='output_triangles.png'):
        fig, ax = plt.subplots()
        for i_c, p in enumerate(self.polygons):
            ax.add_patch(Polygon(np.array(p), alpha=0.2, facecolor=list(
                mcolors.CSS4_COLORS.values())[self.color_indeces[i_c+12]], label="%2d" % (i_c+1)))
        ax.scatter(self.all_x, self.all_y, s=20, c='r')
        plt.triplot(
            self.the_all_points[:, 0], self.the_all_points[:, 1], self.new_array, linewidth=0.7)
        for i_tri, tri_coor in enumerate(self.the_all_points[self.new_array]):
            the_center = sly_Polygon(tri_coor).centroid
            plt.text(the_center.x, the_center.y, "%d" % (i_tri + 1), fontdict={
                'fontsize': 4,
                'ha': 'center',
                'va': 'center',
                'c': 'gray'
            })
        ax.axis('equal')
        ax.legend(loc='lower center', ncol=self.n_polygons)
        dpi = fig.get_dpi()
        plt.savefig(fig_triangles_file_name, dpi=dpi*3)

    def do_everything(self):
        self.draw_blank()
        self.triangulate()
        self.save_triangles()
        self.draw_triangles()
