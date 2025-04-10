import tkinter as tk
from tkinter import messagebox
import re
import graphics
import processing


def evaluate_report():
    anomalies_on_8_10 = False
    anomalies_on_other = False
    axis_info = {}
    anomalies_details = []

    try:
        with open("contour_info.txt", "r", encoding="utf-8") as file:
            contour_info = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл contour_info.txt не найден.")
        return

    for line in contour_info:
        if "Главная ось" in line:
            match = re.search(r"Изображение (\d+): Главная ось (\S+)", line)
            if match:
                image_num = int(match.group(1))
                axis = match.group(2)
                axis_info[image_num] = axis
                if image_num in [8, 9, 10]:
                    anomalies_on_8_10 = True
                    anomalies_details.append(f"Изображение {image_num}: Главная ось - {axis}")
                else:
                    anomalies_on_other = True
                    anomalies_details.append(f"Изображение {image_num}: Главная ось - {axis}")

        if "Обнаружены аномалии" in line:
            match = re.search(r"Изображение (\d+): Обнаружены аномалии", line)
            if match:
                image_num = int(match.group(1))
                if (image_num == 8 and image_num == 9) or (image_num == 9 and image_num == 10) or (image_num == 8 and image_num == 10) or (image_num == 8 and image_num == 9 and image_num==10):
                    anomalies_on_8_10 = True
                    anomalies_details.append(f"Аномалии обнаружены на изображении {image_num}")
                else:
                    anomalies_on_other = True
                    anomalies_details.append(f"Аномалии обнаружены на изображении {image_num}")

    if anomalies_on_8_10:
        messagebox.showinfo("Оценка", "Аномалии в 10-30% самых частых запросов: Плохой результат.\n")
    elif anomalies_on_other:
        messagebox.showinfo("Оценка", "Аномалии в 40-100% частых запросах: Удовлетворительно.\n")
    else:
        messagebox.showinfo("Оценка", "Без аномалий: Хороший результат.\n")




def run_script_1():
    graphics.main()


def run_script_2():
    processing.main()


def main():
    root = tk.Tk()
    root.title("Меню скриптов")
    button1 = tk.Button(root, text="Запустить скрипт 1", command=run_script_1)
    button1.pack(pady=10)
    button2 = tk.Button(root, text="Запустить скрипт 2", command=run_script_2)
    button2.pack(pady=10)
    evaluate_button = tk.Button(root, text="Проверить отчет", command=evaluate_report)
    evaluate_button.pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()