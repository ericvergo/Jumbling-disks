from math import *

from PIL import ImageDraw, Image

c2c = 1.6
# turn_value = pi / 6
# turn_count = 1
sf = 400
# x_center = c2c / 2
# y_point = abs(sqrt(1 - x_center ** 2))
x_size = int(sf * c2c)
y_size = int(sf)
im = Image.new(mode="RGB", size=(x_size, y_size), color=(255, 255, 255))
draw = ImageDraw.Draw(im)


def distance(point1, point2):
    return sqrt(((point1.x - point2.x) ** 2) + ((point1.y - point2.y) ** 2))


class point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y


class circ:
    def __init__(self, x: float = 0.0, y: float = 0.0, side: bool = True, depth: int = 0):
        self.x = x
        self.y = y
        self.side = side
        self.depth = depth


class part:
    def __init__(self, circ_list=[]):
        self.circ_list = circ_list

    def get_max_depth(self):
        max_depth = 0
        for i in self.circ_list:
            temp = i.depth
            if temp > max_depth:
                max_depth = temp
        return max_depth


def need_to_cut(part_in, circ_in):
    circ_list = part_in.circ_list
    checklist = []
    for i in circ_list:
        if i.side:
            checklist.append(i)
    for i in checklist:
        temp = distance(i, circ_in)
        if temp >= 2:
            return False
    return True


def cut(part_in, circ_in):
    circ_list_1 = []
    circ_list_2 = []
    for i in part_in.circ_list:
        circ_list_1.append(i)
        if distance(i, circ_in) < 2:
            circ_list_2.append(i)
    circ_list_1.append(circ(circ_in.x, circ_in.y, False, 150))
    circ_list_2.append(circ(circ_in.x, circ_in.y, True, 200))
    part_list = []
    part_1 = part(circ_list_1)
    part_2 = part(circ_list_2)
    part_list.append(part_1)
    part_list.append(part_2)
    return part_list


def add(circ_in):
    global part_list
    temp_list = []
    for i in part_list:
        if need_to_cut(i, circ_in):
            temp_list.extend(cut(i, circ_in))
        else:
            temp_list.append(i)
    part_list.clear()
    for i in temp_list:
        part_list.append(i)


def render(part_in):
    global sf
    draw = ImageDraw.Draw(im)
    for i in range(x_size):
        for j in range(y_size):
            should_draw = True
            temp_point = point(i / sf, j / sf)
            for k in part_in.circ_list:
                if distance(temp_point, k) >= 1 and k.side:
                    should_draw = False
                if distance(temp_point, k) < 1 and not k.side:
                    should_draw = False
            if should_draw:
                draw.point((i, j), fill=(0, 0, part_in.get_max_depth()))


part_list = []
part_list.append(part([circ(0.0, 0.0, True, 0), circ(c2c, 0.0, True, 0)]))
part_list.append(part([circ(0.0, 0.0, False, 0), circ(c2c, 0.0, True, 50)]))
part_list.append(part([circ(0.0, 0.0, True, 0), circ(c2c, 0.0, False, 100)]))
add(circ(0.0, 1.9, True, 0))
for i in part_list:
    render(i)
im.show()
