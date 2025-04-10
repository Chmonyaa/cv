import cv2
import numpy as np
from tkinter import Tk, filedialog, Button, messagebox, Canvas, ttk, Toplevel
from PIL import Image, ImageTk
import math
import os

img_list = []
img_result = None
mask = None
contour_info = []
min_area = 400
contours = []
selected_contour = None
selected_image = None
pr = None
current_image = None


def load_images_from_folder():
    global img_list, selected_image, img_result
    pr.withdraw()
    folder_path = filedialog.askdirectory(title="Выберите папку с изображениями")
    pr.deiconify()

    if not folder_path:
        return

    folder_name = os.path.basename(folder_path)
    image_paths = [os.path.join(folder_path, f"{folder_name}_{i}.png") for i in range(11)]

    print(f"Пути к изображениям: {image_paths}")

    missing = [path for path in image_paths if not os.path.exists(path)]
    if missing:
        messagebox.showerror("Ошибка", f"Не найдены файлы: \n" + "\n".join(missing))
        return

    with open("contour_info.txt", "w", encoding="utf-8") as f:
        f.write("")

    img_list = []
    for path in image_paths[:10]:
        img = cv2.imread(path)
        if img is None:
            print(f"Не удалось загрузить изображение: {path}")
            continue
        if img.shape[0] > 2:
            img = img[2:, :, :]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (800, 400), interpolation=cv2.INTER_CUBIC)
        img_list.append(img)

    result_img = cv2.imread(image_paths[10])
    if result_img is None:
        messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {image_paths[10]}")
        return
    if result_img.shape[0] > 2:
        result_img = result_img[2:, :, :]
    result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    result_img = cv2.resize(result_img, (800, 400), interpolation=cv2.INTER_CUBIC)
    img_result = result_img
    image_combobox['values'] = [f" {100 - i * 10}%" for i in range(len(img_list))]
    image_combobox.set("100%")
    selected_image = 0
    show_image(result_img)


def find_middle_curve(contours, max_gap=30):
    middle_points = []
    has_anomalies = False
    large_distance_warning = False

    for contour in contours:
        contour = contour.reshape(-1, 2)
        x_to_ys = {}

        for x, y in contour:
            if x not in x_to_ys:
                x_to_ys[x] = []
            x_to_ys[x].append(y)

        for x, ys in x_to_ys.items():
            if len(ys) < 2:
                continue
            if len(ys) > 2:
                continue
            y_min, y_max = min(ys), max(ys)
            y_middle = (y_min + y_max) / 2
            middle_points.append((x, y_middle))

    middle_points = sorted(middle_points, key=lambda p: p[0])

    for i in range(1, len(middle_points)):
        x1, y1 = middle_points[i - 1]
        x2, y2 = middle_points[i]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        if distance > max_gap:
            large_distance_warning = True
            has_anomalies = True

    return middle_points, has_anomalies, large_distance_warning


def select_image(event):
    global selected_image
    selected_image = image_combobox.current()
    if selected_image >= 0 and selected_image < len(img_list):
        process_images()


def draw_axis(img, center, vector, color, scale=50):
    endpoint = (int(center[0] + vector[0] * scale), int(center[1] + vector[1] * scale))
    cv2.arrowedLine(img, (int(center[0]), int(center[1])), endpoint, color, 2, tipLength=0.3)


def show_image(image):
    global current_image
    if not isinstance(image, np.ndarray):
        return
    try:
        image_pil = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image_pil)

        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=image_tk)

        current_image = image_tk
    except Exception as e:
        print(f"Error displaying image: {e}")

