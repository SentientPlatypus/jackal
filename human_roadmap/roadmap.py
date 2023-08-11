import numpy as np
import pprint
from matplotlib import pyplot as plt
import math


def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def do_intersect(seg1, seg2):
    p1, q1 = seg1
    p2, q2 = seg2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2 and o3 != o4) or (o1 == 0 and on_segment(p1, p2, q1)) or (o2 == 0 and on_segment(p1, q2, q1)) or (o3 == 0 and on_segment(p2, p1, q2)) or (o4 == 0 and on_segment(p2, q1, q2)):
        return True

    return False


def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1]-p1[1])**2)

def project_point_onto_line_segment(h, p1, p2):
    v = p2 - p1
    w = h - p1
    projection = np.dot(w, v) / np.dot(v, v)
    proj_h = p1 + np.clip(projection, 0, 1) * v
    return proj_h


class RoadMap():
    def __init__(self, wallpath:str, waypointpath:str) -> None:
        walls = np.loadtxt(wallpath)
        self.walls = walls.reshape(-1, 2, 2)

        waypoints = np.loadtxt(waypointpath)
        self.waypoints = waypoints

        self.roadmap = []
        # Go through each waypoint
        for i in range(len(self.waypoints)):
            #go through all other waypoints
            for j in range(len(self.waypoints)):
                if i== j:
                    continue

                w = self.waypoints[i]
                w2 = self.waypoints[j]
                
                w_w2_segment = np.array([w, w2])

                if not any([do_intersect(wall, w_w2_segment) for wall in self.walls]):
                    self.roadmap.append(w_w2_segment)

        self.roadmap = np.array(self.roadmap)
        print("Initialized".center(20, "-"))
        
    def project(self, h):
        closest = 0
        for segments in self.roadmap:
            try:
                projected = project_point_onto_line_segment(h, segments[0], segments[1])
                if distance(h, projected) < distance(h,closest):
                    closest = projected
            except:
                closest = projected
        return closest
        
        
    

    def plot(self, human = None):
        for wall in self.walls:
            x_values = [point[0] for point in wall]
            y_values = [point[1] for point in wall]
            plt.plot(x_values, y_values, color="green")
        
        for line in self.roadmap:
            x_values = [point[0] for point in line]
            y_values = [point[1] for point in line]
            plt.plot(x_values, y_values, color="red", linestyle="dotted")



        plt.scatter(self.waypoints[:, 0], self.waypoints[:, 1], color="blue", marker="*", label="waypoint")

        if human is not None:
            plt.scatter([human[0]], [human[1]], color="orange", marker="o", label="human")
            projected = self.project(h=human)
            print(projected)
            plt.scatter([projected[0]], [projected[1]], color="black", marker="D", label="projected")
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Plot of Walls')
        plt.legend()
        plt.grid(True)
        plt.show()





if __name__ == "__main__":

    print(do_intersect([[-1, 0], [1, 0]], [[0, -1], [0, 1]]))
    rm = RoadMap(r"W:\Code\workorinternship\jackal\human_roadmap\rhd3_map_3_walls.txt", r"W:\Code\workorinternship\jackal\human_roadmap\rhd3_map_3_waypoints.txt")
    human = np.array([10, -9])
    # rm.project(human)
    rm.plot(human= human)