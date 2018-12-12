import cv2
import os
import numpy
from matplotlib import pyplot

cur_folder = os.path.dirname(__file__)
train_folder = os.path.join(cur_folder, 'trainset')

class ImageParser:
    
    def __init__(self, image_path):
        self.path = image_path


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


    def prepareImageNew(self, isInverse = False, drawPlot = False, saveToFiles = False):
        im = cv2.imread(self.path)


        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        qr = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)


        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(im, contours, -1, (0,255,0), 3)
                
        img = cv2.imread(os.path.join(cur_folder, 'test_inverse.png'))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        xGist = [sum(imgGray[k]) / len(imgGray[k]) for k in range(imgGray.shape[0])]
        xGist_median = numpy.median(xGist) * 0.78
        xGistNorm = [min(x, xGist_median) for x in xGist]
        # img1 = [img0[x] - minimal for x in range(len(img0))]
        # plt.title("Гистограмма по строкам")
        # plt.plot(range(len(xGist)), xGist); plt.show()
        #
        # plt.title("Гистограмма по строкам new")
        # plt.plot(range(len(xGistNorm)), xGistNorm); plt.show()

        xPoints = self.calcBorders(xGistNorm)

        yGist = [sum(imgGray[:, k]) / len(imgGray[:, k]) for k in range(imgGray.shape[1])]
        yGist_median = numpy.median(yGist) * 0.78
        yGistNorm = [min(x, yGist_median) for x in yGist]

        # plt.title("Гистограмма по столбцам")
        # plt.plot(range(len(yGist)), yGist); plt.show()
        # plt.title("Гистограмма по стобцам new")
        # plt.plot(range(len(yGistNorm)), yGistNorm); plt.show()

        yPoints = self.calcBorders(yGistNorm)

        trainData = []
        responses = []
        number = 0
        for x in range(min(len(xPoints['start']), len(xPoints['end']))):
            for y in range(min(len(yPoints['start']), len(yPoints['end']))):
                imageNumber = imgGray[xPoints['start'][x]:xPoints['end'][x] + 1,
                            yPoints['start'][y]:yPoints['end'][y] + 1]
                if imageNumber.shape[0] > 10 and imageNumber.shape[1] > 10:
                    # cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + "_" + str(int(len(responses) / 500)) + ".png",
                    #             cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
                    imageNumber = numpy.array(cv2.resize(imageNumber, (17,17), interpolation=cv2.INTER_AREA)).reshape(17*17, -1)
                    trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
                    responses.append(int(len(responses) / 500))
                    number +=1


        return trainData, responses

    
    def MSER(self):
        oldStyleMode = False
        needSave = False
        img = cv2.imread(self.path)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create(_min_area=10)
        regions, _ = mser.detectRegions(imgGray)

        responses = []

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
            iters = 0
            for contour in rectangles:
                x, y, w, h = contour
                if w < 13 or h < 13:
                    continue
                imageNumber = imgGray[y:y + h, x: x + w]
                imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                    17 * 17, -1)
                trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
                responses.append(int(len(responses) / 500))
                iters += 1
            return trainData, responses


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
                cv2.imwrite(os.path.join(cur_folder, 'tmp/item') + str(number) + ".png",
                            cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
            imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                17 * 17, -1)

            number += 1
            trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
            responses.append(int(len(responses) / 500))

        return trainData, responses
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        img = cv2.imread(self.path)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(imgGray)

        rectangles = list(set([cv2.boundingRect(x) for x in regions]))
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
        responses = []

        for contour in rectangles:
            x, y, w, h = contour
            if w < 13 or h < 13:
                continue
            imageNumber = imgGray[y:y + h, x: x + w]
            imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                17 * 17, -1)
            trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
            responses.append(int(len(responses) / 500))

        return trainData, responses