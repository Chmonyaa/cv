import math
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('./heat-hostports-KBPS-Svt-Read (31).png')
# img = cv2.imread('./3.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = img[25:275, 200:675]

lower_bound_1 = np.array([206, 0, 21])
upper_bound_1 = np.array([255, 146, 157])
mask_1 = cv2.inRange(img, lower_bound_1, upper_bound_1)
result = cv2.bitwise_and(img, img, mask=mask_1)
plt.subplot(1, 2, 1)
plt.imshow(mask_1, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()

lower_bound_2 = np.array([178, 156, 4])
upper_bound_2 = np.array([255, 244, 161])
mask_2 = cv2.inRange(img, lower_bound_2, upper_bound_2)
result_2 = cv2.bitwise_and(img, img, mask=mask_2)
plt.subplot(1, 2, 1)
plt.imshow(mask_2, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result_2)
plt.show()

lower_bound_3 = np.array([215, 57, 0])
upper_bound_3 = np.array([254, 187, 121])
mask_3 = cv2.inRange(img, lower_bound_3, upper_bound_3)
result_3 = cv2.bitwise_and(img, img, mask=mask_3)
plt.subplot(1, 2, 1)
plt.imshow(mask_3, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result_3)
plt.show()

final_mask = mask_1 + mask_2 + mask_3

final_result = cv2.bitwise_and(img, img, mask=final_mask)
plt.subplot(1, 2, 1)
plt.imshow(final_mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(final_result)
plt.show()

imgray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,200,255,0)
ret2, thresh2 = cv2.threshold(imgray,140,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours2, hierarchy2 = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(result,contours, -1,(0, 0, 255),1)
cv2.drawContours(result,contours2, -1,(0, 255, 0),1)
rgb_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
cv2.imshow('image',rgb_image)

dst_img = cv2.Canny(result, 50, 200, None, 3)

linesP = cv2.HoughLinesP(dst_img, 1, np.pi / 180, 10, None, 20, 10)

for i in range(0, len(linesP)):
    lin = linesP[i][0]

    cv2.line(result, (lin[0], lin[1]), (lin[2], lin[3]), (0, 0, 255), 3, cv2.LINE_AA)
cv2.imshow("Image with lines", result)

# Инициализация флагов
has_vertical = False
has_horizontal = False
has_diagonal = False
has_diagonal_2 = False

if linesP is not None:
    for i in range(0, len(linesP)):
        lin = linesP[i][0]
        x1, y1, x2, y2 = lin
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        if -10 <= angle <= 10:
            has_horizontal = True
            color = (0, 255, 0)
            label = "Горизонтальная"
        elif 85 <= angle <= 95:
            has_vertical = True
            color = (255, 0, 0)
            label = "Вертикальная"
        elif 10 < angle < 85:
            has_diagonal = True
            color = (0, 0, 255)
            label = "Диагональная"
        elif -85 < angle < -10:
            has_diagonal_2 = True
            color = (255, 165, 0)
            label = "Диагональная (противоположная)"

        cv2.line(result, (x1, y1), (x2, y2), color, 3, cv2.LINE_AA)

# Подсветка итогов
result_text = ""
if has_vertical:
    result_text += "Найдены вертикальные линии\n"
if has_horizontal:
    result_text += "Найдены горизонтальные линии\n"
if has_diagonal:
    result_text += "Найдены диагональные нисходящие линии\n"
if has_diagonal_2:
    result_text += "Найдены диагональные восходящие линии\n"
if not (has_vertical or has_horizontal or has_diagonal):
    result_text = "Линии не найдены"
print(result_text)

# Отображение результатов
cv2.imshow("Image with lines", result)
cv2.waitKey(0)
cv2.destroyAllWindows()