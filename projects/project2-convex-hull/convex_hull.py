from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        # SORT THE POINTS BY INCREASING X-VALUE
        sorted_points = sorted(points, key=lambda point: point.x())
        t2 = time.time()

        t3 = time.time()
        # this is a dummy polygon of the first 3 unsorted points
        # polygon = [QLineF(points[i], points[(i + 1) % 3]) for i in range(3)]
        # DIVIDE AND CONQUER
        hull_list = convexHull(sorted_points)
        t4 = time.time()
        polygon = []
        for i in range(0, len(hull_list) - 1):
            line = QLineF(hull_list[i], hull_list[i+1])
            polygon.append(line)
        polygon.append(QLineF(hull_list[-1], hull_list[0]))

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))


def convexHull(points):
    length = len(points)
    if length < 4:
        # order them in clockwise order and return them
        return orderHull(points)
    # split into 2 subtasks of half the size and merge them
    return mergeHull(convexHull(points[:length//2]), convexHull(points[length//2:]))


# called when the sub-hulls are of size < 4
def orderHull(points):
    # set the point to compare to the lowest x value, which is the first element at this point
    left_point = points[0]
    # sort according to their slope (remove the leftmost in order to get rid of any weird infinite/0 slope it might get)
    ordered_points = sorted(points[1:], key=lambda point: slope(left_point, point), reverse=True)
    # insert the leftmost point to the beginning of the list
    ordered_points.insert(0, left_point)
    return ordered_points


def slope(point1, point2):
    return (point2.y() - point1.y())/(point2.x() - point1.x())


def mergeHull(left_hull, right_hull):
    # upper tangent points
    left_upper, right_upper = upperTangent(left_hull, right_hull)
    # lower tangent points
    left_lower, right_lower = lowerTangent(left_hull, right_hull)

    # merge based on the tangent lines
    merged_hull = left_hull[:left_upper + 1]
    if right_lower == 0:
        merged_hull.extend(right_hull[right_upper:])
        merged_hull.append(right_hull[0])
    else:
        merged_hull.extend(right_hull[right_upper:right_lower + 1])
    if not left_lower == 0:
        merged_hull.extend(left_hull[left_lower:])

    print(merged_hull)

    return merged_hull


def upperTangent(left_hull, right_hull):
    # it's not ordered by x value anymore, but by slope, with the leftmost at the beginning
    left_point = left_hull.index(max(left_hull, key=lambda point: point.x()))
    right_point = 0
    done = False
    while not done:
        done = True
        left_next = left_point - 1
        right_next = right_point + 1
        # left moving tangent
        if left_next < 0:
            left_next = len(left_hull) - 1
        if right_next >= len(right_hull):
            right_next = 0
        while slope(left_hull[left_point], right_hull[right_point]) > slope(left_hull[left_next], right_hull[right_point]):
            left_point = left_next
            left_next += - 1
            if left_next < 0:
                left_next = len(left_hull) - 1
            done = False

        # right moving tangent
        while slope(left_hull[left_point], right_hull[right_point]) < slope(left_hull[left_point], right_hull[right_next]):
            right_point = right_next
            right_next += 1
            if right_next >= len(right_hull):
                right_next = 0
            done = False

    return left_point, right_point


def lowerTangent(left_hull, right_hull):
    # it's not ordered by x value anymore, but by slope, with the leftmost at the beginning
    left_point = left_hull.index(max(left_hull, key=lambda point: point.x()))
    right_point = 0
    done = False
    while not done:
        done = True
        left_next = left_point + 1
        right_next = right_point - 1
        # left moving tangent
        if right_next < 0:
            right_next = len(right_hull) - 1
        if left_next >= len(left_hull):
            left_next = 0
        while slope(left_hull[left_point], right_hull[right_point]) < slope(left_hull[left_next], right_hull[right_point]):
            left_point = left_next
            left_next += 1
            if left_next >= len(left_hull):
                left_next = 0
            done = False

        # right moving tangent
        while slope(left_hull[left_point], right_hull[right_point]) > slope(left_hull[left_point], right_hull[right_next]):
            right_point = right_next
            right_next += -1
            if right_next < 0:
                right_next = len(right_hull) - 1
            done = False

    return left_point, right_point


def main():
    points = [QPointF(2, 6), QPointF(3, 3), QPointF(5, 10), QPointF(8, 5), QPointF(9, 11), QPointF(12, 7), QPointF(13, 1)]
    hull = convexHull(points)
    print(hull)


if __name__ == "__main__":
    main()

