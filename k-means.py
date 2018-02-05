from PIL import Image, ImageDraw
import numpy as np
import random
import colorsys
import math
from collections import Counter
import matplotlib.pyplot as plt
import copy
import os
import random
from Distance import Distance
from polynom import derivative

H_CONST = 4 * (10 ** 8)
S_CONST = 10 ** 5
V_CONST = 10 ** 4

print ("Input file name (example \"image.jpg\")")
picture = input()
image = Image.open(picture)
pixel_image = image.load()

print ("Enter number of clusters")
cluster_number = input()

# List of centers coordinates. There are only X and Y coordinates of centers. (X, Y)
cur_centers = []
last_centers = []

hight = image.size[1]
width = image.size[0]


# R = pixel_image[320, 400][0]
# G = pixel_image[320, 400][1]
# B = pixel_image[320, 400][2]
# HSV = colorsys.rgb_to_hsv(R, G, B)
# print HSV
#
# RGB = colorsys.hsv_to_rgb(HSV[0], HSV[1], HSV[2])
# colorsys method you should divide v by 255 finally
# print RGB


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


class ColoursConverter:
    # Convert colours formats
    def RGB_to_HSV(self, RGB):
        RGB = [x / 255.0 for x in RGB]
        MAX = (max(RGB))
        MIN = (min(RGB))
        HSV = [0.0, 0.0, 0.0]

        # For H
        if MAX == MIN:
            HSV[0] = 0
        elif (MAX == RGB[0]) and (RGB[1] >= RGB[2]):
            HSV[0] = (60.0 / 360.0) * ((RGB[1] - RGB[2]) / (MAX - MIN))
        elif (MAX == RGB[0]) and (RGB[2] > RGB[1]):
            HSV[0] = (60.0 / 360.0) * ((RGB[1] - RGB[2]) / (MAX - MIN)) + 1
        elif MAX == RGB[1]:
            HSV[0] = (60.0 / 360.0) * ((RGB[2] - RGB[0]) / (MAX - MIN)) + 120.0 / 360.0
        elif MAX == RGB[2]:
            HSV[0] = (60.0 / 360.0) * ((RGB[0] - RGB[1]) / (MAX - MIN)) + 240.0 / 360.0

        # For S
        if MAX == 0:
            HSV[1] = 0
        else:
            HSV[1] = 1 - MIN / MAX

        # For V
        HSV[2] = MAX

        return HSV


class ImagesWorker:
    def __init__(self, num, picture_name):
        self.num = num
        self.picture_name = picture_name

    picture_name = ''
    num = 0

    # Takes points dictionary
    def draw_cluster(self, points_dict, path):
        for i in range(self.num):
            print(len(list(points_dict.values())))
            cluster_name = "cluster_lida" + str(i) + ".jpg"
            cluster = Image.open(path + self.picture_name)
            draw = ImageDraw.Draw(cluster)
            for index in range(len(list(points_dict.values()))):
                if index != i:
                    for p in list(points_dict.values()[index]):
                        draw.point((int(p[0]), int(p[1])), (0, 0, 0))
            cluster.save(cluster_name)
            print("cluster saved")


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


# k-means!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
initializer = PointsInitializer(cluster_number, pixel_image)
binder = PointsBinder(cluster_number)

#cur_centers = initializer.initialize_centers_rand(cur_centers)
last_centers = initializer.initialize_centers_rand(last_centers)
points_list = []
for w in range(width):
    for h in range(hight):
        point = initializer.initialize_point(w, h)
        points_list.append(point)

cur_centers = initializer.initialize_centers(cur_centers, points_list)
#cur_centers = initializer.initialize_centers_rand(cur_centers)

while True:
    last_centers = cur_centers
    points = binder.binding_points(cur_centers, points_list)
    cur_centers = initializer.initializing_new_centers(points)
    print(cur_centers)
    if (np.isclose(cur_centers[0][0], last_centers[0][0])):
        break

image_worker = ImagesWorker(cluster_number, picture)
image_worker.draw_cluster(points, '')

# comlete clusterization
# cluster is our objects
related_cluster_num = 0
if len(list(points.values()[0])) < len(list(points.values()[1])):
    cluster = list(points.values()[0])
else:
    cluster = list(points.values()[1])
    related_cluster_num = 1

#cluster = points_list

# Creating massive of points(X Y H)
object_points_H = []
object_points_XY = []

for point in cluster:
    object_points_XY.append(point[:-3])
    object_points_H.append(point[2])

normal_distribution = NormalDistribution()
sigma_0 = normal_distribution.count_sigma(object_points_H)

X = []
Y = []
H = []
for point in cluster:
    X.append(point[0])
    Y.append(point[1])
    H.append(point[2])

myu_x = normal_distribution.count_myu_2dim(X)
myu_y = normal_distribution.count_myu_2dim(Y)
print("X: " + str(myu_x))
print("Y: " + str(myu_y))
sigma_x = normal_distribution.count_variance(X)
print("sigma^2 X: " + str(sigma_x))

plt.hist(X, 200)
plt.hist(Y, 200)
plt.show()

