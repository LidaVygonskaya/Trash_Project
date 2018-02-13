from Distance import Distance
from collections import Counter
import math

class PointsBinder:
    def __init__(self, cluster_amount):
        self.cluster_amount = cluster_amount

    cluster_amount = 0

    def binding_points(self, centers, points_list):
        distance_list = []
        distance_counter = Distance()
        points = {a: [] for a in range(self.cluster_amount)}

        for point in points_list:
            for center in centers:
                r = distance_counter.euclidean_distance(center, point)
                distance_list.append(r)
            min_center_index = distance_list.index(min(distance_list))
            points.setdefault(min_center_index, []).append(point)
            distance_list = []
        return points

    def bind_points_sigma(self, centers, p_list, sigma):
        distance_list = []
        distance_counter = Distance()
        points_dict = {a: [] for a in range(self.cluster_amount)}

        for point in p_list:
            for center in centers:
                r = distance_counter.sigma_distance(sigma, center[2], point)
                distance_list.append(r)
            min_center_index = distance_list.index(min(distance_list))
            points_dict.setdefault(min_center_index, []).append(point)
            distance_list = []
        return points_dict

    def bind_points_XYH(self, centers, points_XY, points_H, sigma):
        distance_list = []
        distance_counter = Distance()
        points = {a: [] for a in range(self.cluster_amount)}
        for pointXY, pointH in zip(points_XY, points_H):
            for center in centers:
                r_xy = distance_counter.euclidean_distance(center[:2], pointXY)
                #r_h = distance_counter.sigma_distance(sigma, center[2], pointH)
                #  * 4 * (10 ** 4)
                r_h  = distance_counter.euclidean_distance([center[2]], [pointH])
                r = r_xy + r_h
                distance_list.append(r)
            min_center_index = distance_list.index(min(distance_list))
            points.setdefault(min_center_index, []).append(pointXY + [pointH])
            distance_list = []
        return points



class NormalDistribution:
    # Takes list of for example H
    def count_sigma(self, coordinates):
        mean = (sum(coordinates) / len(coordinates))
        summ = 0
        for coordinate in coordinates:
            summ += (coordinate - mean) ** 2
        sigma = math.sqrt(summ / len(coordinates))
        return sigma

    def count_myu_2dim(self, coordinate_list):
        # Count myu as expecting value
        myu = []
        c = Counter(coordinate_list)
        # coordinate_list.index()
        for coordinate in set(coordinate_list):
            e = coordinate * (float(c[coordinate]) / len(coordinate_list))
            myu.append(e)
        return sum(myu)

    def count_variance(self, coordinate_list):
        # counting sigma^2 xx or sigma yy E[X - E(X)]
        # X - E(X):
        sigma = []
        new_coordinates = []
        c = Counter(coordinate_list)
        for coordinate in set(coordinate_list):
            e = (coordinate - coordinate * (float(c[coordinate]) / len(coordinate_list))) ** 2
            for i in range(c[coordinate]):
                new_coordinates.append(e)
        c = Counter(new_coordinates)
        for coordinate in set(new_coordinates):
            e = coordinate * (float(c[coordinate]) / len(coordinate_list))
            sigma.append(e)
        return sum(sigma)