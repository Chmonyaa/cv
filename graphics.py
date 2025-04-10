import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import tkinter as ttk
from tkinter import *
from tkinter import filedialog
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

start_x, start_y, end_x, end_y = None, None, None, None
drawing = False


def confirm_exit():
    sys.exit()


def load_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    process_csv(file_path, os.path.dirname(file_path))


def load_csv_folder():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not csv_files:
        print("В выбранной папке нет CSV-файлов.")
        return

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        process_csv(file_path, folder_path)


def process_csv(file_path, output_folder):
    df = pd.read_csv(file_path, sep=',', header=None)
    if df.shape[1] == 1:
        df = df[0].str.split(',', expand=True)
    if df.shape[1] < 3:
        print(f"Ошибка: недостаточно данных в файле {file_path}")
        return
    df.columns = ['X', 'Y', 'Count']
    df['X'] = pd.to_numeric(df['X'], errors='coerce')
    df['Y'] = pd.to_numeric(df['Y'], errors='coerce')
    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    df.dropna(inplace=True)
    df_filtered = df[df['Count'].between(0, df['Count'].max())]
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    save_path = os.path.join(output_folder, file_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_images(df_filtered, os.path.join(save_path, file_name))


def save_images(df, file_path):
    global img
    color_maps = [
        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (0 / 255, 0 / 255, 0 / 255)),
         (0.2, (0 / 255, 0 / 255, 0 / 255)),
         (0.3, (0 / 255, 0 / 255, 0 / 255)),
         (0.4, (0 / 255, 0 / 255, 0 / 255)),
         (0.5, (0 / 255, 0 / 255, 0 / 255)),
         (0.6, (0 / 255, 0 / 255, 0 / 255)),
         (0.7, (0 / 255, 0 / 255, 0 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (0 / 255, 0 / 255, 0 / 255)),
         (0.3, (0 / 255, 0 / 255, 0 / 255)),
         (0.4, (0 / 255, 0 / 255, 0 / 255)),
         (0.5, (0 / 255, 0 / 255, 0 / 255)),
         (0.6, (0 / 255, 0 / 255, 0 / 255)),
         (0.7, (0 / 255, 0 / 255, 0 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (0 / 255, 0 / 255, 0 / 255)),
         (0.4, (0 / 255, 0 / 255, 0 / 255)),
         (0.5, (0 / 255, 0 / 255, 0 / 255)),
         (0.6, (0 / 255, 0 / 255, 0 / 255)),
         (0.7, (0 / 255, 0 / 255, 0 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (255 / 255, 255 / 255, 255 / 255)),
         (0.4, (0 / 255, 0 / 255, 0 / 255)),
         (0.5, (0 / 255, 0 / 255, 0 / 255)),
         (0.6, (0 / 255, 0 / 255, 0 / 255)),
         (0.7, (0 / 255, 0 / 255, 0 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (255 / 255, 255 / 255, 255 / 255)),
         (0.4, (255 / 255, 255 / 255, 255 / 255)),
         (0.5, (0 / 255, 0 / 255, 0 / 255)),
         (0.6, (0 / 255, 0 / 255, 0 / 255)),
         (0.7, (0 / 255, 0 / 255, 0 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (255 / 255, 255 / 255, 255 / 255)),
         (0.4, (255 / 255, 255 / 255, 255 / 255)),
         (0.5, (255 / 255, 255 / 255, 255 / 255)),
         (0.6, (0 / 255, 0 / 255, 0 / 255)),
         (0.7, (0 / 255, 0 / 255, 0 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (255 / 255, 255 / 255, 255 / 255)),
         (0.4, (255 / 255, 255 / 255, 255 / 255)),
         (0.5, (255 / 255, 255 / 255, 255 / 255)),
         (0.6, (255 / 255, 255 / 255, 255 / 255)),
         (0.7, (0 / 255, 0 / 255, 0 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (255 / 255, 255 / 255, 255 / 255)),
         (0.4, (255 / 255, 255 / 255, 255 / 255)),
         (0.5, (255 / 255, 255 / 255, 255 / 255)),
         (0.6, (255 / 255, 255 / 255, 255 / 255)),
         (0.7, (255 / 255, 255 / 255, 255 / 255)),
         (0.8, (0 / 255, 0 / 255, 0 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (255 / 255, 255 / 255, 255 / 255)),
         (0.4, (255 / 255, 255 / 255, 255 / 255)),
         (0.5, (255 / 255, 255 / 255, 255 / 255)),
         (0.6, (255 / 255, 255 / 255, 255 / 255)),
         (0.7, (255 / 255, 255 / 255, 255 / 255)),
         (0.8, (255 / 255, 255 / 255, 255 / 255)),
         (0.9, (0 / 255, 0 / 255, 0 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [(0, (255 / 255, 255 / 255, 255 / 255)),
         (0.1, (255 / 255, 255 / 255, 255 / 255)),
         (0.2, (255 / 255, 255 / 255, 255 / 255)),
         (0.3, (255 / 255, 255 / 255, 255 / 255)),
         (0.4, (255 / 255, 255 / 255, 255 / 255)),
         (0.5, (255 / 255, 255 / 255, 255 / 255)),
         (0.6, (255 / 255, 255 / 255, 255 / 255)),
         (0.7, (255 / 255, 255 / 255, 255 / 255)),
         (0.8, (255 / 255, 255 / 255, 255 / 255)),
         (0.9, (255 / 255, 255 / 255, 255 / 255)),
         (1, (0 / 255, 0 / 255, 0 / 255))],

        [
            (0, (5 / 255, 240 / 255, 221 / 255)),
            (0.25, (68 / 255, 211 / 255, 9 / 255)),
            (0.5, (254 / 255, 233 / 255, 0 / 255)),
            (0.75, (249 / 255, 78 / 255, 49 / 255)),
            (1, (248 / 255, 30 / 255, 178 / 255))
        ]
    ]

    for i, colors in enumerate(color_maps):
        custom_cmap = mcolors.LinearSegmentedColormap.from_list(f"custom_cmap_{i}", colors, N=100)
        plt.clf()
        scatter = plt.scatter(df['X'], df['Y'], c=df['Count'], cmap=custom_cmap,
                              norm=mcolors.LogNorm(), alpha=1, s=2)
        plt.colorbar(label='Density')
        plt.xlabel('KB/s')
        plt.ylabel('Service time (ms)')
        plt.xlim(df['X'].min() * 0.8, df['X'].max() * 1.2)
        plt.ylim(df['Y'].min() * 0.8, df['Y'].max() * 1.2)
        plt.xscale('log', base=2)
        plt.yscale('log', base=2)
        plt.draw()

        img_path = f"temp_image_{i}.png"
        plt.savefig(img_path, bbox_inches='tight')
        img = Image.open(img_path)
        cropped_img = img.crop((72, 15, 737, 320))
        cropped_img.save(f"{file_path}_{i}.png")
        print(f"Изображение {i + 1} сохранено в {file_path}_{i}.png")

        if os.path.exists(img_path):
            os.remove(img_path)
            print(f"Временное изображение {img_path} удалено.")


def main():
    r = Tk()
    r.geometry("1100x510")

    button_1 = Button(r, text="Выбрать папку csv", command=load_csv_folder)
    button_1.pack(pady=5)

    button_2 = Button(r, text="Выбрать файл csv", command=load_csv_file)
    button_2.pack(pady=5)

    label = ttk.Label(text="")
    label.pack(pady=5)

    fig = plt.figure(figsize=(10.96, 4.45))
    canvas = FigureCanvasTkAgg(fig, master=r)
    canvas.get_tk_widget().pack()

    r.protocol('WM_DELETE_WINDOW', confirm_exit)
