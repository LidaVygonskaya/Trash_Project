from PIL import Image, ImageDraw

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