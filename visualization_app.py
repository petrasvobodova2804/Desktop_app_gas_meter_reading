import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from detection_app import main_detect, load_network_at_begining
import numpy as np
import csv
from statistics_app import read_csv
from tkinter import ttk

# Create Tkinter window
window = tk.Tk()
window.title("Gas Meter Reader")

style=ttk.Style()
style.theme_use("clam")
style.configure("RoundedButton.TButton", borderwidth=6, relief="groove", bordercolor="gray", padding=2, font=("Arial", 8))

# Create an empty black image
black_image = Image.fromarray(np.zeros((480, 640), dtype=np.uint8), 'L')

# Convert the black image to PhotoImage
black_image_tk = ImageTk.PhotoImage(black_image)

# Create a shared variable to store the result
res = None
current_index = 0

network, class_names, class_colors = load_network_at_begining()


def run_main_detect(file_path=None, dir_path=None):
    global res, current_index
    if file_path:
        res = main_detect(file_path, network, class_names, class_colors)
    elif dir_path:
        res = main_detect(dir_path, network, class_names, class_colors)
        current_index = 0

    for j in range(0,5):
        entries[j].delete(0, tk.END)

    # Convert the processed image to Tkinter-compatible format
    if len(res) == 0:
        img = black_image.copy()
    else:
        img = res[current_index].image
        if not isinstance(img, Image.Image):
            img = Image.fromarray(res[current_index].image)
        # Set predicted labels to Entries
        for i in range(0, len(res[current_index].detect_label)):
            if i < 5:
                entries[i].insert(0, res[current_index].detect_label[i])


    # Resize the image to fit the label dimensions
    img = img.resize((640, 480))

    # Convert the image to PhotoImage
    res_tk = ImageTk.PhotoImage(img)

    # Update the Tkinter label with the new image
    label.configure(image=res_tk)
    label.image = res_tk
    
    size_res = len(res)
    label_text_index.set(str(current_index+1)+"/"+str(size_res))


def move_left():
    global current_index
    if current_index > 0:
        current_index -= 1
        run_main_detect()
        size_res = len(res)
        label_text_index.set(str(current_index+1)+"/"+str(size_res))

def move_right():
    global current_index
    if current_index < len(res) - 1:
        current_index += 1
        run_main_detect()
        size_res = len(res)
        label_text_index.set(str(current_index+1)+"/"+str(size_res))


def save_to_csv():
    # specify csv file
    csv_file = 'Results.csv'
    # uložit do csv souboru
    # Write the predictions to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(0, len(res)):
            l = []
            for k in range(0, len(res[i].detect_label)):
                l.append(res[i].detect_label[k])
            writer.writerow(l)
            print(l)

def save():
    check_num = len(res[current_index].detect_label)
    if check_num == 5:
        for i in range(0, 5):
            res[current_index].detect_label[i] = entries[i].get()
    else:
        for i in range(0, (5-check_num)):
            res[current_index].detect_label.append(9)
        for i in range(0, 5):
            res[current_index].detect_label[i] = entries[i].get()


def create_tabs():
    tab0 = ttk.Frame(tab_control)
    tab_control.add(tab0, text="Home")
    image_pil0 = Image.open("imgs/output_board.png").convert("RGB")
    image_pil0 = image_pil0.resize((600, 420))
    image_tk0 = ImageTk.PhotoImage(image_pil0)
    label0 = tk.Label(tab0, image=image_tk0)
    label0.pack()
    label0.image = image_tk0

    # Create the first tab (Tab 1)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Overview")
    # Convert the OpenCV image to PIL format
    image_pil = Image.open("imgs/gas_meter.png").convert("RGB")
    # Resize the image if needed
    image_pil = image_pil.resize((600, 420))
    # Convert the PIL image to Tkinter-compatible format
    image_tk = ImageTk.PhotoImage(image_pil)
    # Create a Label widget to display the image
    label = tk.Label(tab1, image=image_tk)
    label.pack()
    # Update the image label reference to prevent garbage collection
    label.image = image_tk


    # Create the second tab (Tab 2)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Differences")
    image_pil2 = Image.open("imgs/gas_meter_diff.png").convert("RGB")
    image_pil2 = image_pil2.resize((600, 420))
    image_tk2 = ImageTk.PhotoImage(image_pil2)
    label2 = tk.Label(tab2, image=image_tk2)
    label2.pack()
    label2.image = image_tk2

    # Create the third tab (Tab 3)
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text="Box Plot")
    image_pil3 = Image.open("imgs/box_plot_differences.png").convert("RGB")
    image_pil3 = image_pil3.resize((600, 420))
    image_tk3 = ImageTk.PhotoImage(image_pil3)
    label3 = tk.Label(tab3, image=image_tk3)
    label3.pack()
    label3.image = image_tk3

    # Create the fourthtab (Tab 5)
    tab4 = ttk.Frame(tab_control)
    tab_control.add(tab4, text='Distribution')
    image_pil4 = Image.open("imgs/distributions_of_differences.png").convert("RGB")
    image_pil4 = image_pil4.resize((600, 420))
    image_tk4 = ImageTk.PhotoImage(image_pil4)
    label4 = tk.Label(tab4, image=image_tk4)
    label4.pack()
    label4.image = image_tk4

    # Create the fifth tab (Tab 5)
    tab5 = ttk.Frame(tab_control)
    tab_control.add(tab5, text='KDE Graph')
    image_pil5 = Image.open("imgs/kernel_density.png").convert("RGB")
    image_pil5 = image_pil5.resize((600, 420))
    image_tk5 = ImageTk.PhotoImage(image_pil5)
    label5 = tk.Label(tab5, image=image_tk5)
    label5.pack()
    label5.image = image_tk5

    # Create the sixth tab (Tab 6)
    tab6 = ttk.Frame(tab_control)
    tab_control.add(tab6, text='Clustering')
    image_pil6 = Image.open("imgs/clustering.png").convert("RGB")
    image_pil6 = image_pil6.resize((600, 420))
    image_tk6 = ImageTk.PhotoImage(image_pil6)
    label6 = tk.Label(tab6, image=image_tk6)
    label6.pack()
    label6.image = image_tk6

    # Create the seventh tab (Tab 7)
    tab7 = ttk.Frame(tab_control)
    tab_control.add(tab7, text='Autocorrelation')
    image_pil7 = Image.open("imgs/autocorrelation.png").convert("RGB")
    image_pil7 = image_pil7.resize((600, 420))
    image_tk7 = ImageTk.PhotoImage(image_pil7)
    label7 = tk.Label(tab7, image=image_tk7)
    label7.pack()
    label7.image = image_tk7



