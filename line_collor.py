import cv2
import numpy as np
import random

#Захват изображения
cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera")

#Массивы цветов, Красный, Синий, Жёлтый
lower = [(130, 70, 70),(25, 60, 60),(55, 110, 150)]
upper = [(170, 255, 255),(50, 255, 255),(150, 255, 255)]

#обработка изображения + фильтрация при помощи inRange
def find_mask(lower, upper):
    
    #inRange(img, l_s, r_s) - функция для фильтрации изображения.
    #Первый параметр — изменяемое изображение, а второй и третий — левая и правая граница 
    #пропускаемого цвета. Для задания каждой из границ потребуется 3 числа, так как у 
    #нас 3 канала в RGB. По итогу у нас 6 чисел для настройки света.
    
    #На выходе дает набор пикселей со значением либо 0 1(цвет удовлетворяет заданным границам или не удовлетворяет)
    mask = cv2.inRange(hsv, lower, upper)
    
    #Erode() - эрозия изображения, выполняется для двоичных изображений.
    #Входные данные: первое - входное изображение, второе - элемент структурирования(ядро - определяет характер операции)
    mask = cv2.erode(mask, None, iterations = 2)
    
    #Dilate() - Расширение изображения Увеличивает область объекта.Принимает два входных параметра, 
    #Входные данные: первое - входное изображение, второе - элемент структурирования(ядро)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    return mask

#Функция для сравнения координат
def color_read(xR, xY, xB):
    #Объяевление массива текущими розициями, для дальнейшего сравнения
    curr_order = []
    
    #Сравнение координат шариков, согласно координате x(что чего больше, то и дальше)
    if (xR > xB) and (xB > xY) and (xY!=0):
        curr_order = ["R", "B", "Y"]

    if (xR > xY) and (xY > xB) and (xB!=0):
        curr_order = ["R", "Y", "B"]

    if (xB > xR) and (xR > xY) and (xY!=0):
        curr_order = ["B", "R", "Y"]

    if (xB > xY) and (xY > xR) and (xR!=0):
        curr_order = ["B", "Y", "R"]

    if (xY > xB) and (xB > xR) and (xR!=0):
        curr_order = ["Y", "B", "R"]

    if (xY > xR) and (xR > xB) and (xB!=0):
        curr_order = ["Y", "R", "B"]

    return curr_order

#массив с названием цветов
order = ["R", "B", "Y"]

#перетасовка массива цветов, рандомно
random.shuffle(order)

#вывод ципочки цветов, для проверки на ошибки, при реальной игре можно отключить
print(order)


while cam.isOpened():
    _, image = cam.read()
    
    #Размытие по гаусу, что бы поправить цвета на изображении
    blurred = cv2.GaussianBlur(image, (11,11), 0)
    
    #Преобразование цветов из BGR в HSV для правильного отображения цвета
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    
    # Обращение к функции обработки изображения + фильтрация
    maskR = find_mask(lower[0], upper[0])
    maskY = find_mask(lower[1], upper[1])
    maskB = find_mask(lower[2], upper[2])
    
    #набор массивов со всеми цветами
    mask = maskR +  maskY + maskB 
    
    #findContours - Функция для поиска контуров. Использует для работы монохромное изображение,
    #так что все пиксели картинки с ненулевым цветом будут интерпретироваться как 1, а все нулевые останутся нулями
    
    #Входные параметры функции cv2.findContours ():
    #Двоичное изображение    
    #CV_CHAIN_APPROX_SIMPLE — склеивает все горизонтальные, вертикальные и диагональные контуры.
    #CV_RETR_EXTERNAL — выдаёт только крайние внешние контуры(только внешний контур)
    cntsR = cv2.findContours(maskR.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cntsY = cv2.findContours(maskY.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]    
    cntsB = cv2.findContours(maskB.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    #объявляются 3-и переменных и им присвяевается 0, для избежания ошибок
    xR, xB, xY = 0, 0, 0
    
    #Отвечает за отлов, отображение масок на экране и их цвет(+координаты)
    if len(cntsR) > 0:
        c = max(cntsR, key=cv2.contourArea)
        (xR, yR), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(image, (int(xR) ,int(yR)), int(radius), (0,0,255),2)

    if len(cntsY) > 0:
        c = max(cntsY, key=cv2.contourArea)
        (xY, yY), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(image, (int(xY) ,int(yY)), int(radius), (0,255,255),2)

    if len(cntsB) > 0:
        c = max(cntsB, key=cv2.contourArea)
        (xB, yB), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(image, (int(xB) ,int(yB)), int(radius), (255, 0, 0),2)
            
     #обращение к функции для сравнения координат шариков   
    curr_order = color_read(xR, xY, xB)

    #камера с захваченым главным экраном
    cv2.imshow("Camera", image)
    
    #камера с масками 
    cv2.imshow("Mask", mask)
    
    key = cv2.waitKey(1)
     
    if key == ord('q'):
        break


    #Сравнение загаданной позиции с экранной версией
    if curr_order == order:
        print("Correct")
        #break
        

cam.release()
cv2.destroyAllWindows()
