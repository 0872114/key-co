from canvas import Canvas, Square, WSquare, TriSquare, CSquare
from maps import *
import cv2


class Encoder:

    def __init__(self):
        self.current_map = None
        self.canvas = Canvas()

    def _to_rgb(self, phrase):
        colors = list()
        legend = list()
        rgb = list()
        for char in phrase.lower():
            found = False
            for code, map in maps.items():
                if char in map:
                    found = True
                    if self.current_map != code:
                        legend.append(''.join(maps['S']).index(code) * sym_levels)
                        self.current_map = code
                        if rgb:
                            colors.append(rgb)
                            rgb = list()
                    level = maps[self.current_map].get(char)
                    rgb.append(level)
                    break

            if not found:
                if rgb:
                    self.current_map = None
                    colors.append(rgb)
                    rgb = list()
        if rgb:
            colors.append(rgb)
        return colors, legend

    def encode(self, phrase):
        colors, legend = self._to_rgb(phrase)
        canvas = self.canvas
        y = 0
        x = 0
        row_limit = 12
        for color in colors:
            if x >= row_limit:
                x = 0
                y += 1
            if len(color) <= 3:
                while len(color) < 3:
                    color.append(255)
                shape = Square(color)
                canvas.add_shape(shape, x, y)
            elif len(color) <= 6:
                while len(color) < 6:
                    color.append(255)
                shape = WSquare(color)
                canvas.add_shape(shape, x, y)
            elif len(color) <= 9:
                while len(color) < 9:
                    color.append(255)
                shape = TriSquare(color)
                canvas.add_shape(shape, x, y)
            else:
                while len(color) >= 6:
                    item = list()
                    for _ in range(6):
                        item.append(color.pop(0))
                    shape = CSquare(item)
                    canvas.add_shape(shape, x, y)
                    x += 1
                    if x >= row_limit:
                        x = 0
                        y += 1
                if color:
                    while len(color) < 6:
                        color.append(255)
                    shape = CSquare(color)
                    canvas.add_shape(shape, x, y)
            x += 1

        x = 0
        y = 0
        map_row_limit = 4
        while len(legend) > 9:
            item = list()
            for _ in range(9):
                item.append(legend.pop(0))
            shape = TriSquare(item)
            canvas.add_legend(shape, x, y)
            x += 1
            if x >= map_row_limit:
                x = 0
                y += 1
        if legend:
            while len(legend) < 9:
                legend.append(255)
            shape = TriSquare(legend)
            canvas.add_legend(shape, x, y)

    def save(self):
        if self.canvas is None:
            return

        canvas = self.canvas.draw()
        image_bytes = cv2.imencode('.png', canvas)[1].tobytes()
        return image_bytes