def statistics():
    read_csv()
    create_tabs()



# Add buttons for file and directory selection
file_button = ttk.Button(window, text="Choose File", width = 14, command=lambda: run_main_detect(file_path=filedialog.askopenfilename()))
file_button.grid(row=0, column=8, padx=5, pady=10)

dir_button = ttk.Button(window, text="Choose Directory", width = 16, command=lambda: run_main_detect(dir_path=filedialog.askdirectory()))
dir_button.grid(row=0, column=9, columnspan=2, padx=5, pady=10)

#--------------black-image-as-background
label = tk.Label(window, image=black_image_tk)
label.grid(row=2, column=0, columnspan=11, padx=5, pady=5)

#-------------entry-text-fiels-----------------------
# Empty space in columns 0 and 1
empty_label0 = tk.Label(window, text=" ", width=5)
empty_label0.grid(row=3, column=0)
empty_label1 = tk.Label(window, text=" ", width=5)
empty_label1.grid(row=3, column=1)

entry1 = ttk.Entry(window, width=5)
entry1.grid(row=3, column=2, padx=5, pady=5, ipady=10)

entry2 = ttk.Entry(window, width=5)
entry2.grid(row=3, column=3, padx=5, pady=5, ipady=10)

entry3 = ttk.Entry(window, width=5)
entry3.grid(row=3, column=4, padx=5, pady=5, ipady=10)

entry4 = ttk.Entry(window, width=5)
entry4.grid(row=3, column=5, padx=5, pady=5, ipady=10)



entry5 = ttk.Entry(window, width=5)
entry5.grid(row=3, column=6, padx=5, pady=5, ipady=10)

entries = [entry1, entry2, entry3, entry4, entry5]

#--------------SAVE-button-------------------------------
image_save = Image.open("imgs/save.png")  
width, height = image_save.size
image_save = image_save.resize((int(width*0.08),int(height*0.08)))
photo_save = ImageTk.PhotoImage(image_save)
style.configure('buttondesign3.TButton', width=9, anchor='center',image=photo_save, padding=2)
save_button = ttk.Button(window, style='buttondesign3.TButton', text="Save", compound='top', command=save)
save_button.grid(row=3, column=7, padx=5, pady=5)

#-------------save-to-CSV-button--------------------------
image_csv = Image.open("imgs/csv.png")  
width, height = image_csv.size
image_csv = image_csv.resize((int(width*0.08),int(height*0.08)))
photo_csv = ImageTk.PhotoImage(image_csv)
style.configure('buttondesign1.TButton', width=9, anchor='center',image=photo_csv, padding=2)
save_button = ttk.Button(window, style='buttondesign1.TButton', text="CSV save", compound='top', command=save_to_csv)
save_button.grid(row=3, column=9, padx=5, pady=5)

#------------left-right-ARROWS-------------------
image1 = Image.open("imgs/arrows.png")  
width, height = image1.size
image1 = image1.resize((int(width*0.015),int(height*0.015)))
photo1 = ImageTk.PhotoImage(image1)
style.configure('buttondesign4.TButton', width=9, anchor='center',image=photo1, padding=2)
left_button = ttk.Button(window, style='buttondesign4.TButton', command=move_left)
left_button.grid(row=1, column=5, padx=5, pady=5, ipadx=1, ipady=1)
image2 = image1.transpose(Image.FLIP_LEFT_RIGHT)
photo2 = ImageTk.PhotoImage(image2)
style.configure('buttondesign5.TButton', width=9, anchor='center',image=photo2, padding=2)
right_button = ttk.Button(window, style='buttondesign5.TButton', command=move_right)
right_button.grid(row=1, column=7, padx=5, pady=5, ipadx=1, ipady=1)

# Create a StringVar to hold the label's text
label_text_index = tk.StringVar()
label_text_index.set("0/0")
# Create a label with the text from the StringVar
label_index = tk.Label(window, textvariable=label_text_index)
label_index.grid(row=1, column=6)

#------------create-STATISTICS-button----------------------
image_stat = Image.open("imgs/stati.png")  
width, height = image_stat.size
image_stat = image_stat.resize((int(width*0.08),int(height*0.08)))
photo_stat = ImageTk.PhotoImage(image_stat)
style.configure('buttondesign2.TButton', width=9, anchor='center',image=photo_stat, padding=2)
statistics_button = ttk.Button(window, style='buttondesign2.TButton', text="Statistics", compound='top', command=statistics)
statistics_button.grid(row=3, column=10, padx=5, pady=10)

# Create a Notebook widget
tab_control = ttk.Notebook(window)
tab_control.grid(row=2, column=11, padx=5, pady=5)

# Run the Tkinter event loop
window.mainloop()

# Access the result (res) outside the Tkinter event loop
print("Result:", res)