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
        lastPlus = False
        lastMinus = True
        pointsStart = []
        pointsEnd = []
        for item in range(2, len(points)):
            if (points[item] - points[item - 1]) > 0 and not lastPlus:
                pointsStart += [item-1]
            if (points[item] - points[item - 1]) < 0 and not lastMinus:
                pointsEnd += [item+1]
            lastPlus = (points[item] - points[item - 1]) > 0
            lastMinus = (points[item] - points[item - 1]) < 0
        return {'start' : pointsStart, 'end' : pointsEnd}


    def prepareImageNew(self, needInverse = False, drawPlot = False, saveToFiles = False):
        img = cv2.imread(self.path)
        if needInverse:
            img = cv2.bitwise_not(img)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(os.path.join(cur_folder, 'test_inverse.png'), img)

        # Save pictures to harddrive
        # number = 0
        # for item in trainData:
        #     cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png", item)
        #     number += 1

        xGist = [sum(imgGray[k]) / len(imgGray[k]) for k in range(imgGray.shape[0])]
        xGist_median = numpy.median(xGist) *0.45
        xGistNorm = [0 if x < 10 else 1 for x in xGist]
        if drawPlot:
            pyplot.title("Гистограмма по строкам")
            pyplot.plot(range(len(xGist)), xGist); pyplot.show()
            pyplot.title("Гистограмма по строкам new")
            pyplot.plot(range(len(xGistNorm)), xGistNorm); pyplot.show()

        xPoints = self.calcBorders(xGistNorm)

        trainData = []
        responses = []
        number = 0
        for x in range(min(len(xPoints['start']), len(xPoints['end']))):
            curImage = imgGray[xPoints['start'][x]:xPoints['end'][x] +1, :]
            yGist = [sum(curImage[:, k]) / len(curImage[:, k]) for k in range(curImage.shape[1])]
            yGist_median = numpy.median(yGist) * 0.2
            yGistNorm = [0 if x < 10 else 1 for x in yGist]
            yPoints = self.calcBorders(yGistNorm)

            if drawPlot:
                pyplot.title("Гистограмма по столбцам")
                pyplot.plot(range(len(yGist)), yGist);
                pyplot.show()
                pyplot.title("Гистограмма по стобцам new")
                pyplot.plot(range(len(yGistNorm)), yGistNorm);
                pyplot.show()

            for y in range(min(len(yPoints['start']), len(yPoints['end']))):
                imageNumber = imgGray[
                            # xPoints['start'][x]-1, 0:xPoints['end'][x] + 1,
                            max(xPoints['start'][x]-1, 0):xPoints['end'][x] + 1,
                            max(yPoints['start'][y]-1, 0):yPoints['end'][y] + 1
                            ]
                if imageNumber.shape[0] > 10 and imageNumber.shape[1] > 10:
                    if saveToFiles:
                        cv2.imwrite(os.path.join(cur_folder, 'tmp/item') + str(number) + ".png",
                                    cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
                        number += 1
                    imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                        17 * 17, -1)
                    trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
                    responses.append(int(len(responses) / 500))


        return trainData, responses

    
    def MSER(self, needSave = False, oldStyleMode = False):
        img = cv2.imread(self.path)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create(_min_area=10)
        regions, _ = mser.detectRegions(imgGray)

        rectangles = list(set([cv2.boundingRect(x) for x in regions]))
        if oldStyleMode:
            res = []
            for i in range(len(rectangles)):
                xs, ys, ws, hs = rectangles[i]
                hasBigger = False
                for k in range(len(rectangles)):
                    if i == k:
                        continue
                    xi, yi, wi, hi = rectangles[k]
                    a = max(xi, xs)
                    b = min(xs + ws, xi + wi)
                    c = max(yi, ys)
                    d = min(ys + hs, yi + hi)

                    if (a < b) and (c < d):
                        # hasBigger = True
                        if (wi * hi > ws * hs):
                            hasBigger = True

                if not hasBigger:
                    res.append(rectangles[i])

            rectangles = res

            trainData = []

            for contour in rectangles:
                x, y, w, h = contour
                if w < 13 or h < 13:
                    continue
                imageNumber = imgGray[y:y + h, x: x + w]
                imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                    17 * 17, -1)
                trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
            return trainData


        copyImg = img.copy()
        [cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), cv2.FILLED) for x, y, w, h in rectangles]

        thresh = cv2.inRange(img, (0, 0, 255), (0, 0, 255))

        reg2, _ = mser.detectRegions(thresh)
        rectangles = [cv2.boundingRect(p) for p in reg2]

        trainData = []
        number = 0
        rectangles = sorted(rectangles, key=lambda key: key[0] + key[1] * 10000)
        test = [x[0] + x[1] * 10000 for x in rectangles]
        for contour in rectangles:
            x, y, w, h = contour
            if w * h < 3 * 13:
                continue
            imageNumber = imgGray[y:y + h, x: x + w]
            if needSave:
                cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png",
                            cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
            imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                17 * 17, -1)

            number += 1
            trainData += [numpy.array(imageNumber, dtype=numpy.float32)]

        return trainData
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # img = cv2.imread(self.path)
        # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # mser = cv2.MSER_create()
        # regions, _ = mser.detectRegions(imgGray)

        # rectangles = list(set([cv2.boundingRect(x) for x in regions]))
        # res = []
        # for i in range(len(rectangles)):
        #     xs, ys, ws, hs = rectangles[i]
        #     hasBigger = False
        #     for k in range(len(rectangles)):
        #         if i == k:
        #             continue
        #         xi, yi, wi, hi = rectangles[k]
        #         a = max(xi, xs)
        #         b = min(xs + ws, xi + wi)
        #         c = max(yi, ys)
        #         d = min(ys + hs, yi + hi)

        #         if (a < b) and (c < d):
        #             # hasBigger = True
        #             if (wi * hi > ws * hs):
        #                 hasBigger = True

        #     if not hasBigger:
        #         res.append(rectangles[i])

        # rectangles = res

        # trainData = []
        # responses = []

        # for contour in rectangles:
        #     x, y, w, h = contour
        #     if w < 13 or h < 13:
        #         continue
        #     imageNumber = imgGray[y:y + h, x: x + w]
        #     imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
        #         17 * 17, -1)
        #     trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
        #     responses.append(int(len(responses) / 500))

        # return trainData, responses