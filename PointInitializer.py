import random
from Image import ColoursConverter
from Distance import Distance

H_CONST = 4 * (10 ** 8)
S_CONST = 10 ** 5
V_CONST = 10 ** 4


class PointsInitializer:
    def __init__(self, cluster_amount, image):
        self.cluster_amount = cluster_amount
        self.image = image

    cluster_amount = 0
    image = None


    def initialize_centers_rand(self, centers_list):
        colour_converter = ColoursConverter()
        for i in range(self.cluster_amount):
            X = random.randint(0, width)
            Y = random.randint(0, hight)
            R = self.image[X, Y][0]
            G = self.image[X, Y][1]
            B = self.image[X, Y][2]
            RGB = [R, G, B]
            HSV = colour_converter.RGB_to_HSV(RGB)
            centers_list.append([X, Y, H_CONST * HSV[0], S_CONST * HSV[1], (V_CONST * HSV[2])])
        return centers_list

    def initialize_centers(self, centers_list, points_l):
        distance = Distance()
        colour_converter = ColoursConverter()
        X = random.randint(0, width)
        Y = random.randint(0, hight)
        R = self.image[X, Y][0]
        G = self.image[X, Y][1]
        B = self.image[X, Y][2]
        RGB = [R, G, B]
        HSV = colour_converter.RGB_to_HSV(RGB)
        centers_list.append([X, Y, H_CONST * HSV[0], S_CONST * HSV[1], (V_CONST * HSV[2])])
        for i in range(1, self.cluster_amount):
            print i
            dist_list = []
            sum = 0
            for point in points_l:
                point_d_list = []
                for center in centers_list:
                    d = distance.euclidean_distance(center, point)
                    point_d_list.append(d)
                dist_list.append(min(point_d_list))
                sum += min(point_d_list)
            print sum
            rnd = random.random() * sum
            print rnd

            sum = 0

            for element in dist_list:
                sum += element
                if sum > rnd:
                    centers_list.append(points_l[dist_list.index(element)])
                    break
            print i


        return centers_list







    def initialize_point(self, x, y):
        colour_converter = ColoursConverter()
        R = self.image[x, y][0]
        G = self.image[x, y][1]
        B = self.image[x, y][2]
        RGB = [R, G, B]
        HSV = colour_converter.RGB_to_HSV(RGB)
        return [x, y, H_CONST * HSV[0], S_CONST * HSV[1], V_CONST * HSV[2]]

    def initializing_new_centers(self, points_dict):
        centers = []
        for i in range(self.cluster_amount):
            X = 0.0
            Y = 0.0
            H = 0.0
            S = 0.0
            V = 0.0

            points_list = points_dict.get(i)
            for point in points_list:
                X += float(point[0]) / len(points_list)
                Y += float(point[1]) / len(points_list)
                H += float(point[2]) / len(points_list)
                S += float(point[3]) / len(points_list)
                V += float(point[4]) / len(points_list)
            centers.append([X, Y, H, S, V])
        return centers

    def initialize_new_centers_XY(self, points_dict):
        centers = []
        for i in range(self.cluster_amount):
            X = 0.0
            Y = 0.0

            points_list = points_dict.get(i)
            for point in points_list:
                X += float(point[0]) / len(points_list)
                Y += float(point[1]) / len(points_list)

            centers.append([X, Y])
        return centers

    def initialize_new_centers_XYH(self, points_dict):
        centers = []
        for i in range(self.cluster_amount):
            X = 0.0
            Y = 0.0
            H = 0.0

            points_list = points_dict.get(i)
            for point in points_list:
                X += float(point[0]) / len(points_list)
                Y += float(point[1]) / len(points_list)
                H += float(point[2]) / len(points_list)

            centers.append([X, Y, H])
        return centers

    def initialize_new_center_one_dimension(self, h_dict):
        centers = []
        for i in range(self.cluster_amount):
            H = 0.0
            h_list = h_dict.get(i)
            for h in h_list:
                H += float(h) / len(h_list)
            centers.append(H)
        return centers