plt.hist(H, 200)
plt.show()

quality = []
J_list_mean = []

im = input()

N = 10
# from 2 to 9
for s in range(3):
    J_list = []

    for i in range(1, N):
        print ("Number " + str(i))
        cluster_cur_centers = []
        cluster_last_centers = []
        for k in range(i):
            if i == 1:
                cluster_cur_centers.append(cur_centers[related_cluster_num])
            else:
                cluster_cur_centers.append((random.choice(cluster))[:-2])
        binder = PointsBinder(i)

        initializer = PointsInitializer(i, "bla")

        while True:
            cluster_last_centers = copy.deepcopy(cluster_cur_centers)
            # print(cluster_cur_centers)

            # Counting centers
            # H_points = binder.bind_points_sigma(cluster_cur_centers, object_points_H, sigma_0)
            # XY_points = binder.binding_points(cluster_cur_centers, object_points_XY)
            points_XYH = binder.bind_points_XYH(cluster_cur_centers, object_points_XY, object_points_H, sigma_0)
            # new_center_H = initializer.initialize_new_center_one_dimension(H_points)
            # new_center_XY = initializer.initialize_new_centers_XY(XY_points)
            new_center_XYH = initializer.initialize_new_centers_XYH(points_XYH)

            cluster_cur_centers = new_center_XYH

            # for l in range(i):
            #   cluster_cur_centers[l][0] = new_center_XY[l][0]
            #  cluster_cur_centers[l][1] = new_center_XY[l][1]
            # cluster_cur_centers[l][2] = new_center_H[l]


            print("last" + str(cluster_last_centers))
            print("cur" + str(cluster_cur_centers))
            if np.isclose(cluster_cur_centers[0][0], cluster_last_centers[0][0]):
                break

        directory = "Cluster %s" % str(i)
        if not (os.path.exists(directory)):
            os.mkdir(directory)



        #i_worker = ImagesWorker(i, "object.jpg")
        i_worker = ImagesWorker(i, im)

        os.chdir(directory)
        # i_worker.draw_cluster(XY_points, '../')
        i_worker.draw_cluster(points_XYH, '../')
        os.chdir("..")


        #elbow method
        J = 0
        distance_counter = Distance()
        for cluster_center in cluster_cur_centers:
            for point in points_XYH[cluster_cur_centers.index(cluster_center)]:
                dist = distance_counter.euclidean_distance(cluster_center, point)
                J += dist

        J_list.append(J)

    J_list_mean.append(J_list)


print (J_list)
print(J_list_mean)
print(len(J_list_mean))

mean = []

for i in range(len(J_list_mean[0])):
    summ = 0.0
    for j_list in J_list_mean:
        summ += j_list[i]
    summ /= len(J_list_mean[0])
    mean.append(summ)
print ("mean " + str(mean))

for i in range(1, len(mean)):
    f = (mean[i] - mean[i - 1]) / (mean[i] + mean[i - 1])
    print (f)

    if math.fabs(f) < 0.2:
        print("you need " + str(i - 1) + " clusters")
        break



k = [a for a in range(1, 10)]
plt.plot(k, mean)
plt.show()
#
# derivative_list = derivative(k, J_list)
# plt.plot(k[:-1], derivative_list)
# plt.show()
#
# for i in range(1, len(derivative_list)):
#     multiplication = derivative_list[i] * derivative_list[i - 1]
#     if multiplication < 0:
#         print (k[i-1])
#         break
# print ("der_list " + str(derivative_list))

#for mean list

# k = [a for a in range(1, 10)]
# plt.plot(k, mean)
# plt.show()
#
# derivative_list = derivative(k, mean)
# plt.plot(k[:-1], derivative_list)
# plt.show()
# print("der_" + str(derivative_list))
# for i in range(1, len(derivative_list)):
#     multiplication = (derivative_list[i] - derivative_list[i - 1]) / (derivative_list[i] + derivative_list[i - 1])
#     print multiplication
#     print(np.isclose(derivative_list[i], [0.0]))

        #break




    # Define quality of every cluster
#     distance = Distance()
#     quality_xy = []
#     quality_h = []
#     for cluster_center1 in cluster_cur_centers:
#         c = [item for item in cluster_cur_centers if item != cluster_center1]
#         for cluster_center2 in c:
#             quality_xy.append(distance.euclidean_distance(cluster_center1[:-1], cluster_center2[:-1]))
#
#             quality_h.append(distance.euclidean_distance([cluster_center1[-1]], [cluster_center2[-1]]))
#
#     q = min(min(quality_xy)/(width**2 + hight**2), min(quality_h)/(16*10**16))
#     #q = min(quality_xy)
#     print(min(quality_xy)/(width**2 + hight**2))
#     print((min(quality_h)/(16*10**16))*sigma_0)
#     print(q)
#     quality.append(q)
#
# Q = max(quality)
# print("Best quality is " + str(Q) + " with " + str(quality.index(Q) + 2) + " clusters")
# print(sigma_0/H_CONST)




#Elbow method
