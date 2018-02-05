
class Distance:
    # Count distance between points
    def euclidean_distance(self, center, point):
        distance = 0.0
        for i in range(len(point)):
            distance += (point[i] - center[i]) ** 2
        return distance

    def sigma_distance(self, sigma, center_cor, point_cor):
        # distance = math.fabs(center_cor - point_cor) / sigma
        distance = ((center_cor - point_cor) ** 2) / sigma ** 2
        return distance
