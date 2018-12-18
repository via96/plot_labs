import cv2
import numpy
import os
from sklearn.decomposition import KernelPCA
from image_parser import ImageParser

cur_folder = os.path.dirname(__file__)
train_folder = os.path.join(cur_folder, 'trainset')

class Analazer:
    
    @staticmethod
    def analyzeWithKPCA(trainData, responses, pathToImage):
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

        temp = numpy.array(trainData, dtype=numpy.float32).reshape(len(trainData), -1)
        kpca = KernelPCA(n_components=30, kernel='rbf', gamma=1e-8)

        kpca.fit(temp)

        trainData = kpca.transform(temp)


        # knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)
        knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

        for i in range(len(checkData)):
            checkData[i] = kpca.transform(numpy.array(checkData[i]).reshape(1, -1))

        # test = prepareImage(os.path.join(curFolder, 'test_inverse2.png'))

        res_parser = ImageParser(pathToImage)
        test, _ = res_parser.prepareImageNew(True)
        # test = prepareImageNew(os.path.join(curFolder, 'test5.png'), False, False, saveToFiles=True)

        resultsList = []
        for item in test:
            res, results, neighbours ,dist = knn.findNearest(kpca.transform(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17)).reshape(1,-1), 3)
            resultsList.append(results[0][0])
            print( "result: ", results,"\n")
            print( "neighbours: ", neighbours,"\n")
            # print( "distance: ", dist)


        return resultsList


    @staticmethod
    def analyzeWithoutKPCA(trainData, responses, pathToImage):
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

        num_train_data = numpy.array(trainData, dtype=numpy.float32)

        knn.train(num_train_data, cv2.ml.ROW_SAMPLE, responses)

        # temp = numpy.array(trainData, dtype=numpy.float32).reshape(len(trainData), -1)
        # kpca = KernelPCA(n_components=30, kernel='rbf', gamma=1e-8)

        # kpca.fit(temp)

        # trainData = kpca.transform(temp)


        # knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)
        # knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

        for i in range(len(checkData)):
            checkData[i] = numpy.array(checkData[i]).reshape(1, -1)

        # test = prepareImage(os.path.join(curFolder, 'test_inverse2.png'))

        res_parser = ImageParser(pathToImage)
        test, _ = res_parser.prepareImageNew(True)
        # test = prepareImageNew(os.path.join(curFolder, 'test5.png'), False, False, saveToFiles=True)

        resultsList = []
        for item in test:
            train_shape = num_train_data.shape
            num_shape = numpy.array(item, dtype=numpy.float32).shape
            num_reshape = numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17).reshape(1,-1).shape
            res, results, neighbours ,dist = knn.findNearest(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17).reshape(1,-1), 3)
            resultsList.append(results[0][0])
            # print( "result: ", results,"\n")
            # print( "neighbours: ", neighbours,"\n")
            # print( "distance: ", dist)


        return resultsList