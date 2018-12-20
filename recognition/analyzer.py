import cv2
import numpy
import os
from sklearn.decomposition import KernelPCA
from image_parser import ImageParser

cur_folder = os.path.dirname(__file__)
train_folder = os.path.join(cur_folder, 'trainset')

class Analazer:
    
    @staticmethod
    def analyzeWithKPCA(train_data, responses, path_to_image):
        check_data = []
        checkResponse = []
        import random
        for i in range(int(len(train_data) * 0.2)):
            number = random.randint(0, len(train_data) - 1)
            checkResponse.append(responses[number])
            del responses[number]
            check_data.append(train_data[number])
            del train_data[number]
        print(len(train_data), len(check_data))

        knn = cv2.ml.KNearest_create()
        responses = numpy.array(responses)

        knn.train(numpy.array(train_data, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)

        temp = numpy.array(train_data, dtype=numpy.float32).reshape(len(train_data), -1)
        kpca = KernelPCA(n_components=30, kernel='rbf', gamma=1e-8)

        kpca.fit(temp)

        train_data = kpca.transform(temp)

        knn.train(train_data, cv2.ml.ROW_SAMPLE, responses)

        for i in range(len(check_data)):
            check_data[i] = kpca.transform(numpy.array(check_data[i]).reshape(1, -1))

        res_parser = ImageParser(path_to_image)
        test, _ = res_parser.gridParse(True)

        result = []
        for item in test:
            res, results, neighbours ,dist = knn.findNearest(kpca.transform(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17)).reshape(1,-1), 3)
            result.append(results[0][0])
            # print( "result: ", results,"\n")
            # print( "neighbours: ", neighbours,"\n")


        return result


    @staticmethod
    def analyzeWithoutKPCA(train_data, responses, path_to_image):
        check_data = []
        checkResponse = []
        import random
        for i in range(int(len(train_data) * 0.2)):
            number = random.randint(0, len(train_data) - 1)
            checkResponse.append(responses[number])
            del responses[number]
            check_data.append(train_data[number])
            del train_data[number]
        print(len(train_data), len(check_data))

        knn = cv2.ml.KNearest_create()
        responses = numpy.array(responses)

        num_train_data = numpy.array(train_data, dtype=numpy.float32)

        knn.train(num_train_data, cv2.ml.ROW_SAMPLE, responses)

        for i in range(len(check_data)):
            check_data[i] = numpy.array(check_data[i]).reshape(1, -1)

        res_parser = ImageParser(path_to_image)
        test, _ = res_parser.gridParse(True)

        result = []
        for item in test:
            train_shape = num_train_data.shape
            num_shape = numpy.array(item, dtype=numpy.float32).shape
            num_reshape = numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17).reshape(1,-1).shape
            res, results, neighbours, dist = knn.findNearest(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17).reshape(1,-1), 3)
            result.append(results[0][0])


        return result