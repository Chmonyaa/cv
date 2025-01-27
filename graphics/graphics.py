import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import tkinter as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import filedialog

#plasma

def load_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path, sep=';', header=0)
        df.columns = ['Index', 'X', 'Y', 'Count']
        df['X'] = pd.to_numeric(df['X'])
        df['Y'] = pd.to_numeric(df['Y'])
        df['Count'] = pd.to_numeric(df['Count'])
        df_filtered = df[df['Count'].between(0, df['Count'].max())]
        plt.clf()
        plt.scatter(df_filtered['X'], df_filtered['Y'], c=df_filtered['Count'], cmap=custom_cmap,
                    norm=mcolors.LogNorm(), alpha=1, s=2)
        plt.colorbar(label='Density')
        plt.xlabel('KB/s')
        plt.ylabel('Service time (ms)')
        plt.xlim(df['X'].min() * 0.8, df['X'].max() * 1.2)
        plt.ylim(df['Y'].min() * 0.8, df['Y'].max() * 1.2)
        plt.xscale('log', base=2)
        plt.yscale('log', base=2)

        canvas.draw()
def confirm_exit():
    root.destroy()
    sys.exit()

colors = [
    (0, (5 / 255, 240 / 255, 221 / 255)),
    (0.25, (68 / 255, 211 / 255, 9 / 255)),
    (0.5, (254 / 255, 233 / 255, 0 / 255)),
    (0.75, (249 / 255, 78 / 255, 49 / 255)),
    (1, (248 / 255, 30 / 255, 178 / 255))
]

n_bins = 100
cmap_name = "custom_cmap"
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

root = Tk()
root.geometry("1100x510")

button_1 = Button(root, text="Выбрать файл", command=load_csv_file)
button_1.pack(pady=5)
label = ttk.Label(text="")
label.pack(pady=5)
fig = plt.figure(figsize=(10.96, 4.45))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
root.protocol('WM_DELETE_WINDOW', confirm_exit)
root.mainloop()
