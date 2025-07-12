import math
import random

def fluctuate_number(n):
    if n == 0:
        return 0.0
    magnitude = max(0.1, abs(n) / 10 * 2)
    low = n - magnitude
    high = n + magnitude
    result = random.uniform(low, high)
    return max(0.1, result)

def distance(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def random_offset(n):
    offset = n / 10
    return round(random.uniform(n - offset, n + offset), 3)

def generate_bezier_curve(start, end, control_points, num_points=100):
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1-t)**2 * start[0] + 2*(1-t)*t * control_points[0][0] + t**2 * end[0]
        y = (1-t)**2 * start[1] + 2*(1-t)*t * control_points[0][1] + t**2 * end[1]
        points.append((x, y))
    return points