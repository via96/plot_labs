import cv2
import numpy
import os
from sklearn.decomposition import KernelPCA

cur_folder = os.path.dirname(__file__)
train_folder = os.path.join(cur_folder, 'trainset')

class Analazer:
    
    @staticmethod
    def analyzeWithKPCA(trainData, responses):
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

        print(trainData[0].shape)

        knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)

        temp = numpy.array(trainData, dtype=numpy.float32).reshape(len(trainData), -1)
        kpca = KernelPCA(n_components=30,kernel='rbf', gamma=1e-9)

        kpca.fit(temp)

        trainData = kpca.transform(temp)

        # knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)
        knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

        for i in range(len(checkData)):
            checkData[i] = kpca.transform(numpy.array(checkData[i]).reshape(1, -1))


        for kNeares in range(1, 8):
            # break
            success = 0
            total = 0
            for t in range(3):
                for i in range(len(checkData)):
                    try:
                        # temp = kpca.transform(numpy.array(checkData[i]).reshape(-1, 17*17))
                        res, results, neighbours, dist = knn.findNearest(checkData[i], kNeares)
                        if res == checkResponse[i]:
                            success += 1
                    except Exception as ex:
                        print(ex)
                    total += 1
            print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)
        
        return total, success


#     @staticmethod
#     def analyzeWithoutKPCA(train_data, responses, path_to_image):
#         check_data = []
#         checkResponse = []
#         import random
#         for i in range(int(len(train_data) * 0.2)):
#             number = random.randint(0, len(train_data) - 1)
#             checkResponse.append(responses[number])
#             del responses[number]
#             check_data.append(train_data[number])
#             del train_data[number]
#         print(len(train_data), len(check_data))

#         knn = cv2.ml.KNearest_create()
#         responses = numpy.array(responses)

#         num_train_data = numpy.array(train_data, dtype=numpy.float32)

#         knn.train(num_train_data, cv2.ml.ROW_SAMPLE, responses)

#         for i in range(len(check_data)):
#             check_data[i] = numpy.array(check_data[i]).reshape(1, -1)

#         res_parser = ImageParser(path_to_image)
#         test, _ = res_parser.gridParse(True)

#         result = []
#         for item in test:
#             train_shape = num_train_data.shape
#             num_shape = numpy.array(item, dtype=numpy.float32).shape
#             num_reshape = numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17).reshape(1,-1).shape
#             res, results, neighbours, dist = knn.findNearest(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17).reshape(1,-1), 3)
#             result.append(results[0][0])


# return result