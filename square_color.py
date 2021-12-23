import cv2
import numpy as np
import random

#Захват изображения
cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera")

#Массивы цветов, Красный, Синий, Жёлтый, Зелёный
lower = [(53, 70, 100),(160, 130, 200),(90, 120, 90),(25, 60, 60)]
upper = [(63, 160, 180),(190, 200, 255),(130, 190, 190),(50, 255, 255)]


#обработка изображения + фильтрация при помощи inRange
def find_mask(lower, upper):
    
    #Для фильтрации изображения используется функция вида inRange(img, l_s, r_s). 
    #Первый параметр — изменяемое изображение, а второй и третий — левая и правая граница 
    #пропускаемого цвета. Для задания каждой из границ потребуется 3 ползунка, так как у 
    #нас 3 канала в RGB. Всего нужно шесть ползунков.
    
    #На выходе дает набор пикселей со значением либо 0 1(цвет удовлетворяет заданным границам или не удовлетворяет)
    mask = cv2.inRange(hsv, lower, upper)
    
    #Erode() - эрозия изображения, выполняется для двоичных изображений.
    #Входные данные: первое - входное изображение, второе - элемент структурирования(ядро - определяет характер операции)
    mask = cv2.erode(mask, None, iterations = 2)
      
    #Dilate() - Расширение изображения Увеличивает область объекта.Принимает два входных параметра, 
    #Входные данные: первое - входное изображение, второе - элемент структурирования(ядро)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    return mask

#массив с названием цветов
sequence = ["R", "G", "B", "Y"]

#перетасовка массива с цветами
random.shuffle(sequence)

#расположение цветов на разных уровнях, 2 цвета сверху, 2 снизу
sequence = [[sequence[0], sequence[1]], [sequence[2], sequence[3]]]

#Функция для дебагинга
print(sequence)

#Функция Отвечает за отлов, отображение масок на экране и их цвет(+координаты)
def contur_cord(cnts, image, coloring):
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(image, (int(curr_x) ,int(curr_y)), 5,
                            coloring ,2)
            cv2.circle(image, (int(curr_x) ,int(curr_y)), int(radius),
                            coloring,2)
            return int(curr_x), int(curr_y)
    return 0, 0

while cam.isOpened():
    _, image = cam.read()
    #Размытие по гаусу, что бы поправить цвета.
    blurred = cv2.GaussianBlur(image, (11,11), 0)
    
    #Преобразование цветов из BGR в HSV для правильного отображения цвета
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    
    # Обращение к функции обработки изображения + фильтрация
    maskGr= find_mask(lower[0],upper[0])
    maskPn= find_mask(lower[1],upper[1])
    maskBl= find_mask(lower[2],upper[2])
    maskYel= find_mask(lower[3],upper[3])
    
    #набор массивов с цветами
    mask =   maskGr + maskPn +  maskBl + maskYel
    
    
    #findContours - Функция для поиска контуров. Использует для работы монохромное изображение,
    #так что все пиксели картинки с ненулевым цветом будут интерпретироваться как 1, а все нулевые останутся нулями
    
    #Входные параметры функции cv2.findContours ():
    #Двоичное изображение    
    #CV_CHAIN_APPROX_SIMPLE — склеивает все горизонтальные, вертикальные и диагональные контуры
    #CV_RETR_EXTERNAL — выдаёт только крайние внешние контуры(только внешний контур)
    cntsR = cv2.findContours(maskPn.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cntsG = cv2.findContours(maskGr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]    
    cntsB = cv2.findContours(maskBl.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cntsY = cv2.findContours(maskYel.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    #Массив с функцией contur_cord - возвращающей маску, + координаты шариков
    cords = [contur_cord(cntsB,image, (255,0,0)), contur_cord(cntsG,image, (0,255,0)),contur_cord(cntsR,image, (0, 0, 255)),contur_cord(cntsY,image, (0,255,255))]
    
    #Словарь содерщащий коордианты y шариков из массива cords для дальнейшей удобной сартировки по уровням
    y_cords = {"B": cords[0][1], "G": cords[1][1], "R": cords[2][1],"Y": cords[3][1]}    
    
    #Сортировка словаря по парядку
    sorted_y = list(dict(sorted(y_cords.items(), key=lambda item: item[1])))
   
    #Массив с списками из двух цвутов в каждом(первыми буквами от цветов)
    levels = [[sorted_y[0], sorted_y[1]], [sorted_y[2], sorted_y[3]]]
   
    #Словарь содерщащий коордианты x шариков из массива cords для дальнейшей удобной сартировки по уровням
    x_cords = {"B": cords[0][0], "G": cords[1][0], "R": cords[2][0],"Y": cords[3][0]}
    
    #Проверка что в levels цвета стоят правильно, сравния по x координате
    if x_cords[levels[0][1]] < x_cords[levels[0][0]]:
        levels[0][1], levels[0][0] = levels[0][0], levels[0][1]
        
    if x_cords[levels[1][1]] < x_cords[levels[1][0]]:
        levels[1][1], levels[1][0] = levels[1][0], levels[1][1]
    
    


    #камера с захваченым главным экраном
    cv2.imshow("Camera", image)
    
    #камера с масками 
    cv2.imshow("Mask", mask)
    
    key = cv2.waitKey(1)
     
    if key == ord('q'):
        break

    if levels == sequence:
        print("Correct")

cam.release()
cv2.destroyAllWindows()
