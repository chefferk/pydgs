import DGS
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


window = Tk()
# window.iconbitmap("py.ico")
window.title("pyDGS")
window.geometry("330x400")
window.resizable(False, False)
# window.tk_setPalette(background='#e6e6e6')


def save_stats():
    with open("output.txt", "w") as f:
        x = clicked()
        print(x, file=f)
    print("Stats saved at output.txt")


menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label="New")
new_item.add_command(label="Edit")
new_item.add_command(label="Save", command=save_stats)
menu.add_cascade(label="File", menu=new_item)
window.config(menu=menu)


def pick_image():
    filee = filedialog.askopenfilename()
    messagebox.showinfo("Image", filee)
    global file_name
    file_name = filee
    print(file_name)
    return filee


# TODO: create funciton that checks data tyes are correct
#       set default values
def clicked():
    # try:
    density = int(dens.get())
    resolution = int(res.get())
    dofilter = 0  # this causes an issue in pyDGS when set to 1
    notes = int(no.get())
    maxscale = int(maxs.get())
    verbose = 0
    x = 0

    try:
        image_file = file_name
    except Exception as e:
        image_file = btnn.invoke()
    dgs_stats = DGS.dgs(
        image_file, density, resolution, dofilter, maxscale, notes, verbose, x
    )

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
    return text
    # except TclError as e:
    #     print(e)
    #     return 'failed'


# def disp(stats):
#     text = (
#         f'Mean grain size: {stats['mean grain size']}\n'
#         f'Mean grain size: {stats['mean grain size']}\n'
#         f'Mean grain size: {stats['mean grain size']}\n'
#         f'Mean grain size: {stats['mean grain size']}\n'
#     )
#     return text


def create_window():
    wind = Toplevel(window)
    display = Label(wind, text=clicked())
    display.pack()

    plt.figure(1)
    plt.plot([1, 2, 3, 4])

    plt.figure(2)
    plt.plot([4, 3, 2, 1])

    plt.show()


def test():
    density = dens.get()
    resolution = res.get()
    dofilter = 0
    notes = no.get()
    maxscale = maxs.get()
    verbrose = 1
    x = 1
    return (density, resolution, dofilter, notes, maxscale, verbrose, x)


# ---------- new window ---------- #
# b = Button(window, text="Create new window", command=create_window)
# b.grid(column=1, row=0)

# ---------- select image ---------- #
btnn = ttk.Button(window, text="Select image", command=pick_image)
btnn.grid(column=0, row=0)

# ---------- density ---------- #
lbl = ttk.Label(window, text="Density", justify="left")
lbl.grid(column=0, row=1)
dens = ttk.Spinbox(window, from_=1, to=100, width=5)
dens.grid(column=1, row=1)

# ---------- resolution ---------- #
lbl = ttk.Label(window, text="Resolution")
lbl.grid(column=0, row=2)
res = ttk.Spinbox(window, from_=0, to=100, width=5)
res.grid(column=1, row=2)

# ---------- dofilter ---------- #
lbl = ttk.Label(window, text="Dofilter")
lbl.grid(column=0, row=3)
rad1 = ttk.Radiobutton(window, text="Yes", value=1)
rad2 = ttk.Radiobutton(window, text="No", value=0)
rad1.grid(column=1, row=3)
rad2.grid(column=2, row=3)

# ---------- notes---------- #
lbl = ttk.Label(window, text="Notes")
lbl.grid(column=0, row=4)
no = ttk.Spinbox(window, from_=0, to=8, width=5)
no.grid(column=1, row=4)

# ---------- maxscale ---------- #
lbl = ttk.Label(window, text="Maxscale")
lbl.grid(column=0, row=5)
maxs = ttk.Spinbox(window, from_=2, to=40, width=5)
maxs.grid(column=1, row=5)

# ---------- process ---------- #
btn = ttk.Button(window, text="Process", command=create_window)
btn.grid(column=0, row=6)


window.mainloop()
