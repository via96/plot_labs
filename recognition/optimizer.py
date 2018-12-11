

class Optimizer:
    
    @staticmethod
    def KPCA(val):
        temp = numpy.array(trainData, dtype=numpy.float32).reshape(len(trainData), -1)
        kpca = KernelPCA(n_components=30, kernel='rbf', gamma=1e-8)

        kpca.fit(temp)

        trainData = kpca.transform(temp)


        # knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)
        knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

        for i in range(len(checkData)):
            checkData[i] = kpca.transform(numpy.array(checkData[i]).reshape(1, -1))

        