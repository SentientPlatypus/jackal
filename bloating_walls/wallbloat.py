import numpy as np
import matplotlib.pyplot as plt
import math

def shift(wall:np.array, d):
    """This will shift the wall by d units assuming the wall is always on the right
    
    >>> shift([[0, 0],[10, 0]], 1)
    >>> [[0, 1],[10, 1]]
    """
    
    dx, dy = wall[1, 0]-wall[0, 0], wall[1, 1]-wall[0,1]
    distance = math.sqrt(dy**2 + dx **2)
    translation_vec = np.array([-dy, dx]) / distance * d

    shifted_wall = []
    for coord in wall:
        newcoord = np.array(coord) + translation_vec
        shifted_wall.append(list(newcoord))

    return np.array(shifted_wall)


def shiftall(walls:np.array, d):
    walls_shifted = []
    for wall in walls:
        walls_shifted.append(shift(wall, d))
    
    return np.array(walls_shifted)


def cornermatch(walls:np.array):
    """This function will return a dictionary that maps indices to other indices based off of which other wall has the closest starting point to the first walls endpoint"""
    graph = {}
    for i in range(len(walls)):
        minindex = 0
        for j in range(len(walls)):
            if i == j:
                continue

            distance = math.sqrt((walls[i, 1, 1]-walls[j, 0, 1])**2 + (walls[i, 1, 0]-walls[j, 0, 0])**2)
            minindex = j if math.sqrt((walls[i, 1, 1]-walls[minindex, 0, 1])**2 + (walls[i, 1, 0]-walls[minindex, 0, 0])**2) > distance else minindex
        graph[i] = minindex
    return graph

def intersect(w1, w2):
    def find_line_equation(point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        # Calculate the slope (m)
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
        else:
            # The slope is undefined for vertical lines (x2 - x1 = 0)
            slope = 99999

        # Calculate the y-intercept (b)
        y_intercept = y1 - slope * x1

        return slope, y_intercept

    # Get the equations of the two lines
    m1, b1 = find_line_equation(w1[0], w1[1])
    m2, b2 = find_line_equation(w2[0], w2[1])

    # Check if the lines are parallel (no intersection)
    if m1 == m2:
        return None

    # Calculate the x-coordinate of the intersection point
    x_intersection = (b2 - b1) / (m1 - m2)

    # Calculate the y-coordinate using one of the line equations
    y_intersection = m1 * x_intersection + b1

    return round(x_intersection, 2), round(y_intersection, 2)


def cornermerge(walls_shifted:np.array, wall_graph:dict):
    bloated_walls = walls_shifted.copy()
    for k in wall_graph.keys():
        ipoint = intersect(walls_shifted[k], walls_shifted[wall_graph[k]])
        bloated_walls[k, 1]= ipoint
        bloated_walls[wall_graph[k], 0] = ipoint
    
    return bloated_walls

def cornerRepair(walls:np.array, walls_shifted:np.array):
    wall_graph = cornermatch(walls)
    walls_bloat = cornermerge(walls_shifted, wall_graph)
    return walls_bloat

def bloat(walls:np.array, d):
    walls_shifted = shiftall(walls, d)
    return cornerRepair(walls, walls_shifted)


def plot_walls(walls, bloated):
    for wall in walls:
        x_values = [point[0] for point in wall]
        y_values = [point[1] for point in wall]
        plt.plot(x_values, y_values, color="blue")

    for wall in bloated:
        x_values = [point[0] for point in wall]
        y_values = [point[1] for point in wall]
        plt.plot(x_values, y_values, color="green")

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Walls')
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.show()


def walls_from_file(filename):
    walls = np.loadtxt(filename)
    return walls.reshape(-1, 2, 2)

def walls_to_file(bloated, filename):
    with open(filename, 'w') as file:
        for wall in bloated:
            x1, y1 = wall[0]
            x2, y2 = wall[1]
            file.write(f"{x1} {y1} {x2} {y2}\n")


if __name__ == "__main__":
    rhodes = walls_from_file("bloating_walls\walls.txt")
    plot_walls(rhodes, bloat(rhodes, 0.5))
    walls_to_file(bloat(rhodes, 0.5), "bloating_walls\bloated.txt")