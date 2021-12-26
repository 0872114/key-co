import cv2
import cv2 as cv
from maps import maps, sym_levels
import numpy as np


class Decoder:

    def __init__(self):
        self.phrases = list()
        self.symbols = list()

    @staticmethod
    def _find_squares(img):
        squares = []
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        for thrs in range(0, 1):
            _, bin = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY_INV)
            contours, _hierarchy = cv.findContours(bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.01 * cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    if cnt[3][1] > 2:
                        squares.append(cnt)
        return squares

    def _predict(self, img_buf):
        img_str = np.frombuffer(img_buf, dtype=np.uint8)
        img = cv2.imdecode(img_str, cv2.IMREAD_COLOR)
        canvas = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        squares = self._find_squares(img)
        square_data = dict()
        for square in squares:
            l = min(coord[0] for coord in square)
            r = max(coord[0] for coord in square)
            t = min(coord[1] for coord in square)
            b = max(coord[1] for coord in square)

            # [y][x]
            square_data[(t, l)] = (l, t, r, b)

        keys = sorted(square_data)
        phrases = []
        legend_storage = []
        values = []
        l0 = t0 = None
        legend = False
        for n, key in enumerate(keys):

            l, t, r, b = square_data[key]

            if t0 is not None and t - t0 > b - t:
                print('LEGEND OFF')
                legend = False

            if l0 is not None and l - l0 > (r - l) * 2:
                print(n + 1, 'INDENT:')
                phrases.append(values[:])
                values = []
            elif l0 is not None and l - l0 > (r - l) * 1.25:
                print(n + 1, 'LEGEND:')
                legend = True

            l0 = l
            t0 = t

            x = l + (r - l) // 3
            y = t + (b - t) // 6
            A = tuple(canvas[y, x])
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

            x = l + (r - l) // 3 * 2
            y = t + (b - t) // 6
            B = tuple(canvas[y, x])
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

            x = l + (r - l) // 3
            y = t + (b - t) // 2
            C = tuple(canvas[y, x])
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

            x = l + (r - l) // 3 * 2
            y = t + (b - t) // 2
            D = tuple(canvas[y, x])
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

            x = l + (r - l) // 3
            y = t + (b - t) // 6 * 5
            E = tuple(canvas[y, x])
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

            x = l + (r - l) // 3 * 2
            y = t + (b - t) // 6 * 5
            F = tuple(canvas[y, x])
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

            figure = 'undefined'
            if A == B == C == D == E == F:
                figure = 'square'
                if values:
                    phrases.append(values[:])
                    values = []

                if legend:
                    legend_storage += A[:]
                    legend_storage += C[:]
                    legend_storage += E[:]
                else:
                    phrases.append((A[:],))
            elif all((C == E == F, A == B == D)):
                figure = 'long'
                values.append(A[:])
                if 255 in A:
                    phrases.append(values[:])
                    values = []
                else:
                    values.append(C[:])
                    if 255 in C:
                        phrases.append(values[:])
                        values = []

            elif all((A == B == C, D == E == F)):
                figure = 'double'
                if values:
                    phrases.append(values[:])
                    values = []

                phrases.append((A[:], D[:]))
            elif all((A == B, C == D, E == F)):
                figure = 'triple'
                if values:
                    phrases.append(values[:])
                    values = []

                if legend:
                    legend_storage += A[:]
                    legend_storage += C[:]
                    legend_storage += E[:]
                else:
                    phrases.append((A[:], C[:], E[:]))

            print(n + 1, figure)

        if values:
            phrases.append(values[:])

        return phrases, legend_storage

    @staticmethod
    def translate_char(char, current_map):
        ord = (1 + char) // (256 // len(current_map))
        try:
            letter = current_map[ord]
        except IndexError:
            letter = ''
        return letter

    def translate(self, chars, sym):
        sympop = sym.pop(0)
        symbol = sympop // sym_levels
        code = ''.join(maps['S'])[symbol]
        current_map = ''.join(maps[code])
        phrase = ''
        for word in chars:
            for char in list(word):
                phrase += self.translate_char(int(char), current_map)
        phrase += ' '
        return phrase

    def decode(self, img_buf):
        phrases, legend_storage = self._predict(img_buf)
        text = ''
        for n, phrase in enumerate(phrases):
            text += self.translate(phrase, legend_storage)
        return text


if __name__ == '__main__':
    decoder = Decoder()
    response = decoder.decode("output.png")
    print(response)
