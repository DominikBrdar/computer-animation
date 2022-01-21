import numpy as np
from pygame import Vector3

class Krivulja:
    def __init__(self, path):
        self.starting_points = []
        self.points = []
        self.vectors = []
        self.direction = 1  # 1 ili -1 (inkrement za indeks)
        self.current_point = 0  # index
        self.load_data(path)
        for i in range(len(self.starting_points) - 3):
            self.calculate_points(*self.starting_points[i:i + 4])

    def load_data(self, path):
        with open(path, 'r') as file:
            for line in file.readlines():
                line = line.rstrip().split(" ")
                self.starting_points.append(Vector3(float(line[0]), float(line[1]), float(line[2])))

    def get_next_point(self):
        self.current_point += self.direction 
        self.current_point = self.current_point % len(self.points)
        print(self.current_point)
        return self.points[self.current_point]

    def calculate_points(self, point_0, point_1, point_2, point_3):
        t = 0
        Bi3 = 1 / 6 * np.matrix([[-1, 3, -3, 1],
                                 [3, -6, 3, 0],
                                 [-3, 0, 3, 0],
                                 [1, 4, 1, 0]])
        Rx = np.matrix([[point_0.x],
                        [point_1.x],
                        [point_2.x],
                        [point_3.x]])
        Ry = np.matrix([[point_0.y],
                        [point_1.y],
                        [point_2.y],
                        [point_3.y]])
        Rz = np.matrix([[point_0.z],
                        [point_1.z],
                        [point_2.z],
                        [point_3.z]])
        while t < 1:
            T3 = np.matrix([t ** 3, t ** 2, t, 1])
            T2 = np.matrix([3 * t ** 2, 2 * t, 1, 0])
            self.points.append(Vector3(T3 * Bi3 * Rx, T3 * Bi3 * Ry, T3 * Bi3 * Rz))                     
            self.vectors.append(Vector3(T2 * Bi3 * Rx, T2 * Bi3 * Ry, T2 * Bi3 * Rz))
            t += 0.02
