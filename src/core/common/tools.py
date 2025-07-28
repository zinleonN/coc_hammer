import math
import random

def fluctuate_number(n):
    if n == 0:
        return 0
    magnitude = max(0.1, abs(n) / 10 * 2)
    low = n - magnitude
    high = n + magnitude
    result = round(random.uniform(low, high), 3)
    
    return max(0.1, result)

def distance(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
