from PIL import Image, ImageDraw
import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import os
import random
from Distance import Distance
from Image import ColoursConverter, ImagesWorker
from PointInitializer import PointsInitializer
from PointsBinder import PointsBinder, NormalDistribution

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

height = image.size[1]
width = image.size[0]

initializer = PointsInitializer(cluster_number, pixel_image, width, height)
binder = PointsBinder(cluster_number)

#cur_centers = initializer.initialize_centers_rand(cur_centers)
last_centers = initializer.initialize_centers_rand(last_centers)
points_list = []
for w in range(width):
    for h in range(height):
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

        initializer = PointsInitializer(i, "bla", width, height)

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
#     q = min(min(quality_xy)/(width**2 + height**2), min(quality_h)/(16*10**16))
#     #q = min(quality_xy)
#     print(min(quality_xy)/(width**2 + height**2))
#     print((min(quality_h)/(16*10**16))*sigma_0)
#     print(q)
#     quality.append(q)
#
# Q = max(quality)
# print("Best quality is " + str(Q) + " with " + str(quality.index(Q) + 2) + " clusters")
# print(sigma_0/H_CONST)



