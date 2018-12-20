import cv2
import os
import numpy
from matplotlib import pyplot

cur_folder = os.path.dirname(__file__)
train_folder = os.path.join(cur_folder, 'trainset')

class ImageParser:
    
    def __init__(self, image_path):
        self.path = image_path


    @staticmethod
    def getResponses(num_amount = 500):
        res = []
        for num in range(10):
            for i in range(num_amount):
                res.append(num)
        return res


    def calcBorders(self, points : list):
        last_plus = False
        last_minus = True
        start_points = []
        ends_points = []
        for item in range(2, len(points)):
            if (points[item] - points[item - 1]) > 0 and not last_plus:
                start_points += [item-1]
            if (points[item] - points[item - 1]) < 0 and not last_minus:
                ends_points += [item+1]
            last_plus = (points[item] - points[item - 1]) > 0
            last_minus = (points[item] - points[item - 1]) < 0
        return {'start' : start_points, 'end' : ends_points}


    def gridParse(self, is_inverse = False, draw_mode = False):
        img = cv2.imread(self.path)
        if is_inverse:
            img = cv2.bitwise_not(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(os.path.join(cur_folder, 'test_inverse.png'), img)

        x_gist = [sum(img_gray[k]) / len(img_gray[k]) for k in range(img_gray.shape[0])]
        # xGist_median = numpy.median(x_gist) *0.45
        x_gist_norm = [0 if x < 10 else 1 for x in x_gist]
        if draw_mode:
            pyplot.title("Гистограмма по строкам")
            pyplot.plot(range(len(x_gist)), x_gist); pyplot.show()
            pyplot.title("Гистограмма по строкам new")
            pyplot.plot(range(len(x_gist_norm)), x_gist_norm); pyplot.show()

        x_series = self.calcBorders(x_gist_norm)

        train_data = []
        responses = []
        # number = 0
        for x in range(min(len(x_series['start']), len(x_series['end']))):
            cur_image = img_gray[x_series['start'][x]:x_series['end'][x] +1, :]
            y_gist = [sum(cur_image[:, k]) / len(cur_image[:, k]) for k in range(cur_image.shape[1])]
            # yGist_median = numpy.median(y_gist) * 0.2
            y_gist_norm = [0 if x < 10 else 1 for x in y_gist]
            yPoints = self.calcBorders(y_gist_norm)

            if draw_mode:
                pyplot.title("Гистограмма по столбцам")
                pyplot.plot(range(len(y_gist)), y_gist);
                pyplot.show()
                pyplot.title("Гистограмма по стобцам new")
                pyplot.plot(range(len(y_gist_norm)), y_gist_norm);
                pyplot.show()

            for y in range(min(len(yPoints['start']), len(yPoints['end']))):
                img_num = img_gray[
                            # xPoints['start'][x]-1, 0:xPoints['end'][x] + 1,
                            max(x_series['start'][x]-1, 0):x_series['end'][x] + 1,
                            max(yPoints['start'][y]-1, 0):yPoints['end'][y] + 1
                            ]
                if img_num.shape[0] > 10 and img_num.shape[1] > 10:
                    img_num = numpy.array(cv2.resize(img_num, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                        17 * 17, -1)
                    train_data += [numpy.array(img_num, dtype=numpy.float32)]
                    responses.append(int(len(responses) / 500))


        return train_data, responses

    
    def MSER(self):
        img = cv2.imread(self.path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create(_min_area=10)
        regions, _ = mser.detectRegions(img_gray)

        rectangles = list(set([cv2.boundingRect(x) for x in regions]))
        [cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), cv2.FILLED) for x, y, w, h in rectangles]

        thresh = cv2.inRange(img, (0, 0, 255), (0, 0, 255))

        reg2, _ = mser.detectRegions(thresh)
        rectangles = [cv2.boundingRect(p) for p in reg2]

        train_data = []
        number = 0
        rectangles = sorted(rectangles, key=lambda key: key[0] + key[1] * 10000)
        # test = [x[0] + x[1] * 10000 for x in rectangles]
        for contour in rectangles:
            x, y, w, h = contour
            if w * h < 3 * 13:
                continue
            image_num = img_gray[y:y + h, x: x + w]
            image_num = numpy.array(cv2.resize(image_num, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                17 * 17, -1)

            number += 1
            train_data += [numpy.array(image_num, dtype=numpy.float32)]

        return train_data