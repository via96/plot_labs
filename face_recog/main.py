import cv2
import numpy
import os
from sklearn.decomposition import KernelPCA
from analyzer import Analazer


def face_trainData(needsave = False):
    face_cascade = cv2.CascadeClassifier('trainset/haarcascade_frontalface_default.xml')

    img = cv2.imread('trainset/yalefaces.png')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, scaleFactor=6.2)

    print(len(faces))
    imgNum = 0
    faces = sorted(faces, key=lambda k: k[0] + k[1] * 10000)
    trainData = []
    responses = []
    for (x, y, w, h) in faces:
        tmpImage = imgGray[y:y + h, x:x + w]
        if needsave:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite("tmp/" + str(imgNum) + '.png', tmpImage)
        imageNumber = numpy.array(cv2.resize(tmpImage, (512, 512), interpolation=cv2.INTER_AREA)).reshape(
            512 * 512, -1)
        responses.append(int(imgNum/11))
        imgNum += 1
        trainData += [numpy.array(imageNumber, dtype=numpy.float32)]

    return trainData, responses


trainData, responses = face_trainData()
# trainData = prepareImageMSER(os.path.join(curFolder, 'trainset/digits_inverse4.png'))

print("Len trainData:", len(trainData))

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

anal = Analazer()

total, success = anal.analyzeWithKPCA(trainData, responses)

print("Total: " + str(total))
print("Success: " + str(success))