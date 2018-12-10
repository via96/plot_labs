from image_parser import ImageParser
import cv2
import numpy
import os
from sklearn.decomposition import KernelPCA

def newTrainData():
    from sklearn import datasets
    digits = datasets.load_digits()

    tmp = [[i for i in range(len(digits['target'])) if digits['target'][i] == y] for y in range(10)]

    allDigits = []
    targets = []

    # imageNumber = numpy.array(cv2.resize(imageNumber, (17,17), interpolation=cv2.INTER_AREA)).reshape(17*17, -1)
    #         trainData += [numpy.array(imageNumber, dtype=numpy.float32)]

    for digit in tmp:
        for item in digit:

            allDigits.append(numpy.array(cv2.resize(digits['images'][item], (17, 17), interpolation=cv2.INTER_AREA)).reshape(17*17, -1))
            targets.append(digits['target'][item])

    return allDigits, targets

if __name__ == '__main__':
    train_parser = ImageParser("train_img.png")

    trainData = train_parser.prepareImageNew(True)

    trainData, responses = newTrainData()

    checkData = []
    checkResponse = []
    import random
    for i in range(int(len(trainData)*0.2)):
        number = random.randint(0, len(trainData) - 1)
        checkResponse.append(responses[number])
        del responses[number]
        checkData.append(trainData[number])
        del trainData[number]
    print(len(trainData), len(checkData))

    knn = cv2.ml.KNearest_create()
    responses = numpy.array(responses)

    knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)

    print("Without PCA")
    for kNeares in range(1, 5):
        # break
        success = 0
        total = 0
        for t in range(3):
            for i in range(len(checkData)):
                res, results, neighbours, dist = knn.findNearest(numpy.array(checkData[i], dtype=numpy.float32).reshape(1, -1), kNeares)
                if res == checkResponse[i]:
                    success += 1
                total += 1
        print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)

    print("With PCA")

    temp = numpy.array(trainData, dtype=numpy.float32).reshape(len(trainData), -1)
    kpca = KernelPCA(n_components=30, kernel='rbf', gamma=1e-8)

    kpca.fit(temp)

    trainData = kpca.transform(temp)


    # knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)
    knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

    for i in range(len(checkData)):
        checkData[i] = kpca.transform(numpy.array(checkData[i]).reshape(1, -1))


    for kNeares in range(1, 8):
        break
        success = 0
        total = 0
        for t in range(3):
            for i in range(len(checkData)):
                try:
                    temp = kpca.transform(numpy.array(checkData[i]).reshape(-1, 17*17))
                    res, results, neighbours, dist = knn.findNearest(checkData[i], kNeares)
                    if res == checkResponse[i]:
                        success += 1
                except Exception as ex:
                    print(ex)
                total += 1
        print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)


    # test = prepareImage(os.path.join(curFolder, 'test_inverse2.png'))

    res_parser = ImageParser('test1.png')
    test = res_parser.prepareImageNew(True)
    # test = prepareImageNew(os.path.join(curFolder, 'test5.png'), False, False, saveToFiles=True)

    resultsList = []
    for item in test:
        res, results, neighbours ,dist = knn.findNearest(kpca.transform(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17)).reshape(1,-1), 3)
        resultsList.append(results[0][0])
        print( "result: ", results,"\n")
        print( "neighbours: ", neighbours,"\n")
        # print( "distance: ", dist)


    print(resultsList)
