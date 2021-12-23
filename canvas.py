import numpy as np
import cv2 as cv


class Canvas:

    def __init__(self):
        self.size = 36
        self.border = 8
        self.margin = 4
        self.shapes = dict()
        self.legend = dict()
        self.max_x = 0
        self.max_y = 0
        self.legend_size = 0

    def get_canvas(self):
        width = self.border * 2 + (self.max_x + 1) * (self.size + self.margin) + (self.legend_size + 1) * \
                (self.size + self.margin) + self.size // 2 - self.margin
        height = self.border * 2 + (self.max_y + 1) * (self.size + self.margin) - self.margin
        return np.zeros((height, width, 4), np.uint8)

    def draw(self):
        canvas = self.get_canvas()
        for xy, shape in self.shapes.items():
            shape.draw(canvas, *xy, size=self.size, border=self.border, margin=self.margin)
        for xy, shape in self.legend.items():
            x, y = xy
            shape.draw(canvas, self.max_x + x + 1, y, size=self.size, border=self.border, margin=self.margin,
                       left_indent=self.size // 2)
        canvas = cv.cvtColor(canvas, cv.COLOR_BGR2RGB)
        return canvas

    def add_shape(self, shape, x, y):
        self.shapes[x, y] = shape
        if x > self.max_x:
            self.max_x = x
        if y > self.max_y:
            self.max_y = y

    def add_legend(self, shape, x, y):
        self.legend[x, y] = shape
        if x > self.legend_size:
            self.legend_size = x
        if y > self.max_y:
            self.max_y = y


class Square:

    def __init__(self, color):
        assert len(color) == 3
        self.color = color + [255]

    def draw(self, img, x, y, size=36, border=8, margin=4):
        l = border + x * (size + margin)
        r = border + x * (size + margin) + size
        t = border + y * (size + margin)
        b = border + y * (size + margin) + size
        cv.rectangle(img, (l, t), (r, b), self.color, -1)


class TriSquare:

    def __init__(self, color):
        assert len(color) == 9
        self.color1 = color[:3] + [255]
        self.color2 = color[3:6] + [255]
        self.color3 = color[6:9] + [255]

    def draw(self, img, x, y, size=36, border=8, margin=4, left_indent=0):
        l = border + x * (size + margin) + left_indent
        r = border + x * (size + margin) + size + left_indent
        t = border + y * (size + margin)
        b = border + y * (size + margin) + size // 3
        cv.rectangle(img, (l, t), (r, b), self.color1, -1)

        l = border + x * (size + margin) + left_indent
        r = border + x * (size + margin) + size + left_indent
        t = border + y * (size + margin) + size // 3 + 1
        b = border + y * (size + margin) + size // 3 * 2
        cv.rectangle(img, (l, t), (r, b), self.color2, -1)

        l = border + x * (size + margin) + left_indent
        r = border + x * (size + margin) + size + left_indent
        t = border + y * (size + margin) + size // 3 * 2  + 1
        b = border + y * (size + margin) + size
        cv.rectangle(img, (l, t), (r, b), self.color3, -1)


class WSquare:

    def __init__(self, color):
        assert len(color) == 6
        self.color1 = color[:3] + [255]
        self.color2 = color[3:6] + [255]

    def draw(self, img, x, y, size=36, border=8, margin=4):
        l = border + x * (size + margin)
        r = border + x * (size + margin) + size
        t = border + y * (size + margin)
        b = border + y * (size + margin) + size

        pts = np.array([[l, t], [r, t], [l, b]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.polylines(img, [pts], True, self.color1, thickness=0)
        cv.fillPoly(img, [pts], color=self.color1)

        pts = np.array([[r, b], [r, t], [l, b]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.polylines(img, [pts], True, self.color2, thickness=0)
        cv.fillPoly(img, [pts], color=self.color2)


class CSquare:

    def __init__(self, color):
        assert len(color) == 6
        self.color1 = color[:3] + [255]
        self.color2 = color[3:6] + [255]

    def draw(self, img, x, y, size=36, border=8, margin=4):
        l = border + x * (size + margin)
        r = border + x * (size + margin) + size
        t = border + y * (size + margin)
        b = border + y * (size + margin) + size

        pts = np.array([[l, t], [r, t], [r, b]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.polylines(img, [pts], True, self.color1, thickness=0)
        cv.fillPoly(img, [pts], color=self.color1)

        pts = np.array([[l, t], [r, b], [l, b]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.polylines(img, [pts], True, self.color2, thickness=0)
        cv.fillPoly(img, [pts], color=self.color2)
