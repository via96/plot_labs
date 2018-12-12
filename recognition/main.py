from image_parser import ImageParser
import cv2
import numpy
import os
from sklearn.decomposition import KernelPCA
from analyzer import Analazer
from timer import Timer


def getResponses(num_amount):
    res = []
    for num in range(10):
        for i in range(num_amount):
            res.append(num)
    return res


def trueRecogAmount(result, data):
    amount = 0
    if len(result) < data:
        for i in range(len(result)):
            if result[i] == data[i]:
                amount += 1
    else:
        for i in range(len(data)):
            if result[i] == data[i]:
                amount += 1
    return amount

    
def printResult(method_name, values, time, true_amount):
    print('\nМетод: ' + method_name + ' | Время выполнения: ' + time + ' | Верных результатов: ' + true_amount)
    print("Значения: " + str(values))


if __name__ == '__main__':

    print('start')
    targetImgPath = 'test1.png'
    real_data = [1, 2, 5, 3, 7, 4]

    train_parser = ImageParser("train_img.png")

    responses = getResponses(500)

    print('01')
    trainData_grid, responses_grid = train_parser.prepareImageNew()
    print('02')
    trainData_mser, responses_mser = train_parser.MSER()

    timer = Timer()

    print('1')
    timer.start()
    res_grid = Analazer.analyzeWithoutKPCA(trainData_grid, responses, targetImgPath)
    time_grid = timer.stop()

    print('2')
    timer.start()
    res_mser = Analazer.analyzeWithoutKPCA(trainData_mser, responses, targetImgPath)
    time_mser = timer.stop()

    print('3')
    timer.start()
    res_grid_kpca = Analazer.analyzeWithKPCA(trainData_grid, responses, targetImgPath)
    time_grid_kpca = timer.stop()

    print('4')
    timer.start()
    res_mser_kpca = Analazer.analyzeWithKPCA(trainData_mser, responses, targetImgPath)
    time_mser_kpca = timer.stop()

    printResult('Строк и столбцов без KPCA', res_grid, time_grid, trueRecogAmount(res_grid, real_data))
    printResult('MSER без KPCA', res_mser, time_mser, trueRecogAmount(res_mser, real_data))
    printResult('Строк и столбцов с KPCA', res_grid_kpca, time_grid_kpca, trueRecogAmount(res_grid_kpca, real_data))
    printResult('MSER и столбцов с KPCA', res_mser_kpca, time_mser_kpca, trueRecogAmount(res_mser_kpca, real_data))



















    # train_parser = ImageParser("train_img.png")

    # trainData, responses = train_parser.prepareImageNew(True)

    # checkData = []
    # checkResponse = []
    # import random
    # for i in range(int(len(trainData)*0.2)):
    #     number = random.randint(0, len(trainData) - 1)
    #     checkResponse.append(responses[number])
    #     del responses[number]
    #     checkData.append(trainData[number])
    #     del trainData[number]
    # print(len(trainData), len(checkData))

    # knn = cv2.ml.KNearest_create()
    # responses = numpy.array(responses)

    # knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)

    # print("Without PCA")
    # for kNeares in range(1, 5):
    #     break
    #     success = 0
    #     total = 0
    #     for t in range(3):
    #         for i in range(len(checkData)):
    #             res, results, neighbours, dist = knn.findNearest(numpy.array(checkData[i], dtype=numpy.float32).reshape(1, -1), kNeares)
    #             if res == checkResponse[i]:
    #                 success += 1
    #             total += 1
    #     print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)

    # print("With PCA")

    # temp = numpy.array(trainData, dtype=numpy.float32).reshape(len(trainData), -1)
    # kpca = KernelPCA(n_components=30, kernel='rbf', gamma=1e-8)

    # kpca.fit(temp)

    # trainData = kpca.transform(temp)


    # # knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)
    # knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

    # for i in range(len(checkData)):
    #     checkData[i] = kpca.transform(numpy.array(checkData[i]).reshape(1, -1))


    # for kNeares in range(1, 8):
    #     break
    #     success = 0
    #     total = 0
    #     for t in range(3):
    #         for i in range(len(checkData)):
    #             try:
    #                 temp = kpca.transform(numpy.array(checkData[i]).reshape(-1, 17*17))
    #                 res, results, neighbours, dist = knn.findNearest(checkData[i], kNeares)
    #                 if res == checkResponse[i]:
    #                     success += 1
    #             except Exception as ex:
    #                 print(ex)
    #             total += 1
    #     print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)


    # # test = prepareImage(os.path.join(curFolder, 'test_inverse2.png'))

    # res_parser = ImageParser('test1.png')
    # test = res_parser.prepareImageNew(True)
    # # test = prepareImageNew(os.path.join(curFolder, 'test5.png'), False, False, saveToFiles=True)

    # resultsList = []
    # for item in test:
    #     res, results, neighbours ,dist = knn.findNearest(kpca.transform(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17)).reshape(1,-1), 3)
    #     resultsList.append(results[0][0])
    #     print( "result: ", results,"\n")
    #     print( "neighbours: ", neighbours,"\n")
    #     # print( "distance: ", dist)


    # print(resultsList)