def process_images():
    global img_list, img_result, mask, contour_info, contours, selected_contour, selected_image

    if len(img_list) != 10:
        messagebox.showerror("Ошибка", "Сначала загрузите 10 изображений для обработки!")
        return

    if img_result is None:
        messagebox.showerror("Ошибка", "Сначала выберите изображение для отображения контуров!")
        return

    if selected_image is None or selected_image >= len(img_list):
        messagebox.showerror("Ошибка", "Сначала выберите изображение для обработки!")
        return

    contour_info = []
    contours = []
    img = img_list[selected_image]
    img_result_copy = img_result.copy() if img_result is not None else img_list[selected_image].copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_bound = np.array([0, 0, 0])
    upper_bound = np.array([180, 50, 230])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contour_list, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filtered_contours = [cnt for cnt in contour_list if cv2.contourArea(cnt) >= min_area]

    if not filtered_contours:
        messagebox.showinfo("Результат", "Не найдено контуров с достаточной площадью.")
        return

    clean_mask = np.zeros_like(mask)
    cv2.drawContours(clean_mask, filtered_contours, -1, 255, -1)
    contour_list, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours.extend(contour_list)
    if not contours:
        messagebox.showinfo("Результат", "Контуры не найдены.")
        return

    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) < min_area:
            continue

        cv2.drawContours(img_result_copy, [contour], -1, (0, 0, 0), 1)
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        mu20 = M["mu20"] / M["m00"]
        mu02 = M["mu02"] / M["m00"]
        mu11 = M["mu11"] / M["m00"]
        cov_matrix = np.array([[mu20, mu11], [mu11, mu02]])
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        major_axis = eigenvectors[:, np.argmax(eigenvalues)]
        angle_rad = np.arctan2(-major_axis[1], major_axis[0])
        angle_deg = np.degrees(angle_rad) % 180
        draw_axis(img_result_copy, (cx, cy), major_axis, (0, 0, 255))

        if 80 <= angle_deg <= 100 or 260 <= angle_deg <= 280:
            contour_info.append(
                f"Изображение {selected_image + 1}: Главная ось вертикальная. Угол {int(angle_deg)}°"
            )
        elif 100 <= angle_deg <= 170 or 280 <= angle_deg <= 350:
            contour_info.append(
                f"Изображение {selected_image + 1}: Главная ось диагональная нисходящая. Угол {int(angle_deg)}°"
            )

        middle_segments, has_anomalies, large_distance_warning = find_middle_curve([contour], max_gap=50)
        if has_anomalies:
            contour_info.append(
                f"Изображение {selected_image + 1}: Обнаружены аномалии в контуре (большие разрывы между точками)"
            )

        if large_distance_warning:
            contour_info.append(
                f"Изображение {selected_image + 1}: Перегрузка сервера (большие расстояния между точками средней линии)"
            )

        if middle_segments and len(middle_segments) > 1:
            for i in range(1, len(middle_segments)):
                pt1 = (int(middle_segments[i - 1][0]), int(middle_segments[i - 1][1]))
                pt2 = (int(middle_segments[i][0]), int(middle_segments[i][1]))

                if (0 <= pt1[0] < img_result_copy.shape[1] and 0 <= pt1[1] < img_result_copy.shape[0] and
                        0 <= pt2[0] < img_result_copy.shape[1] and 0 <= pt2[1] < img_result_copy.shape[0]):
                    cv2.line(img_result_copy, pt1, pt2, (0, 0, 0), 1)

        show_image(img_result_copy)
        pr.update_idletasks()
    write_mode = "a"
    with open("contour_info.txt", write_mode, encoding="utf-8") as f:
        for info in contour_info:
            if "вертикальная" in info or "диагональная нисходящая" in info or "аномалии" in info or "всплески" in info:
                f.write(info + "\n")
        f.write("-" * 30 + "\n")


def main():
    global pr, canvas, image_combobox
    pr = Toplevel()  # Use Toplevel instead of Tk
    pr.title("Обработка изображений")
    canvas = Canvas(pr, width=800, height=500, bg="white")
    canvas.pack()
    Button(pr, text="Загрузить папку с изображениями", command=load_images_from_folder).pack(pady=5)
    image_combobox = ttk.Combobox(pr, values=[f" {100 - i * 10}%" for i in range(10)])
    image_combobox.set("100%")
    image_combobox.bind("<<ComboboxSelected>>", select_image)
    image_combobox.pack(pady=5)
    pr.mainloop()