# util.py

def manhattanDistance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy2[1] - xy1[1])

def nearestPoint(pos):
    (current_row, current_col) = pos
    row = int(current_row + 0.5)
    col = int(current_col + 0.5)
    return (row, col)
