import DGS
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from tkinter.ttk import Progressbar
import time
import threading
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("pyDGS")
        self.geometry("330x400")
        self.resizable(False, False)
        # self.iconbitmap("py.ico")

        self.file_name = None

        # ---------- select image ---------- #
        self.btnn = ttk.Button(self, text="Select image", command=self.pick_image)
        self.btnn.grid(column=0, row=0, padx=10, pady=10)

        # ---------- picked image ---------- #
        self.img_lbl = ttk.Label(self, text='No image selected')
        self.img_lbl.grid(column=1, row=0)

        # ---------- remove image ---------- #
        self.del_btn = ttk.Button(self, text="X", command=self.rem_img, state='disabled', width=3)
        self.del_btn.grid(column=2, row=0)

        # ---------- density ---------- #
        self.lbl = ttk.Label(self, text="Density", anchor='w', width=10)
        self.lbl.grid(column=0, row=1)
        self.dens = ttk.Spinbox(self, from_=1, to=100, width=5)
        self.dens.grid(column=1, row=1, padx=10, pady=10)
        self.dens.set(10)

        # ---------- resolution ---------- #
        self.lbl = ttk.Label(self, text="Resolution", anchor='w', width=10)
        self.lbl.grid(column=0, row=2)
        self.res = ttk.Spinbox(self, from_=0, to=100, width=5)
        self.res.grid(column=1, row=2)
        self.res.set(1)

        # ---------- dofilter ---------- #
        self.lbl = ttk.Label(self, text="Dofilter", anchor='w', width=10)
        self.lbl.grid(column=0, row=3, padx=10, pady=10)
        self.rad1 = ttk.Radiobutton(self, text="Yes", value=1)
        self.rad2 = ttk.Radiobutton(self, text="No", value=0)
        self.rad1.grid(column=1, row=3)
        self.rad2.grid(column=2, row=3)

        # ---------- notes---------- #
        self.lbl = ttk.Label(self, text="Notes", anchor='w', width=10)
        self.lbl.grid(column=0, row=4, padx=10, pady=10)
        self.no = ttk.Spinbox(self, from_=0, to=8, width=5)
        self.no.grid(column=1, row=4)
        self.no.set(8)

        # ---------- maxscale ---------- #
        self.lbl = ttk.Label(self, text="Maxscale", anchor='w', width=10)
        self.lbl.grid(column=0, row=5, padx=10, pady=10)
        self.maxs = ttk.Spinbox(self, from_=2, to=40, width=5)
        self.maxs.grid(column=1, row=5)
        self.maxs.set(8)

        # ---------- process ---------- #
        self.btn = ttk.Button(self, text="Process", command=self.process)
        self.btn.grid(column=0, row=6, padx=10, pady=10)

    def rem_img(self):
        self.file_name = None
        self.img_lbl.configure(text='No image selected')
        self.del_btn.configure(state='disabled')
    
    def pick_image(self):
        '''opens dialog to choose file'''
        picked_file = filedialog.askopenfilename()
        # messagebox.showinfo("Image", picked_file)
        self.file_name = picked_file

        # ---------- picked image ---------- #.
        self.img_lbl.configure(text=os.path.basename(self.file_name))

        # ---------- remove image ---------- #
        self.del_btn.configure(state='active')

        return picked_file
    
    # TODO: Make this a JSON file with more meta data
    #       Also write some software to parse this output in a notebook
    def save_stats(self):
        with open("output.txt", "w") as f:
            x = self.output_text
            print(x, file=f)
        self.output_text.to_csv('output.csv')
        print("Stats saved at output.txt")

    # TODO: figure out the threading and have some sort of progress bar
    def process(self):
        self.create_window()
    
    def create_window(self):
        '''creates new window with output information along with graphs'''
        if self.file_name is None:
            messagebox.showinfo("Image", 'Please select an image first.')
            return
        
        output_text, dgs_stats = self.clicked()
        self.wind = Toplevel(self)

        # self.menubar = Menu(self.wind)
        # self.new_item = Menu(self.menubar)
        # self.new_item.add_command(label="New")
        # self.wind.config(menu=self.menubar)

        menubar = Menu(self.wind)
        self.wind.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Export", command=self.save_stats)
        menubar.add_cascade(label="File", menu=fileMenu)

        # self.iconbitmap("py.ico")
        self.display = Label(self.wind, text=output_text)
        self.display.pack()

        plt.figure(1, figsize=(8,10))
        plt.semilogx(dgs_stats['grain size bins'], dgs_stats['grain size frequencies'], 'k-o', label='GSD')
        plt.legend()
        plt.xlabel('Grain Size [pixels]')
        plt.ylabel('Normalized frequency [-]')

        plt.figure(2, figsize=(10,10))
        plt.plot(dgs_stats['grain size bins'][:5], np.cumsum(dgs_stats['grain size frequencies'][:5]), 'k-o', label='GSD')
        plt.legend()
        plt.xlabel('Grain Size [pixels]')
        plt.ylabel('Normalized frequency [-]')
        counter = 0
        for k in dgs_stats['percentile_values']:
            plt.axvline(k)
            plt.text(k,1.03,str(dgs_stats['percentiles'][counter]), rotation=45)
            counter += 1

        plt.show()

    # TODO: create funciton that checks data tyes are correct
    #       more testing for file types and stuff
    def clicked(self):
        # try:
        # density = int(self.dens.get())
        # resolution = int(self.res.get())
        # dofilter = 0  # this causes an issue in pyDGS when set to 1
        # notes = int(self.no.get())
        # maxscale = int(self.maxs.get())
        # verbose = 0
        # x = 0

        density = 10
        resolution = 1
        dofilter = 1  # this causes an issue in pyDGS when set to 1
        notes = 16
        maxscale = 8
        verbose = 1
        x = -0.5

        if self.file_name is not None:
            image_file = self.file_name
        else:
            # flash messeage about selecting image first
            messagebox.showinfo("Image", 'Please select an image first.')
            return
            # image_file = self.btnn.invoke()

        dgs_stats = DGS.dgs(
            image_file, density, resolution, dofilter, maxscale, notes, verbose, x
        )

        myDict = {
            'Mean grain size': [dgs_stats['mean grain size']],
            'Grain size sorting': [dgs_stats['grain size sorting']],
            'Grain size skewness': [dgs_stats['grain size skewness']],
            'Grain size kurtosis': [dgs_stats['grain size kurtosis']],
            'Percentiles': [dgs_stats['percentiles']],
            'Percentile_values': [dgs_stats['percentile_values']],
            'Grain size frequencies': [dgs_stats['grain size frequencies']],
            'Grain size bins': [dgs_stats['grain size bins']],
        }

        df = pd.DataFrame.from_dict(myDict, orient='index')

        text = (
            f"Mean grain size: {dgs_stats['mean grain size']}\n"
            f"Grain size sorting: {dgs_stats['grain size sorting']}\n"
            f"Grain size skewness: {dgs_stats['grain size skewness']}\n"
            f"Grain size kurtosis: {dgs_stats['grain size kurtosis']}\n"
            f"Percentiles: {dgs_stats['percentiles']}\n"
            f"Percentile_values: {dgs_stats['percentile_values']}\n"
            f"Grain size frequencies: {dgs_stats['grain size frequencies']}\n"
            f"Grain size bins: {dgs_stats['grain size bins']}\n"
        )
        print('finished processing')

        self.output_text = df
        return df, dgs_stats

if __name__ == "__main__":
    root = Root()
    root.mainloop()