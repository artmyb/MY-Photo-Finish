#pyinstaller main.py --onefile --windowed --name "MY Photo-Finish" --manifest MYPhoto-Finish.manifest --icon "images/main.png"
#pyinstaller main.py --onefile --windowed --add-data "path_to_tkinter;tkinter" --hidden-import=tkinter --name "MY Photo-Finish" --icon "images/main.png"

print("Loading az bekle...")
import tkinter
import os
import traceback

tkinter_path = os.path.dirname(tkinter.__file__)
print(f"Tkinter is located at: {tkinter_path}")
import tkinter as tk
import threading
from PIL import ImageTk, Image
import numpy as np

import base64
from io import BytesIO

# Import the encoded image data
from splash_image import image_data
from generate_image_button import image_data as generate_image_bt
from update_image_button import image_data as update_image_bt
from preview_button import image_data as preview_bt
from apply_button import image_data as apply_bt

from import_video_button import image_data as import_video_bt
from import_video_button_w import image_data as import_video_bt_w
from export_button import image_data as export_bt
from export_button_w import image_data as export_bt_w
from add_button import image_data as add_bt
from remove_button import image_data as remove_bt
from add_button_w import image_data as add_bt_w
from remove_button_w import image_data as remove_bt_w
from import_button import image_data as import_bt
from import_button_w import image_data as import_bt_w
from main_icon import image_data as main_icon
from add_instance_button import image_data as add_instance_bt
from add_instance_button_w import image_data as add_instance_bt_w
from video import image_data as video_bt
from play import image_data as play_bt
from pause import image_data as pause_bt
from stop import image_data as stop_bt
from play_w import image_data as play_bt_w
from pause_w import image_data as pause_bt_w
from stop_w import image_data as stop_bt_w
from video_l import image_data as video_l_bt
from video_l_w import image_data as video_l_bt_w



#the below part is for splash screen
splash = tk.Tk()
splash.resizable(False, False)

splash.configure(bg='black')

window_width = 700
window_height = 250
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
splash.geometry(f'{window_width}x{window_height}+{x}+{y}')
splash.attributes("-topmost", True)
splash_canvas = tk.Canvas(splash, bg='black', width=window_width, height=window_height, highlightthickness=0)
splash_canvas.pack(fill="both", expand=True)

image_data_bytes = base64.b64decode(image_data)
image = Image.open(BytesIO(image_data_bytes))
splash_icon = ImageTk.PhotoImage(image)

splash_canvas.create_image(0, 0, anchor=tk.NW, image=splash_icon)

splash.overrideredirect(True)

splash.after(5000, splash.destroy)

splash.mainloop()





import time

import cv2
import tkinter as tk
from tkinter import filedialog

import os
from PIL import ImageDraw, ImageFont
import numpy as np
import sounddevice as sd
from tkinter import ttk
import tkinter.messagebox
import io
from moviepy.editor import VideoFileClip
import proglog
import soundfile as sf
#import tktable


from tkinter.filedialog import asksaveasfile
import pandas as pd
import pyautogui
import openpyxl
from functools import partial
import io
import base64

from matplotlib import pyplot as plt
#from pydub import AudioSegment
#import simpleaudio as sa

"""
this is for VideoFileClip function to work without cmd. 
after generating executable with --windowed option, which is for running the app without cmd,
the VideoFileClip function doesn't work because it tries to print a progress bar in the cmd.
using this class below, we use another progress bar instead of printing to the cmd, that
actually does nothing.
"""
class DummyLogger(proglog.ProgressBarLogger):
    def callback(self, **changes):
        pass

    def bars_callback(self, bar, attr, value, old_value=None):
        pass



#a table that can be edited with interaction
class EditableTable(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg="#222222")
        self.pack(fill=tk.BOTH, expand=True)

        self.title_canvas = tk.Canvas(self, height=50, bg="#222222", bd=0, highlightthickness=0)
        self.title_canvas.pack(fill=tk.X, expand=False)

        self.title = self.title_canvas.create_text(
            self.title_canvas.winfo_width() // 2, 25,
            text="Title: ",
            anchor=tk.W,
            fill="white"
        )

        self.root = root
        self.headers = ["Lane", "ID", "Name", "Date of Birth", "Affiliation", "License", "Time", "Place"]
        self.data = []

        self.results = []

        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Calibri", 10), background="#222222", fieldbackground="#222222",
                        foreground="#CCCCCC")
        style.map('Custom.Treeview', background=[('selected', '#444444')], foreground=[('selected', 'white')])
        style.configure("Custom.Treeview.Heading", font=("Calibri", 10, "bold"), background="#111111",
                        foreground="white")

        # Create a frame to hold the treeview and scrollbars
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)


        self.tree = ttk.Treeview(self.tree_frame, columns=self.headers, show='headings', style="Custom.Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for header in self.headers:
            self.tree.heading(header, text=header)
            if header in ["Lane", "ID", "Time", "Place"]:
                self.tree.column(header, anchor='center', width=0)
            else:
                self.tree.column(header, anchor='center')

        self.update_table()

        # the table is edited by double clicking on a cell.
        self.tree.bind('<Double-1>', self.on_double_click)

        self.entry = None
        self.combobox_frame = None
        self.combobox = None

        self.button_frame = tk.Frame(self, bg="#222222")
        self.button_frame.pack(fill=tk.X, padx=10, pady=0)

        self.center_frame = tk.Frame(self.button_frame, bg="#222222")
        self.center_frame.pack(pady=10)

        self.image_canvas = tk.Canvas(self, bg = "black", highlightthickness = 0)
        self.image_canvas.pack(fill=tk.BOTH, expand = True)

        self.image_button_frame = tk.Frame(self, bg="#222222", height = 10)
        self.image_button_frame.pack(padx = 10)

        self.image_left_button = tk.Button(self.image_button_frame, image=left_icon,
                                           command=partial(self.image_borders, "vleft"), bd=0, width=70, height=35)
        self.image_left_button.bind("<Enter>", self.enter_left)
        self.image_left_button.bind("<Leave>", self.leave_left)
        self.image_left_button.pack(side=tk.LEFT, padx=10)
        self.image_out_button = tk.Button(self.image_button_frame, image=zoom_out_icon,
                                          command=partial(self.image_borders, "vout"), bd=0, width=35, height=35)
        self.image_out_button.bind("<Enter>", self.enter_out)
        self.image_out_button.bind("<Leave>", self.leave_out)
        self.image_out_button.pack(side=tk.LEFT)
        self.image_in_button = tk.Button(self.image_button_frame, image=zoom_in_icon,
                                         command=partial(self.image_borders, "vin"), bd=0, width=35, height=35)
        self.image_in_button.bind("<Enter>", self.enter_in)
        self.image_in_button.bind("<Leave>", self.leave_in)
        self.image_in_button.pack(side=tk.LEFT)
        self.image_right_button = tk.Button(self.image_button_frame, image=right_icon,
                                            command=partial(self.image_borders, "vright"), bd=0, width=70, height=35)
        self.image_right_button.bind("<Enter>", self.enter_right)
        self.image_right_button.bind("<Leave>", self.leave_right)
        self.image_right_button.pack(side=tk.LEFT, padx=10)

        # Image decoding
        image_data_bytes = base64.b64decode(import_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.import_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(import_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.import_icon_w = ImageTk.PhotoImage(image)

        self.import_button = tk.Button(self.center_frame, image=self.import_icon, bd=0, command=self.root.import_heat,
                                       bg="#222222")
        self.import_button.pack(side=tk.LEFT, padx=10)
        self.import_button.bind("<Enter>", self.enter_import)
        self.import_button.bind("<Leave>", self.leave_import)

        image_data_bytes = base64.b64decode(video_l_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.video_l_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(video_l_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.video_l_icon_w = ImageTk.PhotoImage(image)

        # to view photo-finish image on top-level while setting up results.
        self.view_pf_button = tk.Button(self.center_frame, image=self.video_l_icon, bd=0, command=self.visualise_image)
        self.view_pf_button.pack(side=tk.LEFT, padx=10)
        self.view_pf_button.bind("<Enter>", self.enter_view_pf)
        self.view_pf_button.bind("<Leave>", self.leave_view_pf)

        image_data_bytes = base64.b64decode(add_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.add_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(add_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.add_icon_w = ImageTk.PhotoImage(image)

        # to add a new row (or new athlete if you will)
        self.add_button = tk.Button(self.center_frame, image=self.add_icon, bd=0, command=self.add_row, bg="#222222")
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.add_button.bind("<Enter>", self.enter_add)
        self.add_button.bind("<Leave>", self.leave_add)

        image_data_bytes = base64.b64decode(remove_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.remove_icon = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(remove_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.remove_icon_w = ImageTk.PhotoImage(image)

        # to remove a row
        self.remove_button = tk.Button(self.center_frame, image=self.remove_icon, bd=0,
                                       command=partial(self.delete_row, 0), bg="#222222")
        self.remove_button.pack(side=tk.LEFT, padx=10)
        self.remove_button.bind("<Enter>", self.enter_remove)
        self.remove_button.bind("<Leave>", self.leave_remove)
        self.tree.bind("<Delete>", self.delete_row)

        # obvious
        self.sort_combobox = ttk.Combobox(self.center_frame, values=[x for i in self.headers for x in (
        "Sort by " + i + "\u2191", "Sort by " + i + "\u2193")], background="#222222")
        self.sort_combobox.set("Sort by...")
        self.sort_combobox.pack(side=tk.LEFT, padx=10)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.sort_table)
        self.sort_combobox.state(["readonly"])

        # to export the results as excel or text file
        self.export_button = tk.Button(self.center_frame, image=self.root.export_image_icon, bd=0,
                                       command=self.root.export_results_table, bg="#222222")
        self.export_button.pack(side=tk.LEFT, padx=10)
        self.export_button.bind("<Enter>", self.enter_export)
        self.export_button.bind("<Leave>", self.leave_export)

        # Create a vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        self.original_v_scrollbar_command = self.v_scrollbar.cget('command')
        self.no_op_command = lambda *args: None

        self.image_center = 0.5
        self.image_zoom_x = 1

    """
    those enter_sth, leave_sth functions are for changing the button image
    when the mouse is hovering over the button. the images are just a brighter
    versions of the originals.
    """
    def enter_view_pf(self,event):
        self.view_pf_button.config(image = self.video_l_icon_w)

    def leave_view_pf(self,event):
        self.view_pf_button.config(image = self.video_l_icon)


    def enter_import(self, event):
        self.import_button.config(image=self.import_icon_w)

    def leave_import(self, event):
        self.import_button.config(image=self.import_icon)

    def enter_export(self, event):
        self.export_button.config(image=self.root.export_image_icon_w)

    def leave_export(self, event):
        self.export_button.config(image=self.root.export_image_icon)

    def enter_add(self, event):
        self.add_button.config(image=self.add_icon_w)

    def leave_add(self, event):
        self.add_button.config(image=self.add_icon)

    def enter_remove(self, event):
        self.remove_button.config(image=self.remove_icon_w)

    def leave_remove(self, event):
        self.remove_button.config(image=self.remove_icon)

    def change_title(self, title):
        self.title_canvas.itemconfig(self.title, text=title)

    def on_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == 'cell':
            column = self.tree.identify_column(event.x)
            row = self.tree.identify_row(event.y)

            if self.entry:
                self.entry.destroy()
            if self.combobox:
                self.combobox.destroy()
            if self.combobox_frame:
                self.combobox_frame.destroy()

            x, y, width, height = self.tree.bbox(row, column)
            value = self.tree.item(row, 'values')[int(column[1:]) - 1]

            col_index = int(column[1:]) - 1

            self.v_scrollbar.config(command=self.no_op_command)
            if self.headers[col_index] == "Time":
                self.combobox_frame = tk.Frame(self.tree_frame, borderwidth=1, relief='solid', bg="#222222")
                self.combobox_frame.place(x=x, y=y, width=width, height=height)

                self.combobox = ttk.Combobox(self.combobox_frame, values=self.results, background="#222222")
                self.combobox.pack(fill=tk.BOTH, expand=True)
                self.combobox.set(value)
                self.combobox.focus()

                self.combobox.bind('<<ComboboxSelected>>',
                                   lambda event, col=column, r=row: self.on_combobox_selected(col, r))
                self.combobox.bind('<Return>',
                                   lambda event, col=column, r=row: self.on_combobox_selected(col, r))
            else:
                self.entry = tk.Entry(self.tree, background="#222222", foreground="white")
                self.entry.place(x=x, y=y, width=width, height=height)
                self.entry.insert(0, value)
                self.entry.focus()
                self.entry.bind('<Return>', lambda event, col=column, r=row: self.on_entry_return(col, r))
                self.entry.bind('<FocusOut>', lambda event, col=column, r=row: self.on_entry_return(col, r))

    def on_entry_return(self, column, row):
        self.v_scrollbar.config(command=self.original_v_scrollbar_command)
        new_value = self.entry.get()
        values = list(self.tree.item(row, 'values'))
        col_index = int(column[1:]) - 1
        values[col_index] = new_value
        self.tree.item(row, values=values)

        for row_data in self.data:
            if str(row_data["ID"]) == values[1]:  # Assuming ID is unique
                row_data[self.headers[col_index]] = new_value
                break

        self.entry.destroy()
        self.entry = None

    def on_combobox_selected(self, column, row):
        self.v_scrollbar.config(command=self.original_v_scrollbar_command)
        new_value = self.combobox.get()
        values = list(self.tree.item(row, 'values'))
        col_index = int(column[1:]) - 1
        values[col_index] = new_value
        self.tree.item(row, values=values)

        for row_data in self.data:
            if str(row_data["ID"]) == values[1]:  # Assuming ID is unique
                row_data[self.headers[col_index]] = new_value
                break

        self.combobox.destroy()
        self.combobox_frame.destroy()
        self.combobox = None
        self.combobox_frame = None
        self.update_places()

    def add_row(self):
        new_id = len(self.data) + 1
        new_row = {"Lane": "Type Lane", "ID": new_id, "Name": "Type Name", "Date of Birth": "Type DOB", "Affiliation": "Type Affiliation", "License": "Type License", "Time": "",
                   "Place": ""}
        self.data.append(new_row)
        self.tree.insert('', tk.END, values=[new_row.get(header, '') for header in self.headers])

    def delete_row(self,event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], 'values')
            self.tree.delete(selected_item[0])
            self.data = [row for row in self.data if str(row["ID"]) != values[1]]

    def sort_table(self, event):
        selected_header = self.sort_combobox.get()
        ascending = selected_header.endswith("\u2191")
        selected_header = selected_header.replace("Sort by ", "").rstrip("\u2191\u2193")

        if selected_header == "Time":
            self.update_places()
        else:
            self.data.sort(key=lambda x: x.get(selected_header, ''), reverse=not ascending)
            self.update_table()


    #places are updated according to times.
    def update_places(self):
        time_to_place = sorted(self.data, key=lambda x: x.get("Time", ''))
        time_to_place_dict = {row["ID"]: str(index + 1) for index, row in enumerate(time_to_place)}

        for row in self.data:
            row["Place"] = time_to_place_dict.get(row["ID"], "")
        self.update_table()

    def update_results(self, new_results):
        self.results = []
        for i in new_results:
            if i > 60:
                item = str(int(i // 60)) + ":" + str(int((i % 60) * 100) / 100)
                if item[-2] == ".":
                    item = item + "0"
            else:
                item = str(int((i) * 100) / 100)
                if item[-2] == ".":
                    item = item + "0"
            self.results.append(item)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.data:
            self.tree.insert('', tk.END, values=[row.get(header, '') for header in self.headers])


    # to get data from excel, excel data is first converted into a matrix (list of lists)
    # and here it sets the table according to that matrix.
    def set_data_from_matrix(self, matrix):
        self.data = []

        if all(len(row) == len(self.headers) for row in matrix):
            for row in matrix:
                row_data = {self.headers[i]: row[i] for i in range(len(self.headers))}
                self.data.append(row_data)
            self.update_table()
        else:
            print("Matrix row length does not match headers length")

    def visualise_image(self):

        self.image_canvas.delete("all")

        center_time = (1-self.image_center)*(self.root.image_end_time_full-self.root.image_start_time_full) + self.root.image_start_time_full

        self.image_start_time = center_time - (self.root.image_end_time_full-self.root.image_start_time_full)*0.5*0.75 ** (self.image_zoom_x-1)
        self.image_end_time = center_time + (self.root.image_end_time_full - self.root.image_start_time_full) * 0.5*0.75 ** (self.image_zoom_x-1)

        start = self.image_center - 0.5*0.75 ** (self.image_zoom_x-1)
        end = self.image_center + 0.5*0.75 ** (self.image_zoom_x-1)


        level = np.log(self.image_end_time-self.image_start_time)/np.log(10)
        level = int(level+0.5)
        tick_increments = 10**(level-2)
        label_increments = 10**(level-1)

        tick_start = self.image_start_time - self.image_start_time%tick_increments + tick_increments
        tick_end = self.image_end_time - self.image_end_time%tick_increments
        ticks = np.arange(tick_start,tick_end+10*tick_increments,tick_increments)

        label_start = self.image_start_time - self.image_start_time % label_increments + label_increments
        label_end = self.image_end_time - self.image_end_time % label_increments
        labels = np.arange(label_start, label_end + label_increments, label_increments)

        locations = self.image_canvas.winfo_width()*(1-(ticks-self.image_start_time)/(self.image_end_time-self.image_start_time))

        locations_2 = self.image_canvas.winfo_width() * (1-(labels - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))

        #print(labels)
        #print(locations_2)

        loc_points = []
        scaleY = self.image_canvas.winfo_height() - self.root.scale_height
        for i in range(len(locations)-1):
            loc_points.append(locations[i])
            loc_points.append(scaleY+5)
            loc_points.append(locations[i])
            loc_points.append(scaleY)
            loc_points.append(locations[i+1])
            loc_points.append(scaleY)

        #print("time borders:",self.image_start_time,self.image_end_time)

        #print("center:",self.image_center)
        #print("zoom:", self.image_zoom_x)

        for i in range(len(labels)):
            if label_increments >=1:
                thestr = str(int(labels[i]))
            else:
                thestr = round(labels[i]*(1/label_increments))*label_increments
                thestr = str(thestr)
                thestr = thestr.split(".")[0]+"."+thestr.split(".")[-1][:int(np.log(1/label_increments)/np.log(10))]

            self.image_canvas.create_text(locations_2[i],self.image_canvas.winfo_height()-10,text = thestr,fill="#DDDDDD")
            self.image_canvas.create_line(locations_2[i],self.image_canvas.winfo_height()-20,locations_2[i],scaleY,fill = "#DDDDDD")


        #print("borders:", start, end)
        #print(len(self.zoomed_images))

        height1, width1  = self.root.zoomed_images[0].shape

        cropped_image = cv2.resize(self.root.zoomed_images[self.root.image_zoom_x - 1][0:height1,
                        int(width1 * (1/0.75) ** (self.root.image_zoom_x - 1) * start):int(
                            width1 * (1/0.75) ** (self.root.image_zoom_x - 1) * end)],
                                   (int(width1*self.image_canvas.winfo_width()/self.root.image_canvas.winfo_width()),self.image_canvas.winfo_height()-self.root.scale_height))

        image_pil = Image.fromarray(cropped_image)

        self.image_tk = ImageTk.PhotoImage(image_pil)
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.image_canvas.create_line(loc_points, fill="#DDDDDD")

        for i in self.root.results:
            X = self.image_canvas.winfo_width() * (1 - (i - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))
            self.image_canvas.create_line(X, 0, X,self.image_canvas.winfo_height() - self.root.scale_height,
                                                       fill=self.root.hashline_color)
        return

    def image_borders(self,var = None):
        if var == "vin" and self.image_zoom_x < self.root.max_image_zoom:
            self.image_zoom_x += 1

        elif var == "vout" and self.image_zoom_x > 1:
            self.image_zoom_x -= 1

        elif var == "vleft":
            self.image_center -= (1-0.75)*0.75**(self.image_zoom_x-1)

        elif var == "vright":
            self.image_center += (1-0.75)*0.75**(self.image_zoom_x-1)

        if self.image_center < 0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 0.5 *0.75** (self.image_zoom_x-1)

        elif self.image_center > 1-0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 1- 0.5*0.75 ** (self.image_zoom_x-1)


        self.visualise_image()

    def enter_left(self, event):
        self.image_left_button.config(image=left_icon_w)

    def leave_left(self, event):
        self.image_left_button.config(image=left_icon)

    def enter_right(self, event):
        self.image_right_button.config(image=right_icon_w)

    def leave_right(self, event):
        self.image_right_button.config(image=right_icon)

    def enter_in(self, event):
        self.image_in_button.config(image=zoom_in_icon_w)

    def leave_in(self, event):
        self.image_in_button.config(image=zoom_in_icon)

    def enter_out(self, event):
        self.image_out_button.config(image=zoom_out_icon_w)

    def leave_out(self, event):
        self.image_out_button.config(image=zoom_out_icon)


"""
    def update_results(self, new_results):
        self.results = []
        for i in new_results:
            if i>60:
                item = str(int(i // 60)) + ":" + str(int((i % 60) * 100) / 100)
                if item[-2] == ".":
                    item = item+"0"
            else:
                item = str(int((i) * 100) / 100)
                if item[-2] == ".":
                    item = item + "0"
            self.results.append(item)
"""


"""
the main class.
this class creates a window with all the components of the program
a window (instance) is already created after you start running the app
for a new instance, you click on the top center icon on the window.
each window will work separately.
all the instances work as "toplevel" windows whose root window is a secretly
running window that always run as long as at least one instance is present,
and stops running after the last single window is closed.
"""
class Instance:
    def __init__(self,root):



        self.mousex = 0
        self.mousey = 0

        image_data_bytes = base64.b64decode(main_icon)
        image = Image.open(BytesIO(image_data_bytes))
        self.main_icon = ImageTk.PhotoImage(image)
        self.parent = root
        self.parent.wm_iconphoto(False, self.main_icon)
        self.root = tk.Toplevel(root)
        self.root.title("MY Photo-Finish")

        self.root.wm_iconphoto(False, self.main_icon)
        self.style = ttk.Style()

        """
        the reason for error handling is that when you try to create the second instance,
        it gives error becos style has already been created.
        """
        try:
            self.style.theme_create('custom_theme', parent='alt', settings={
                'TNotebook': {
                    'configure': {
                        'tabmargins': [0,0,0,0],
                        'background': '#222222'
                    }
                },
                'TNotebook.Tab': {
                    'configure': {
                        'padding': [0, 50],
                        'background': '#222222',
                        'foreground': '#222222',
                        'borderwidth': 0
                    },
                    'map': {
                        'background': [('selected', '#444444')],
                        'foreground': [('selected', '#222222')],
                        'expand': [('selected', [1, 1, 1, 0])]
                    }
                }
            })
        except:
            pass

        self.style.theme_use('custom_theme')
        self.root.configure(bg='black')
        self.root.config(bg='black')
        self.root.option_add('*Background', '#222222')
        self.root.option_add('*Foreground', '#FFFFFF')
        self.root.option_add('*Button.Background', '#222222')
        #self.root.overrideredirect(True)
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.out = None
        self.start_time = 0
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.video_label = tk.Label(root)
        #self.video_label.pack()

        self.font = "courier"
        self.hashline_color = "#FF0000"

        self.audio_data, self.audiosamplerate = None, None
        self.duration = None

        self.top_frame = tk.Frame(self.root, height = 1)
        self.top_frame.pack(fill = "both", expand = True)

        image_data_bytes = base64.b64decode(add_instance_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.add_instance_icon = ImageTk.PhotoImage(image)
        image_data_bytes = base64.b64decode(add_instance_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.add_instance_icon_w = ImageTk.PhotoImage(image)


        self.new_instance_button = tk.Button(self.top_frame, image = self.add_instance_icon, command = self.new_instance, bd = 0)
        self.new_instance_button.pack(fill='x')
        self.new_instance_button.bind("<Enter>",self.enter_new_instance)
        self.new_instance_button.bind("<Leave>", self.leave_new_instance)


        #tabs for the three main frames of the software
        self.notebook = ttk.Notebook(self.top_frame, style='lefttab.TNotebook')
        self.notebook.pack(expand=True, fill='both')

        image_data_bytes = base64.b64decode(video_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.video_bt = ImageTk.PhotoImage(image)

        self.audio_frame = tk.Frame(self.notebook)
        self.image_frame = tk.Frame(self.notebook)
        self.results_frame = tk.Frame(self.notebook)
        self.style.configure('lefttab.TNotebook', font="TkDefaultFont", tabposition='wn')
        self.notebook.add(self.audio_frame, image = gun_icon)
        self.notebook.add(self.image_frame, image= self.video_bt)
        self.notebook.add(self.results_frame, image =results_icon)


        #the bottom frame to display informations, progress bars etc.
        self.global_frame = tk.Frame(self.root, height=50, highlightthickness=0)
        self.global_frame.pack(side=tk.BOTTOM,fill='x')

        self.status = tk.Canvas(self.global_frame, height=40, bg="black", highlightthickness=0)
        self.status.pack(fill='x', expand = True)

        self.status_text =  None
        self.audio_canvas = tk.Canvas(self.audio_frame, bg="#000000", highlightthickness=0)
        self.audio_canvas.pack(fill='both', expand=True)


        self.image_options = tk.Canvas(self.image_frame, width=350, height=745, bg="#222222",
                                       highlightthickness=0)
        self.image_options.pack(side=tk.LEFT)

        self.image_canvas2 = tk.Canvas(self.image_frame, bg="black", highlightthickness=0)
        self.image_canvas2.pack(fill='both', expand=True)
        self.image_canvas2.bind("<Motion>", self.display_zoom)
        self.image_canvas2.bind("<Leave>", self.leave_image_canvas2)

        self.image_canvas = tk.Canvas(self.image_frame, bg="black", highlightthickness=0)
        self.image_canvas.pack(fill='both', expand= True)
        self.image_canvas.bind("<Leave>", self.leave_image_canvas)


        self.audio_button_frame = tk.Frame(self.audio_frame, highlightthickness=0)
        self.audio_button_frame.pack(anchor=tk.S)

        self.image_button_frame = tk.Frame(self.image_frame, highlightthickness=0)
        self.image_button_frame.pack(anchor=tk.S)

        self.image_canvas.config(cursor="none")


        image_data_bytes = base64.b64decode(import_video_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.import_video_icon = ImageTk.PhotoImage(image)
        image_data_bytes = base64.b64decode(import_video_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.import_video_icon_w = ImageTk.PhotoImage(image)


        self.import_video_button = tk.Button(self.audio_button_frame, image = self.import_video_icon, bd = 0, command = self.analyze_audio)
        self.import_video_button.pack(side=tk.LEFT)
        self.import_video_button.bind("<Enter>",self.enter_video_import)
        self.import_video_button.bind("<Leave>", self.leave_video_import)

        image_data_bytes = base64.b64decode(play_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.play_bt = ImageTk.PhotoImage(image)
        image_data_bytes = base64.b64decode(play_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.play_bt_w = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(stop_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.stop_bt = ImageTk.PhotoImage(image)
        image_data_bytes = base64.b64decode(stop_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.stop_bt_w = ImageTk.PhotoImage(image)

        image_data_bytes = base64.b64decode(pause_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.pause_bt = ImageTk.PhotoImage(image)
        image_data_bytes = base64.b64decode(pause_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.pause_bt_w = ImageTk.PhotoImage(image)

        self.play_button = tk.Button(self.audio_button_frame, image = self.play_bt, command = self.play, bd = 0)
        self.play_button.pack(side=tk.LEFT)
        self.play_button.bind("<Enter>", self.enter_play)
        self.play_button.bind("<Leave>", self.leave_play)
        self.stop_button = tk.Button(self.audio_button_frame, image = self.stop_bt, command=self.stop, bd = 0)
        self.stop_button.pack(side=tk.LEFT)
        self.play_button.config(state = "disabled")
        self.stop_button.bind("<Enter>", self.enter_stop)
        self.stop_button.bind("<Leave>", self.leave_stop)

        self.audio_entry_frame = tk.Frame(self.audio_frame, highlightthickness= 0)
        self.audio_entry_frame.pack(anchor = tk.S)


        self.gun_mic_var = 100
        self.gun_start_var = 5
        self.sound_var = 340
        self.wind_var = 0
        self.time_var = 0

        def enable_apply(event):
            self.apply_button.config(state="normal")

        tk.Label(self.audio_entry_frame, text="Start signal - microphone distance (m):").pack(side = tk.LEFT)
        self.gun_mic_entry = tk.Entry(self.audio_entry_frame, width=10)
        self.gun_mic_entry.pack(side = tk.LEFT)
        self.gun_mic_entry.bind("<KeyRelease>", enable_apply)
        """
        self.sound_options.create_image(330, 85, anchor=tk.E, image=mic_icon)
        self.sound_options.create_image(20, 85, anchor=tk.W, image=gun_icon)
        self.sound_options.create_line(220, 85, 300, 85, fill="#666666")
        self.sound_options.create_line(50, 85, 130, 85, fill="#666666")
        self.sound_options.create_text(175, 85, text="?", fill="#DDDDDD")
        """
        self.gun_mic_entry.insert(0, str(self.gun_mic_var))

        tk.Label(self.audio_entry_frame, text="   Race start - start signal distance (m):").pack(side = tk.LEFT)
        self.gun_start_entry = tk.Entry(self.audio_entry_frame, width=10)
        self.gun_start_entry.pack(side = tk.LEFT)
        self.gun_start_entry.bind("<KeyRelease>", enable_apply)
        """
        self.sound_options.create_image(330, 175, anchor=tk.E, image=gun_icon)
        self.sound_options.create_image(20, 175, anchor=tk.W, image=start_icon)
        self.sound_options.create_line(220, 175, 300, 175, fill="#666666")
        self.sound_options.create_line(50, 175, 130, 175, fill="#666666")
        self.sound_options.create_text(175, 175, text="?", fill="#DDDDDD")
        """
        self.gun_start_entry.insert(0, str(self.gun_start_var))

        tk.Label(self.audio_entry_frame, text="   Speed of sound (m/s):").pack(side = tk.LEFT)
        self.sound_entry = tk.Entry(self.audio_entry_frame, width=10)
        self.sound_entry.pack(side = tk.LEFT)
        #self.sound_options.create_image(330, 250, anchor=tk.E, image=sound_icon)
        self.sound_entry.insert(0, str(self.sound_var))
        self.sound_entry.bind("<KeyRelease>", enable_apply)

        tk.Label(self.audio_entry_frame, text="   Wind speed (m/s):").pack(side = tk.LEFT)
        self.wind_entry = tk.Entry(self.audio_entry_frame, width=10)
        self.wind_entry.pack(side = tk.LEFT)
        #self.sound_options.create_image(330, 320, anchor=tk.E, image=wind_icon)
        self.wind_entry.insert(0, str(self.wind_var))
        self.wind_entry.bind("<KeyRelease>", enable_apply)

        tk.Label(self.audio_entry_frame, text="   Additional time offset (s):").pack(side = tk.LEFT)
        self.time_entry = tk.Entry(self.audio_entry_frame, width=10)
        self.time_entry.pack(side = tk.LEFT)
        self.time_entry.insert(0, str(self.time_var))
        self.time_entry.bind("<KeyRelease>", enable_apply)


        def apply():
            self.gun_mic_var = float(self.gun_mic_entry.get())
            self.gun_start_var = float(self.gun_start_entry.get())
            self.sound_var = float(self.sound_entry.get())
            self.wind_var = float(self.wind_entry.get())
            self.time_var = float(self.time_entry.get())
            self.apply_button.config(state="disabled")
            return

        image_data_bytes = base64.b64decode(apply_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.apply_icon = ImageTk.PhotoImage(image)

        self.apply_button = tk.Button(self.audio_entry_frame, image = self.apply_icon, bd = 0, command = apply)
        self.apply_button.pack(side = tk.LEFT, padx=10)
        self.apply_button.config(state = "disabled")


        tk.Label(self.image_button_frame, text= "Start (mm:ss) =").pack(side=tk.LEFT)
        self.image_start_entry = tk.Entry(self.image_button_frame, width = 10)
        self.image_start_entry.pack(side=tk.LEFT, padx=10)

        tk.Label(self.image_button_frame, text="   End (mm:ss) =").pack(side=tk.LEFT)
        self.image_end_entry = tk.Entry(self.image_button_frame, width=10)
        self.image_end_entry.pack(side=tk.LEFT, padx=10)

        self.fps_inc_combo = ttk.Combobox(self.image_button_frame, values = ["Do not increase FPS",
                                                                             "Increase FPS by x2",
                                                                             "Increase FPS by x3",
                                                                             "Increase FPS by x4",
                                                                             "Increase FPS by x5",
                                                                             "Increase FPS by x6"])
        self.style.configure("TCombobox",  fieldbackground="#444444", background="#222222", foreground = "#DDDDDD")
        self.fps_inc_combo.configure(style="TCombobox")
        self.fps_inc_combo.config(state = ["readonly"])
        self.fps_inc_combo.set("Do not increase FPS")
        self.fps_inc_combo.pack(side = tk.LEFT)

        image_data_bytes = base64.b64decode(generate_image_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.generate_image_icon = ImageTk.PhotoImage(image)

        self.image_button = tk.Button(self.image_button_frame, image = self.generate_image_icon, bd = 0, command=self.generate_new_image)
        self.image_button.pack(side=tk.LEFT, padx=10)
        self.image_button.config(state= "disabled")


        self.image_undo_button = tk.Button(self.image_button_frame, image=undo_icon, command=self.undo, bd=0, width=35,
                                           height=35)
        self.image_undo_button.bind("<Enter>",self.enter_undo)
        self.image_undo_button.bind("<Leave>", self.leave_undo)
        self.image_undo_button.pack(side=tk.LEFT)

        self.image_redo_button = tk.Button(self.image_button_frame, image=redo_icon, command=self.redo, bd=0, width=35,
                                           height=35)
        self.image_redo_button.bind("<Enter>",self.enter_redo)
        self.image_redo_button.bind("<Leave>", self.leave_redo)
        self.image_redo_button.pack(side=tk.LEFT)

        self.root.bind('<Control-z>', self.undo)
        self.root.bind('<Control-Z>', self.redo)

        self.image_left_button = tk.Button(self.image_button_frame, image=left_icon,
                                           command=partial(self.image_borders, "vleft"), bd=0, width=70, height=35)
        self.image_left_button.bind("<Enter>",self.enter_left)
        self.image_left_button.bind("<Leave>", self.leave_left)
        self.image_left_button.pack(side=tk.LEFT, padx=10)
        self.image_out_button = tk.Button(self.image_button_frame, image=zoom_out_icon,
                                          command=partial(self.image_borders, "vout"), bd=0, width=35, height=35)
        self.image_out_button.bind("<Enter>",self.enter_out)
        self.image_out_button.bind("<Leave>", self.leave_out)
        self.image_out_button.pack(side=tk.LEFT)
        self.image_in_button = tk.Button(self.image_button_frame, image=zoom_in_icon,
                                         command=partial(self.image_borders, "vin"), bd=0, width=35, height=35)
        self.image_in_button.bind("<Enter>",self.enter_in)
        self.image_in_button.bind("<Leave>", self.leave_in)
        self.image_in_button.pack(side=tk.LEFT)
        self.image_right_button = tk.Button(self.image_button_frame, image=right_icon,
                                            command=partial(self.image_borders, "vright"), bd=0, width=70, height=35)
        self.image_right_button.bind("<Enter>",self.enter_right)
        self.image_right_button.bind("<Leave>", self.leave_right)
        self.image_right_button.pack(side=tk.LEFT, padx=10)

        image_data_bytes = base64.b64decode(export_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.export_image_icon = ImageTk.PhotoImage(image)


        image_data_bytes = base64.b64decode(export_bt_w)
        image = Image.open(BytesIO(image_data_bytes))
        self.export_image_icon_w = ImageTk.PhotoImage(image)

        self.export_image_button = tk.Button(self.image_button_frame, image=self.export_image_icon,
                                            command=self.take_canvas_screenshot, bd=0)
        self.export_image_button.bind("<Enter>",self.enter_export_image)
        self.export_image_button.bind("<Leave>", self.leave_export_image)
        self.export_image_button.pack(side=tk.LEFT, padx=15)


        tk.Label(self.image_options, text="Image Alignment").place(x = 175, y=10, anchor="center")

        tk.Label(self.image_options, text="Frame width (pixels):").place(x = 5 +20, y = 10+20, anchor = "w")
        self.frame_width_entry = tk.Entry(self.image_options, width=10)
        self.frame_width_entry.place(x = 345 -20, y = 10+20, anchor = "e")
        self.frame_width_entry.insert(0,"50")

        tk.Label(self.image_options, text="Image center offset (pixels):").place(x = 5 +20, y = 35+20, anchor = "w")
        self.image_center_entry = tk.Entry(self.image_options, width=10)
        self.image_center_entry.place(x = 345-20, y = 35+20, anchor = "e")
        self.image_center_entry.insert(0,"0")

        tk.Label(self.image_options, text="Height padding on top (pixels):").place(x = 5 +20, y = 60+20, anchor = "w")
        self.top_y_offset_entry = tk.Entry(self.image_options, width=10)
        self.top_y_offset_entry.place(x = 345-20, y = 60+20, anchor = "e")
        self.top_y_offset_entry.insert(0, "0")

        tk.Label(self.image_options, text="Height padding on bottom (pixels):").place(x = 5 +20, y = 85+20, anchor = "w")
        self.bottom_y_offset_entry = tk.Entry(self.image_options, width=10)
        self.bottom_y_offset_entry.place(x = 345-20, y = 85+20, anchor = "e")
        self.bottom_y_offset_entry.insert(0, "0")

        self.direction = tk.IntVar()

        tk.Label(self.image_options, text="Race direction:").place(x=5 + 20, y=110 + 20, anchor="w")
        self.running_dir_1 = tk.Radiobutton(self.image_options, text="Left to Right", variable=self.direction, value=0)
        self.running_dir_2 = tk.Radiobutton(self.image_options, text="Right to Left", variable=self.direction, value=1)
        self.running_dir_1.place(x=210, y=110 + 20, anchor = "e")
        self.running_dir_2.place(x=320, y=110 + 20,anchor = "e")
        self.direction.set(0)



        self.preview_canvas_width = 300
        self.preview_canvas_height = 500

        self.preview_canvas = tk.Canvas(self.image_options, width = 300, height = 500, bg = "black", highlightthickness=0)
        self.preview_canvas.place(x = 175, y = 150+20, anchor = "n")

        image_data_bytes = base64.b64decode(preview_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.preview_icon = ImageTk.PhotoImage(image)

        self.preview_button = tk.Button(self.image_options,image = self.preview_icon, bd = 0, command = self.preview_frame)
        self.preview_button.place(x = 70, y = 660+20, anchor = "nw")
        self.preview_button.config(state = "disabled")


        image_data_bytes = base64.b64decode(update_image_bt)
        image = Image.open(BytesIO(image_data_bytes))
        self.update_image_icon = ImageTk.PhotoImage(image)

        self.image_update_button = tk.Button(self.image_options, image = self.update_image_icon, bd = 0,  command=self.update_image)
        self.image_update_button.place(x=350-70, y=660 + 20, anchor="ne")
        self.image_update_button.config(state="disabled")


        points = [250,10,345,10,345,725,5,725,5,10,100,10]
        self.image_options.create_line(points, fill = "#444444")

        self.audio_canvas.bind("<Button-1>", self.on_click_audio)
        self.audio_canvas.bind("<MouseWheel>", self.handle_scroll_audio)
        self.audio_canvas.bind("<Motion>", self.on_mouse_motion_audio)

        self.image_middle = 0.5

        self.scale_height = 30

        self.cursorline = self.audio_canvas.create_line(self.audio_canvas.winfo_width() / 2, 0, self.audio_canvas.winfo_width() / 2,
                                                        self.audio_canvas.winfo_height(),
                                                        fill="white")

        self.start_cursor = self.audio_canvas.create_line(self.mousex, 0, self.mousex, self.audio_canvas.winfo_height(),
                                                          fill="red")

        self.red_gun = self.audio_canvas.create_image(99999,
                                                      self.audio_canvas.winfo_height() - self.scale_height - 30,
                                                      anchor=tk.S,image = red_gun_icon)
        self.red_gun2 = self.audio_canvas.create_image(99999,
                                                       self.scale_height + 30, anchor=tk.N,
                                                       image=red_gun_icon)

        #self.video_label = tk.Label(self.image_frame)
        #self.video_label.pack()

        self.audio_canvas.create_line(0, int(self.audio_canvas.winfo_height() / 2),
                                      int(self.audio_canvas.winfo_width()),
                                      int(self.audio_canvas.winfo_height() / 2), fill="white")

        self.audio_zoom_x = 1
        self.audio_zoom_y = 1



        self.audiostartrel = 0
        self.audioendrel = 1

        self.image_zoom_x = 1
        self.image_center = 0.5
        self.imagestartrel = 0
        self.imageendrel = 1

        self.playback_cursor = None

        self.line_thickness = 50
        self.image_offset_x = 0
        self.image_offset_upper = 0
        self.image_offset_lower = 0

        self.playing = False

        self.timeline_image = None
        self.image = None
        self.image_resized = None
        self.zoomed_images = []

        self.image_start_time_full = 0
        self.image_end_time_full = 0

        self.image_start_time = 0
        self.image_end_time = 0

        self.max_image_zoom = 10

        self.start_entry = None
        self.end_entry = None



        self.image_canvas.bind("<Button-1>", self.on_click_image)
        self.image_canvas.bind("<MouseWheel>", self.handle_scroll_image)
        self.image_canvas.bind("<Motion>", self.on_mouse_motion_image)
        self.image_canvas.bind("<Button-3>", self.display_frames)

        self.hash_line = self.image_canvas.create_line(self.image_canvas.winfo_width() // 2, 0,
                                                       self.image_canvas.winfo_width() // 2,
                                                       self.image_canvas.winfo_height(),
                                                       fill=self.hashline_color)

        self.hash_line_hor = self.image_canvas.create_line(self.image_canvas.winfo_width() // 2 + 5,
                                                           self.image_canvas.winfo_height() // 2,
                                                           self.image_canvas.winfo_width() // 2 + 5,
                                                           self.image_canvas.winfo_height() // 2,
                                                           fill=self.hashline_color)

        self.results = []
        self.deleted_results = []
        self.results_sorted = None

        self.status_text = None


        self.progress_bar_bg = None
        self.progress_bar = None

        self.status_text_left = None

        self.root.configure(bg="#555555")

        #self.results_table()
        #self.create_edit_controls()
        self.table = EditableTable(self.results_frame,self)

        self.current_time_audio = 0

        self.default_athlete =  {"Lane":"nan","ID":"nan","Name":"nan","Date of Birth": "nan", "Affiliation":"nan","License":"nan","Time":"nan","Place": "nan"}

        self.background_change = False

        self.frames_ready = False
        self.timeline_ready = False
        self.framess = None

        self.view_pf_var = False
        self.update_image_var = False
        self.excel_import = False

        self.frame_interpolation = False
        self.interpolation_factor = 1

        polygon_points = [self.status.winfo_width() - 600, 5, self.status.winfo_width() - 600 + 0 * 600, 5,
                          self.status.winfo_width() - 600 + 0 * 600, self.status.winfo_height() - 5,
                          self.status.winfo_width() - 600, self.status.winfo_height() - 5]
        self.progress_bar = self.status.create_polygon(polygon_points, fill="#555555")
        self.status.tag_lower(self.progress_bar)

        self.paused_time = 0
    def enter_play(self,event):
        if self.playing == True:
            self.play_button.config(image= self.pause_bt_w)
        else:
            self.play_button.config(image=self.play_bt_w)

    def leave_play(self,event):
        if self.playing == True:
            self.play_button.config(image= self.pause_bt)
        else:
            self.play_button.config(image=self.play_bt)
    def enter_stop(self, event):
        self.stop_button.config(image=self.stop_bt_w)

    def leave_stop(self, event):
        self.stop_button.config(image=self.stop_bt)

    def enter_new_instance(self,event):
        self.new_instance_button.config(image = self.add_instance_icon_w)

    def leave_new_instance(self,event):
        self.new_instance_button.config(image = self.add_instance_icon)

    def enter_export_image(self,event):
        self.export_image_button.config(image = self.export_image_icon_w)

    def leave_export_image(self,event):
        self.export_image_button.config(image = self.export_image_icon)

    def enter_video_import(self,event):
        self.import_video_button.config(image = self.import_video_icon_w)

    def leave_video_import(self,event):
        self.import_video_button.config(image = self.import_video_icon)

    def enter_undo(self,event):
        self.image_undo_button.config(image = undo_icon_w)

    def leave_undo(self, event):
        self.image_undo_button.config(image=undo_icon)

    def enter_redo(self, event):
        self.image_redo_button.config(image=redo_icon_w)

    def leave_redo(self, event):
        self.image_redo_button.config(image=redo_icon)

    def enter_left(self, event):
        self.image_left_button.config(image=left_icon_w)

    def leave_left(self, event):
        self.image_left_button.config(image=left_icon)

    def enter_right(self, event):
        self.image_right_button.config(image=right_icon_w)

    def leave_right(self, event):
        self.image_right_button.config(image=right_icon)

    def enter_in(self, event):
        self.image_in_button.config(image=zoom_in_icon_w)

    def leave_in(self, event):
        self.image_in_button.config(image=zoom_in_icon)

    def enter_out(self, event):
        self.image_out_button.config(image=zoom_out_icon_w)

    def leave_out(self, event):
        self.image_out_button.config(image=zoom_out_icon)


    """
    i said that all instances are connected to a secret root and that main root
    is closed after the last single frame is closed.
    this condition is checked via the global var total_instances
    """
    def new_instance(self):
        global total_instances
        total_instances += 1
        video_recorder = Instance(root)
        video_recorder.root.mainloop()

    def on_closing(self):
        global total_instances
        total_instances -= 1
        if total_instances == 0:
            global root
            root.destroy()
        else:
            self.root.destroy()


    """
    after a video is selected, 
    its audio is imported first.
    """
    def analyze_audio(self):
        #self.root.iconbitmap("images/cross.ico")
        try:
            video_file = filedialog.askopenfilename(title="Import Video")

            self.video_file = video_file

            #print(self.video_file)

            if self.status_text_left:
                self.status.itemconfig(self.status_text_left, text="Extracting audio...")

            else:
                self.status_text_left = self.status.create_text(7, self.status.winfo_height() // 2,
                                                                text="Extracting audio...", font=(self.font, 15),
                                                                anchor="w", fill="#00FF00")

            #self.cap_timeline = cv2.VideoCapture(self.video_file)
            #fps = self.cap_timeline.get(cv2.CAP_PROP_FPS)
            #frame_count = int(self.cap_timeline.get(cv2.CAP_PROP_FRAME_COUNT))
            #duration = frame_count / fps
            clip = VideoFileClip(self.video_file)
            self.audio = clip.audio

            self.audio.write_audiofile("temporary.wav",logger=DummyLogger())

            self.audio_data, self.audiosamplerate = sf.read("temporary.wav")

            self.duration = len(self.audio_data[:, 1]) / self.audiosamplerate
            if self.status_text:
                self.status.itemconfig(self.status_text, text = "Audio extracted.")
            else:
                self.status_text = self.status.create_text(self.status.winfo_width()-7, self.status.winfo_height() // 2,
                                                       text="Audio extracted.", anchor="e", fill="#00FF00", font = self.font)
            self.visualise_audio(self.audio_data, self.audiosamplerate, 0, 1)

            #self.create_image()

            self.status.itemconfig(self.status_text_left,
                                   text="Title: "+str(self.video_file).split("/")[-1].split(".")[0])
            self.root.title(str(self.video_file).split("/")[-1].split(".")[0]+" - MY Photo-Finish")
            if self.excel_import == False:
                self.table.change_title("Title: "+str(self.video_file).split("/")[-1].split(".")[0]+", Wind: "+str(self.wind_var)+" m/s")

            self.play_button.config(state = "normal")
            self.image_button.config(state="normal")
            self.current_time_audio = 0
            self.paused_time = 0
            self.start_time = 0

        except Exception as e:
            self.status.itemconfig(self.status_text_left, text= f"error:{e}")
            error_traceback = traceback.format_exc()

            # Write the error message and traceback to a file
            with open('error_log.txt', 'w') as error_file:
                error_file.write(error_traceback)

    def start_sample(self):
        return

    # play the audio of the video

    def play(self):
        #this function also pauses the audio if evoked while playing.
        if self.playing == True:
            self.play_button.config(image= self.play_bt_w)
            sd.stop()
            self.playing = False
            self.paused_time = self.current_time_audio
        else:
            self.play_button.config(image= self.pause_bt_w)
            self.audio_canvas.delete(self.playback_cursor)
            self.playback_deleted = True
            print(self.current_time_audio)
            def play_audio():
                sd.play(self.audio_data[:,1][int(len(self.audio_data[:,1])*self.current_time_audio/self.duration):], samplerate=self.audiosamplerate)
                sd.wait()

            self.playing = True
            audio_thread = threading.Thread(target=play_audio)
            audio_thread.start()


        #the cursor progresses as the audio plays
        def playback_cursor():
            self.playback_start = time.time()

            while self.playing == True:

                #frama rate of the cursor is 30 fps
                time.sleep(1/30)

                #time_elapsed = time.time()- self.playback_start
                #self.audio_canvas.delete(self.playback_cursor)
                #calculates how much seconds has passed after the playback_cursor function is evoked.
                self.current_time_audio = (time.time() - self.playback_start) + self.paused_time

                #sets the position of the cursor on the canvas according to the time passed.
                self.playback_cursor_position = self.audio_canvas.winfo_width() * (
                            self.current_time_audio / self.duration - self.audiostartrel) / (self.audioendrel - self.audiostartrel)
                #print(self.playback_cursor_position)

                #the first cursor is created when the play is evoked, the next cursors are just shifted versions.
                if self.playback_deleted == True:
                    self.playback_cursor = self.audio_canvas.create_line(self.playback_cursor_position, 0,
                                                                         self.playback_cursor_position,
                                                                         self.audio_canvas.winfo_height(),
                                                                         fill="green")
                    self.playback_deleted = False
                else:
                    self.audio_canvas.coords(self.playback_cursor, self.playback_cursor_position, 0,
                                                                self.playback_cursor_position,
                                                                self.audio_canvas.winfo_height())



                #formatting the times. i know there are much neater ways...
                current_time_str = str(int(self.current_time_audio // 60)) + ":" + str(
                    (int((self.current_time_audio % 60) * 10 + 0.5)) / 10)

                gun_shot = str(int(self.start_time // 60)) + ":" + str(
                    (int((self.start_time % 60) * 1000 + 0.5)) / 1000)

                time_delta = str(int((self.current_time_audio - self.start_time) // 60)) + ":" + str(
                    (int(((self.current_time_audio - self.start_time) % 60) * 10 + 0.5)) / 10)

                self.status.itemconfig(self.status_text_left,text = "Video time: "+current_time_str+"    Time elapsed: "+time_delta)

        cursor_thread = threading.Thread(target=playback_cursor)
        cursor_thread.start()


    def stop(self):
        self.playing = False
        sd.stop()
        time.sleep(1 / 30)
        self.current_time_audio = self.start_time
        self.audio_canvas.delete(self.playback_cursor)
        self.playback_deleted = True
        self.play_button.config(image= self.play_bt)
        self.status.itemconfig(self.status_text_left,
                               text="Gun shot at: " + self.gun_shot)
        self.paused_time = self.start_time


    #clicking on the audio will determine a start time for the race.
    def on_click_audio(self,event):
        if event == 0:
            print("event 0")
        elif event == 1:
            print("event")

        elif self.playing == False:
            clicked = self.mousex_rel*len(self.audio_data[:,1])/self.audiosamplerate
            print(clicked)
            self.audio_canvas.delete(self.start_cursor)
            self.audio_canvas.delete(self.red_gun)
            self.audio_canvas.delete(self.red_gun2)
            self.start_cursor = self.audio_canvas.create_line(self.mousex, 0, self.mousex, self.audio_canvas.winfo_height(),
                                                    fill="red")

            self.red_gun = self.audio_canvas.create_image(self.mousex, self.audio_canvas.winfo_height()-self.scale_height-30, anchor = tk.S, image = red_gun_icon)
            self.red_gun2 = self.audio_canvas.create_image(self.mousex,
                                                        self.scale_height + 30, anchor = tk.N,
                                                          image=red_gun_icon)

            self.start_cursor_x = self.mousex_rel
            self.start_time = clicked
            self.start_cursor_position = self.audio_canvas.winfo_width()*(self.start_time/self.duration - self.audiostartrel)/(self.audioendrel-self.audiostartrel)
            self.current_time_audio = self.start_time
            self.paused_time = self.start_time

        self.gun_shot = str(int(self.start_time // 60)) + ":" + str(
            (int((self.start_time % 60) * 1000 + 0.5)) / 1000)
        self.status.itemconfig(self.status_text_left,
                               text="Gun shot at: " + self.gun_shot)

        #print(int(self.start_time*self.audiosamplerate),int(self.start_time*self.audiosamplerate) + int(self.audiosamplerate/2))
        #chunk = self.audio_data[:,1][int(self.start_time*self.audiosamplerate):int(self.start_time*self.audiosamplerate) + int(self.audiosamplerate*0.002)]
        #fourier = abs(np.fft.fft(chunk))[:len(chunk)]
        #frequencies = np.linspace(0,int(self.audiosamplerate/2), len(chunk))
        #from matplotlib import pyplot as plt
        #plt.plot(frequencies, fourier)
        #plt.show()
        return

    #moving the mouse will move the cursor.
    def on_mouse_motion_audio(self, event):
        try:
            self.mousex, self.mousey = event.x, event.y
            self.mousex_oncanvas = self.mousex/self.audio_canvas.winfo_width()
            self.mousex_rel = self.image_middle + (self.mousex_oncanvas-0.5)*2**(1-self.audio_zoom_x)
            #print(self.mousex_rel)

            self.audio_canvas.delete(self.cursorline)
            self.cursorline = self.audio_canvas.create_line(self.mousex, 0, self.mousex, self.audio_canvas.winfo_height(),
                                                        fill="white")
            clicked = self.mousex_rel * len(self.audio_data[:, 1]) / self.audiosamplerate
            current_time_str = str(int(clicked//60)) + ":" +str((int((clicked%60)*1000+0.5))/1000)

            self.status.itemconfig(self.status_text, text = current_time_str)
        except:
            pass

    # visualises the audio signal
    # evoked after the audio is imported, and each time zoom level or position is changed via scroll
    def visualise_audio(self,audio, sr, start, end):

        data = audio[:,1][int(start*len(audio[:,1])):int(end*len(audio[:,1]))]
        self.audio_canvas.delete("all",)
        self.playback_deleted = True
        #print(int(start*len(audio[:,1])),int(end*len(audio[:,1])),"::",int(start*len(audio[:,1]))/len(audio[:,1]),int(end*len(audio[:,1]))/len(audio[:,1]))


        #the below part is to determine an amout of increment (powers of 10 in seconds) on the scale
        duration = len(audio[:,1])/sr
        level = np.round(np.log(duration)/np.log(10))
        increments = 10**level
        while True:
            if increments*15 < duration*(end-start):
                break
            else:
                increments /= 10

        #print(duration, start, end, increments)
        starting = duration*start - (duration*start)%increments + increments
        starting = int(starting/increments)
        starting *= increments

        ending =  duration*end - (duration*end)%increments
        #print("operation:", starting,ending, increments)
        thearray = np.arange(starting, ending+10*increments, increments)
        locations = self.audio_canvas.winfo_width()*(thearray/duration - start)/(end-start)


        loc_points = []
        loc_points2 = []
        grids = []
        scaleY = self.audio_canvas.winfo_height()-50
        #locations for the ticks of the scale on the canvas.
        for i in range(len(locations)-1):
            loc_points.append(locations[i])
            loc_points.append(scaleY)
            loc_points.append(locations[i])
            loc_points.append(scaleY+20)
            loc_points.append(locations[i+1])
            loc_points.append(scaleY+20)

            loc_points2.append(locations[i])
            loc_points2.append(50)
            loc_points2.append(locations[i])
            loc_points2.append(30)
            loc_points2.append(locations[i+1])
            loc_points2.append(30)


            grids.append(locations[i])
            grids.append(0)
            grids.append(locations[i])
            grids.append(scaleY + 20)
            grids.append(locations[i + 1])
            grids.append(scaleY + 20)


            if abs(thearray[i]%(increments*10)) < increments:
                thestr = str(int(thearray[i] / increments) * increments)

                if thearray[i] > 60:
                    #print(thearray[i])
                    seconds = thearray[i]%60
                    minutes = thearray[i] // 60
                    seconds = str(int(seconds / increments) * increments)
                    thestr = str(int(minutes))+":"+seconds
                    #print(thestr)
                if "." in thestr:
                    thestr = thestr+"00000000"
                    decimal = thestr.find(".")
                    thestr = thestr[:decimal+int(1-np.log(increments)/np.log(10))]

                if thestr[-1] == ".":
                    thestr = thestr+"00"

                elif increments > 0.005 and increments < 0.05:
                    thestr = thestr+"0"


                self.audio_canvas.create_text(locations[i],scaleY+40, text = thestr, fill = "white")
                self.audio_canvas.create_line(locations[i],scaleY-20,locations[i],scaleY+20, fill="white")

                self.audio_canvas.create_text(locations[i], 10, text=thestr, fill="white")
                self.audio_canvas.create_line(locations[i], 70, locations[i], 30, fill="white")

        grids = self.audio_canvas.create_line(grids, fill="#333333")
        zero_line = self.audio_canvas.create_line(0, int(self.audio_canvas.winfo_height() / 2),
                                      int(self.audio_canvas.winfo_width()),
                                      int(self.audio_canvas.winfo_height() / 2), fill="#333333")
        self.audio_canvas.tag_lower(zero_line)
        self.audio_canvas.tag_lower(grids)
        self.audio_canvas.create_line(loc_points, fill="white")
        self.audio_canvas.create_line(loc_points2, fill="white")

        points = []
        ratio = (1/10)*len(data)/self.audio_canvas.winfo_width()+1
        data = data[::int(ratio)]
        fulldatalen = len(audio[:, 1][::int(ratio)])

        for i in range(len(data)):
            X = self.audio_canvas.winfo_width() * (i / (fulldatalen * (end - start)))
            Y = 0.5 * self.audio_canvas.winfo_height() * (1 - data[i] * 2 ** (1 - self.audio_zoom_y))

            points.append(X)
            points.append(Y)
        self.audio_canvas.create_line(points, fill="white")
        #print("array:",thearray)
        #print("locations",locations)
        #print(duration, start*duration, duration*end)


    #scrolling zooms in the audio signal in x axis.
    #if the mouse is not on the center, the signal is shifted towards the opposite side.
    # to zoom in towards left: keep mouse on the left side etc.
    def handle_scroll_audio(self,event,transfer = 0):
        delta = event.delta
        sigma = (delta / abs(delta)) # delta>1 1, delta<1 -1
        beta = (1-sigma)/2 # delta>1 0, delta<1 1
        self.image_middle = 2*(beta)*self.image_middle + sigma*self.mousex_rel

        self.audio_zoom_x += delta / abs(delta)
        if self.audio_zoom_x < 1:
            self.audio_zoom_x = 1

        start = self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x)
        end = self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x)

        if  start < 0:
            self.image_middle -= self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x)
        elif  end > 1:
            self.image_middle -= self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x)-1

        self.audiostartrel = self.image_middle - 0.5 * 2 ** (1 - self.audio_zoom_x)
        self.audioendrel = self.image_middle + 0.5 * 2 ** (1 - self.audio_zoom_x)

        start = self.audiostartrel
        end = self.audioendrel

        self.visualise_audio(self.audio_data, self.audiosamplerate, start, end)

        self.audio_canvas.delete(self.start_cursor)

        self.start_cursor_position = self.audio_canvas.winfo_width()*(self.start_time/self.duration - self.audiostartrel)/(self.audioendrel-self.audiostartrel)
        self.start_cursor = self.audio_canvas.create_line(self.start_cursor_position, 0, self.start_cursor_position, self.audio_canvas.winfo_height(),
                                                          fill="red")

        self.red_gun = self.audio_canvas.create_image(self.start_cursor_position,
                                                      self.audio_canvas.winfo_height() - self.scale_height - 30, anchor = tk.S,
                                                      image=red_gun_icon)
        self.red_gun2 = self.audio_canvas.create_image(self.start_cursor_position,
                                                      self.scale_height + 30, anchor = tk.N,
                                                      image=red_gun_icon)

        self.mousex_rel = self.image_middle + (self.mousex_oncanvas - 0.5) * (self.audio_zoom_x - 1)* 2 ** (1
            -self.audio_zoom_x)
        #duration = len(self.audio_data)/self.audio_sr
        #start = 0


        #print(delta, self.audio_zoom_x, self.image_middle)

    def create_signal(self):
        self.audio_data, self.audiosr = sf.read("temporary.wav")
        self.handle_scroll(event = 0)
        return

    def display_zoom(self,event):
        self.disx, self.disy = event.x, event.y
        rect_width, rect_height = 30, 50
        def sig(x):
            if x < 0:
                return 0
            else:
                return x

        try:
            self.image_canvas2.delete(self.zoom_rectangle)
        except:
            pass

        try:
            x_left = sig(self.disx-rect_width//2)
            x_right = sig(self.disx + rect_width // 2)
            y_top = sig(self.disy-rect_height//2)
            y_bottom = sig(self.disy+rect_height//2)

            points = [x_left, y_top, x_right, y_top, x_right, y_bottom, x_left, y_bottom, x_left, y_top]
            self.zoom_rectangle = self.image_canvas2.create_line(points, fill = "#00FF00")

            x_left_ratio = ((self.image_canvas2.winfo_width() - x_left)/self.frames_width)
            x_right_ratio = ((self.image_canvas2.winfo_width() - x_right) / self.frames_width)
            y_top_ratio = (sig(y_top-30)/(self.frames_height))
            y_bottom_ratio = (sig(y_bottom-30)/(self.frames_height))

            #print(x_left_ratio, x_right_ratio,y_top_ratio,y_bottom_ratio, self.frames_or_width,self.frames_or_height)

            left_crop = int(self.frames_or_width*(1-x_left_ratio))
            right_crop = int(self.frames_or_width*(1-x_right_ratio))
            top_crop = int(y_top_ratio*self.frames_or_height)
            bottom_crop = int(y_bottom_ratio*self.frames_or_height)

            #print(left_crop,right_crop,top_crop,bottom_crop)

            self.frames_zoomed = self.frames_original[top_crop:bottom_crop,left_crop:right_crop]
            #cv2.imwrite("zoomed.png",self.frames_zoomed)
            self.frames_zoomed = cv2.resize(self.frames_zoomed, (300,500))
            self.frames_zoomed = ImageTk.PhotoImage(Image.fromarray(self.frames_zoomed))
            self.preview_canvas.create_image(0,0,anchor = tk.NW, image = self.frames_zoomed)
        except:
            pass

    def display_frames(self, event):
        #print("button 3")

        self.image_canvas2.delete("all")
        start_frame = int((self.current_time - self.image_start_time_full)*self.fps*self.interpolation_factor)
        frames = []
        the_range = 6
        start_time = self.image_start_time_full + start_frame/(self.fps*self.interpolation_factor)
        times = []
        if self.image_end_time_full-self.current_time < 1.5:
            the_range = int(6*(self.image_end_time_full-self.current_time)/1.5)
        for i in range(the_range):
            #try:
            print(start_frame-i*int((0.3)*self.fps*self.interpolation_factor), self.fps*self.interpolation_factor, self.current_time , self.image_start_time_full)
            times.append(start_time - i*0.3)
            frames.append(self.framess[start_frame-i*int(0.3*self.fps*self.interpolation_factor)])
            #except:
            #    pass
        #print(len(self.framess))
        #print(len(frames))
        #print(times)
        frames = [frames[-i-1] for i in range(len(frames))]

        self.frames_original = cv2.hconcat(frames)
        self.frames_or_height,self.frames_or_width = cv2.hconcat(frames).shape
        #cv2.imwrite("frames.png", self.frames_original)
        self.frames_resized = cv2.resize(self.frames_original, (int((len(frames)/6)*self.image_canvas2.winfo_width()),self.image_canvas2.winfo_height()-30))

        self.frames_height, self.frames_width = self.frames_resized.shape
        self.frames_image = ImageTk.PhotoImage(Image.fromarray(self.frames_resized))
        #print(self.frames_width, self.frames_height)
        points = [1,30,1,1,int(self.image_canvas2.winfo_width()/6),1,int(self.image_canvas2.winfo_width()/6),30,int(self.image_canvas2.winfo_width()/6),1,
                  int(2*self.image_canvas2.winfo_width()/6),1,int(2*self.image_canvas2.winfo_width()/6),30,int(2*self.image_canvas2.winfo_width()/6),1,
                  int(3*self.image_canvas2.winfo_width()/6),1,int(3*self.image_canvas2.winfo_width()/6),30,int(3*self.image_canvas2.winfo_width()/6),1,
                  int(4*self.image_canvas2.winfo_width()/6),1,int(4*self.image_canvas2.winfo_width()/6),30,int(4*self.image_canvas2.winfo_width()/6),1,
                  int(5*self.image_canvas2.winfo_width()/6),1,int(5*self.image_canvas2.winfo_width()/6),30,int(5*self.image_canvas2.winfo_width()/6),1,
                  int(self.image_canvas2.winfo_width()),1,int(self.image_canvas2.winfo_width()),30,int(self.image_canvas2.winfo_width()),1,]

        self.image_canvas2.create_line(points, fill="black")

        self.image_canvas2.create_image(self.image_canvas2.winfo_width(), 30, anchor = tk.NE, image = self.frames_image)

        for i in range(len(times)):
            string = str(int(times[i]//60)) + ":" +str((int((times[i]%60)*100+0.5))/100)
            x_pos = int(self.image_canvas2.winfo_width()*(11/12))-i*int(self.image_canvas2.winfo_width()/6)
            #print(i,x_pos,string)
            self.image_canvas2.create_text(x_pos, 1, text = string, anchor = tk.N, fill="#DDDDDD")
        return

    def update_image(self):
        self.update_image_var = True
        #print(self.update_image_var)
        self.generate_image()

    def generate_new_image(self):
        self.update_image_var = False
        self.generate_image()


    #this function crops all video frames, and stitches all the cropped frames to generate one single time-synchronized photo finish image.
    def generate_image(self):
        self.timeline_ready = False
        self.results = []
        self.deleted_results = []

        self.image_zoom_x = 1
        self.image_center = 0.5

        self.image_offset_x = int(self.image_center_entry.get())
        self.line_thickness = int(self.frame_width_entry.get())
        self.image_offset_upper = int(self.top_y_offset_entry.get())
        self.image_offset_lower = int(self.bottom_y_offset_entry.get())

        if self.update_image_var == False:
            #print("2",self.update_image_var)
            self.create_image()


        def crop_stitch():
            while True:
                if self.frames_ready == False:
                    time.sleep(0.2)
                else:
                    break
            start_y = self.image_offset_upper
            end_y = self.frame_height - self.image_offset_lower
            middle_x = self.frame_width // 2 + self.image_offset_x
            start_x = middle_x - (self.line_thickness + 1) // 2
            end_x = middle_x + (self.line_thickness + 1) // 2
            #print(start_y,end_y,middle_x,start_x,end_x)
            if self.fps_inc_combo.get() == "Do not increase FPS":
                self.frame_interpolation = False
            else:
                self.frame_interpolation = True
                self.interpolation_factor = int(str(self.fps_inc_combo.get()).split("x")[-1])
            if self.update_image_var == False:
                if self.frame_interpolation == True:
                    """
                    this block interpolates frames.
                    it adds frames in between existing frames by calculating the optic flow.
                    so for etc. in frame1, the object is at x=5, in frame2, the object is at x=6; in the interpolated frame, it is gonna apper to be at x = 5.5
                    there is no need for this funcion if frame rate is large enough.
                    """
                    interpolation_factor = self.interpolation_factor
                    #self.frames_to_interpolate = [cv2.resize]
                    interpolated_frames = []

                    background_frame = self.framess[-1]

                    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_ULTRAFAST)

                    for i in range(len(self.framess) - 1):
                        frame1 = self.framess[i]
                        frame2 = self.framess[i + 1]

                        flow = dis.calc(frame1, frame2, None)
                        #flow[..., 1] = 0
                        interpolated_frames.append(frame1)

                        for j in range(1, interpolation_factor):
                            alpha = j / interpolation_factor
                            flow_scaled = flow * alpha

                            h, w = flow.shape[:2]
                            flow_map_x, flow_map_y = np.meshgrid(np.arange(w), np.arange(h))
                            flow_map_x = (flow_map_x - flow_scaled[..., 0]).astype(np.float32)
                            flow_map_y = (flow_map_y - flow_scaled[..., 1]).astype(np.float32)
                            flow_map = np.stack((flow_map_x, flow_map_y), axis=-1)

                            intermediate_frame = cv2.remap(frame1, flow_map, None, cv2.INTER_LINEAR)

                            static_mask = np.abs(background_frame - intermediate_frame) < 5

                            intermediate_frame_corrected = np.where(static_mask, background_frame, intermediate_frame)

                            interpolated_frames.append(intermediate_frame_corrected)

                        polygon_points = [self.status.winfo_width() - 600, 5,
                                              self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                              5, self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                              self.status.winfo_height() - 5,
                                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                        self.status.coords(self.progress_bar, polygon_points)
                        self.status.itemconfig(self.status_text, text="Interpolating frames: " + str(
                            int(100 * (i + 1) / len(self.framess))) + " %", font=self.font)


                    interpolated_frames.append(self.framess[-1])
                    def save_frames():
                        output_filename = 'output_video.avi'
                        frame_height, frame_width = interpolated_frames[0].shape[:2]
                        fps = self.fps*self.interpolation_factor

                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height), isColor=False)

                        for i in range(len(interpolated_frames)):

                            frame = interpolated_frames[i].astype(np.uint8)


                            out.write(frame)


                        out.release()

                        #custom progress bar
                        polygon_points = [self.status.winfo_width() - 600, 5,
                                          self.status.winfo_width() - 600 + int(((i + 1) / len(interpolated_frames)) * 600),
                                          5, self.status.winfo_width() - 600 + int(((i + 1) / len(interpolated_frames)) * 600),
                                          self.status.winfo_height() - 5,
                                          self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                        self.status.coords(self.progress_bar, polygon_points)
                        self.status.itemconfig(self.status_text, text="Saving interpolated video: " + str(
                            int(100 * (i + 1) / len(interpolated_frames))) + " %", font=self.font)
                    #threading.Thread(target = save_frames).start()
                    self.framess = interpolated_frames


            frames = []
            #for i in frames:
                #print(len(i))
            for i in range(len(self.framess)):
                frames.append(self.framess[i][start_y:end_y, start_x:end_x])

                polygon_points = [self.status.winfo_width() - 600, 5,
                                  self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                  5, self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                  self.status.winfo_height() - 5,
                                  self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                self.status.coords(self.progress_bar, polygon_points)
                self.status.itemconfig(self.status_text, text="Cropping & stitching frames: " + str(
                    int(100 * (i + 1) / len(self.framess))) + " %", font=self.font)

            polygon_points = [self.status.winfo_width() - 600, 5,
                              self.status.winfo_width() - 600,
                              5, self.status.winfo_width() - 600,
                              self.status.winfo_height() - 5,
                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

            self.status.coords(self.progress_bar, polygon_points)

            #print("direction:",self.direction.get())

            if self.direction.get() == 1:
                pass
            if self.direction.get() == 0:
                frames = [cv2.flip(i, 1) for i in frames]

            if self.background_change == True:

                self.resize_co = 5
                # Resize the sample frame once
                sample = len(frames)-90
                frames[sample] = cv2.resize(frames[sample],
                                          (int(self.frame_width / self.resize_co), int(self.frame_height / self.resize_co)))

                for j in range(len(frames)):
                    if j != sample:
                        current_frame = cv2.resize(frames[j], (
                        int(self.frame_width / self.resize_co), int(self.frame_height / self.resize_co)))

                        diff = cv2.absdiff(current_frame, frames[sample])

                        mask = abs(diff) < 35

                        current_frame[mask] = 255

                        frames[j] = current_frame

                        if j % 5 == 0:
                            polygon_points = [self.status.winfo_width() - 600, 5,
                                              self.status.winfo_width() - 600 + int(((j + 1) / len(frames)) * 600),
                                              5, self.status.winfo_width() - 600 + int(((j + 1) / len(frames)) * 600),
                                              self.status.winfo_height() - 5,
                                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                            self.status.coords(self.progress_bar, polygon_points)
                            self.status.itemconfig(self.status_text, text="Setting background: " + str(
                                int(100 * (j + 1) / len(frames))) + " %", font=self.font)

                        #self.root.update_idletasks()


            polygon_points = [self.status.winfo_width() - 600, 5,
                              self.status.winfo_width() - 600,
                              5, self.status.winfo_width() - 600,
                              self.status.winfo_height() - 5,
                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

            self.status.coords(self.progress_bar, polygon_points)

            self.timeline_image = cv2.hconcat(frames)

            self.timeline_image = cv2.flip(self.timeline_image, 1)

            #self.timeline_image = cv2.cvtColor(self.timeline_image, cv2.COLOR_RGB2GRAY)

            self.status.itemconfig(self.status_text,
                                   text="Photo-finish image is ready!", font=self.font)

            self.image_button.config(state="normal")
            self.image_update_button.config(state="normal")

            polygon_points = [self.status.winfo_width() - 600, 5,
                                              self.status.winfo_width() ,
                                              5, self.status.winfo_width(),
                                              self.status.winfo_height() - 5,
                                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

            self.status.coords(self.progress_bar, polygon_points)

            start_text = self.image_start_entry.get()
            if ":" in start_text:
                self.start_entry = float(start_text.split(":")[-1]) + (60) * float(start_text.split(":")[0])
            else:
                self.start_entry = float(start_text)

            end_text = self.image_end_entry.get()
            if ":" in end_text:
                self.end_entry = float(end_text.split(":")[-1]) + (60) * float(end_text.split(":")[0])
            else:
                self.end_entry = float(end_text)

            start_ratio = 1 - self.start_entry / self.duration

            if self.end_entry > self.duration:
                self.end_entry = self.duration

            end_ratio = 1 - self.end_entry / self.duration

            height, width = self.timeline_image.shape

            self.image = self.timeline_image[0:height, 0:]

            height, width = self.image.shape

            self.image_resized = cv2.resize(self.image, (
            int(width * (self.image_canvas.winfo_height() - self.scale_height) / height),
            (self.image_canvas.winfo_height() - self.scale_height)))
            self.timeline_ready = True



        crop_stitch_th = threading.Thread(target=crop_stitch)
        crop_stitch_th.start()






        def zoomed_images_thread():
            self.zoomed_images = []
            while True:
                if self.timeline_ready is False:
                    time.sleep(0.2)
                else:
                    break
            for i in range(1,self.max_image_zoom+1):
                zoomed = cv2.resize(self.image_resized, (int(((1/0.75)**(i-1))*self.image_canvas.winfo_width()),(self.image_canvas.winfo_height()-self.scale_height)))
                self.zoomed_images.append(zoomed)
                #cv2.imwrite("zoom"+str(i)+".png", zoomed)
                self.status.itemconfig(self.status_text,
                                       text="Constructing zoom levels "+str(i)+"/"+str(self.max_image_zoom) ,
                                       font=self.font)
                if i == 1:
                    self.visualise_image()
            self.status.itemconfig(self.status_text,
                                   text=str(self.max_image_zoom)+" zoom levels constructed!",
                                   font=self.font)

        images_thread = threading.Thread(target=zoomed_images_thread)
        images_thread.start()



        #cv2.imwrite("test_cropped.png", self.image)

    def on_click_image(self, event):
        self.results.append(self.current_time)
        self.results_sorted = self.results.sort()
        self.visualise_image()
        self.table.update_results(self.results)
        self.table.update_table()
        return

    def undo(self):
        self.deleted_results.append(self.results[-1])
        del self.results[-1]
        self.results_sorted = self.results.sort()
        self.visualise_image()

    def redo(self):
        self.results.append(self.deleted_results[-1])
        del self.deleted_results[-1]
        self.results_sorted = self.results.sort()
        self.visualise_image()

    def handle_scroll_image(self):
        return

    def leave_image_canvas(self,event):
        try:
            self.image_canvas.delete(self.hash_line)
            self.image_canvas.delete(self.hash_line_hor)
        except:
            pass

    def on_mouse_motion_image(self,event):
        self.mousex, self.mousey = event.x, event.y
        self.mousex_oncanvas = self.mousex/self.image_canvas.winfo_width()

        self.current_time = (1-self.mousex_oncanvas)*(self.image_end_time-self.image_start_time) + self.image_start_time

        current_time_str = str(int(self.current_time//60)) + ":" +str((int((self.current_time%60)*1000+0.5))/1000)

        self.status.itemconfig(self.status_text, text = current_time_str)

        try:
            self.image_canvas.delete(self.hash_line)
            self.image_canvas.delete(self.hash_line_hor)
        except:
            pass
        self.hash_line = self.image_canvas.create_line(self.mousex, 0, self.mousex, self.image_canvas.winfo_height()-self.scale_height,
                                                    fill=self.hashline_color)


        self.hash_line_hor = self.image_canvas.create_line(self.mousex-10, self.mousey, self.mousex+10, self.mousey,
                                                       fill=self.hashline_color)
        return

    def image_borders(self,var = None):
        if var == "vin" and self.image_zoom_x < self.max_image_zoom:
            self.image_zoom_x += 1

        elif var == "vout" and self.image_zoom_x > 1:
            self.image_zoom_x -= 1

        elif var == "vleft":
            self.image_center -= (1-0.75)*0.75**(self.image_zoom_x-1)

        elif var == "vright":
            self.image_center += (1-0.75)*0.75**(self.image_zoom_x-1)

        if self.image_center < 0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 0.5 *0.75** (self.image_zoom_x-1)

        elif self.image_center > 1-0.5*0.75**(self.image_zoom_x-1):
            self.image_center = 1- 0.5*0.75 ** (self.image_zoom_x-1)


        self.visualise_image()

    def visualise_image(self):

        self.image_canvas.delete("all")

        self.image_start_time_full = self.start_entry  + self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var)
        self.image_end_time_full = self.end_entry  + self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var)

        center_time = (1-self.image_center)*(self.image_end_time_full-self.image_start_time_full) + self.image_start_time_full

        self.image_start_time = center_time - (self.image_end_time_full-self.image_start_time_full)*0.5*0.75 ** (self.image_zoom_x-1)
        self.image_end_time = center_time + (self.image_end_time_full - self.image_start_time_full) * 0.5*0.75 ** (self.image_zoom_x-1)

        start = self.image_center - 0.5*0.75 ** (self.image_zoom_x-1)
        end = self.image_center + 0.5*0.75 ** (self.image_zoom_x-1)


        level = np.log(self.image_end_time-self.image_start_time)/np.log(10)
        level = int(level+0.5)
        tick_increments = 10**(level-2)
        label_increments = 10**(level-1)

        tick_start = self.image_start_time - self.image_start_time%tick_increments + tick_increments
        tick_end = self.image_end_time - self.image_end_time%tick_increments
        ticks = np.arange(tick_start,tick_end+10*tick_increments,tick_increments)

        label_start = self.image_start_time - self.image_start_time % label_increments + label_increments
        label_end = self.image_end_time - self.image_end_time % label_increments
        labels = np.arange(label_start, label_end + label_increments, label_increments)

        locations = self.image_canvas.winfo_width()*(1-(ticks-self.image_start_time)/(self.image_end_time-self.image_start_time))

        locations_2 = self.image_canvas.winfo_width() * (1-(labels - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))

        #print(labels)
        #print(locations_2)

        loc_points = []
        scaleY = self.image_canvas.winfo_height() - self.scale_height
        for i in range(len(locations)-1):
            loc_points.append(locations[i])
            loc_points.append(scaleY+5)
            loc_points.append(locations[i])
            loc_points.append(scaleY)
            loc_points.append(locations[i+1])
            loc_points.append(scaleY)

        #print("time borders:",self.image_start_time,self.image_end_time)

        #print("center:",self.image_center)
        #print("zoom:", self.image_zoom_x)

        for i in range(len(labels)):
            if label_increments >=1:
                thestr = str(int(labels[i]))
            else:
                thestr = round(labels[i]*(1/label_increments))*label_increments
                thestr = str(thestr)
                thestr = thestr.split(".")[0]+"."+thestr.split(".")[-1][:int(np.log(1/label_increments)/np.log(10))]

            self.image_canvas.create_text(locations_2[i],self.image_canvas.winfo_height()-10,text = thestr,fill="#DDDDDD")
            self.image_canvas.create_line(locations_2[i],self.image_canvas.winfo_height()-20,locations_2[i],scaleY,fill = "#DDDDDD")


        #print("borders:", start, end)
        #print(len(self.zoomed_images))

        height1, width1  = self.zoomed_images[0].shape

        cropped_image = self.zoomed_images[self.image_zoom_x - 1][0:height1,
                        int(width1 * (1/0.75) ** (self.image_zoom_x - 1) * start):int(
                            width1 * (1/0.75) ** (self.image_zoom_x - 1) * end)]

        image_pil = Image.fromarray(cropped_image)

        self.image_tk = ImageTk.PhotoImage(image_pil)
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.image_canvas.create_line(loc_points, fill="#DDDDDD")

        for i in self.results:
            X = self.image_canvas.winfo_width() * (1 - (i - self.image_start_time) / (
                    self.image_end_time - self.image_start_time))
            self.image_canvas.create_line(X, 0, X,self.image_canvas.winfo_height() - self.scale_height,
                                                       fill=self.hashline_color)
        return


    def create_image(self):
        self.image_button.config(state="disabled")
        self.image_update_button.config(state="disabled")
        self.frames_ready = False

        if not self.image_start_entry.get():
            self.image_start_entry.insert(0,"0")
        if not self.image_end_entry.get():
            self.image_end_entry.insert(0,"9999999")

        start_text = self.image_start_entry.get()
        if ":" in start_text:
            self.start_entry = float(start_text.split(":")[-1]) + (60) * float(start_text.split(":")[0])
            self.image_start_entry.insert(0, str(self.start_entry))
        else:
            self.start_entry = float(start_text)
        #print(self.start_entry)
        if self.start_entry < 0:
            self.start_entry = 0
            self.image_start_entry.insert(0, str(self.start_entry))

        end_text = self.image_end_entry.get()
        if ":" in end_text:
            self.end_entry = float(end_text.split(":")[-1]) + (60) * float(end_text.split(":")[0])
            self.image_end_entry.insert(0, str(self.end_entry))
        else:
            self.end_entry = float(end_text)
        if self.end_entry > self.duration - self.start_time-0.1 + self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var):
            self.end_entry = self.duration - self.start_time-0.1 + self.time_var + self.gun_mic_var/(self.sound_var+self.wind_var) - self.gun_start_var/(self.sound_var)
            self.image_end_entry.insert(0, str(self.end_entry))
        if self.end_entry < self.start_entry:
            self.end_entry = self.start_entry +1
            self.image_end_entry.insert(0, str(self.end_entry))


        def image_in_thread():
            #clip = VideoFileClip(self.video_file)
            #framess = [frame for frame in clip.iter_frames()]
            cap = cv2.VideoCapture(self.video_file)

            self.framess = []
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            self.fps = fps
            cap.set(cv2.CAP_PROP_POS_FRAMES,int((float(self.image_start_entry.get())+self.start_time) * fps))
            #print("fps",fps)
            progress_points = [self.status.winfo_width() -600-1,5,self.status.winfo_width()-1,5,self.status.winfo_width()-1,self.status.winfo_height()-5,self.status.winfo_width()-600-1,self.status.winfo_height()-5,self.status.winfo_width()-600-1,5]
            self.progress_bar_bg = self.status.create_line(progress_points, fill = "#00FF00")
            #stamp = 0
            #print(self.duration)
            for i in range(int((float(self.image_start_entry.get())+self.start_time) * fps),int((float(self.image_end_entry.get())+self.start_time) * fps)-1):
                ret, frame = cap.read()
                if not ret:
                    break
                #print(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
                #stamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                self.framess.append(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))
                polygon_points = [self.status.winfo_width()  - 600, 5, self.status.winfo_width() -600 +int( ((i+1-int((float(self.image_start_entry.get())+self.start_time) * fps))/(int((float(self.image_end_entry.get())+self.start_time) * fps)-int((float(self.image_start_entry.get())+self.start_time) * fps))) * 600),
                                  5, self.status.winfo_width() -600 + int( ((i+1-int((float(self.image_start_entry.get())+self.start_time) * fps))/(int((float(self.image_end_entry.get())+self.start_time) * fps)-int((float(self.image_start_entry.get())+self.start_time) * fps))) * 600), self.status.winfo_height() - 5,
                                  self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                self.status.coords(self.progress_bar,polygon_points)

                self.status.itemconfig(self.status_text, text = "Extracting video frames: "+str(int(100 * ((i+1-int((float(self.image_start_entry.get())+self.start_time) * fps)) / (( int((float(self.image_end_entry.get())+self.start_time) * fps)-1)-(int((float(self.image_start_entry.get())+self.start_time) * fps)))))) + " %", font = self.font)

            self.status.itemconfig(self.status_text,
                                   text="Video frames ready!",
                                   font=self.font)
            self.preview_button.config(state="normal")
            cap.release()
            self.frame_height, self.frame_width = self.framess[0].shape

            #print(self.frame_height)

            self.frames_ready = True
            #cv2.imwrite("test.png",self.timeline_image)

        image_thread = threading.Thread(target = image_in_thread)
        image_thread.start()

    def import_heat(self):
        file = filedialog.askopenfilename()
        if file.split(".")[-1] == "xlsx":
            dataframe = openpyxl.load_workbook(file)
            dataframe1 = dataframe.active

            import_heat_w = tk.Toplevel(self.root)
            import_heat_w.wm_iconphoto(False, self.main_icon)
            import_heat_w.wm_title("Import Heat...")

            columns = []
            column_names = [0,"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","V","W","X","Y","Z"]
            for col in range(1, dataframe1.max_column+1):
                tk.Label(import_heat_w, text="Column "+column_names[col]+":").pack()
                globals()[f'col{col}'] =  ttk.Combobox(import_heat_w,values = ["Lane","ID","Name","Date of Birth","Affiliation","License","Time","Place"],state="readonly", width = 9)
                globals()[f'col{col}'].set("nan")
                globals()[f'col{col}'].pack()
                columns.append(globals()[f'col{col}'])



            def done_with_heat():
                df = pd.read_excel(file)

                matrix = df.values
                athletes = []
                for i in range(len(matrix)):
                    athletes.append(dict(self.default_athlete))
                    #self.private_id += 1
                    #athletes[-1]["priv_id"] = int(self.private_id)
                    for j in range(len(matrix[0])):
                        try:
                            athletes[i][globals()[f'col{j + 1}'].get()] = str(matrix[i][j])
                        except:
                            pass
                        print(matrix[i][j])

                for i in range(len(matrix)):
                    athletes[i] = list(athletes[i].values())

                self.excel_import = True

                import_heat_w.destroy()

                self.table.change_title("Title: "+str(file).split("/")[-1].split(".")[0]+", Wind: "+str(self.wind_var)+" m/s")




                self.table.set_data_from_matrix(athletes)
            tk.Button(import_heat_w,text="Ok",command= done_with_heat).pack()

            heat_height = 42*len(columns)+50
            import_heat_w.geometry("250x"+str(heat_height))

            import_heat_w.mainloop()

    def view_pf(self):
        self.view_pf_var = True
        self.take_canvas_screenshot()
        return

    def take_canvas_screenshot(self):
        if self.view_pf_var == False:
            filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))

        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        image_pil = Image.new('RGB', (canvas_width, canvas_height), 'white')
        draw = ImageDraw.Draw(image_pil)

        font = ImageFont.load_default()

        level = np.log(self.image_end_time - self.image_start_time) / np.log(10)
        level = int(level+0.5)
        tick_increments = 10 ** (level - 2)
        label_increments = 10 ** (level - 1)

        tick_start = self.image_start_time - self.image_start_time % tick_increments + tick_increments
        tick_end = self.image_end_time - self.image_end_time % tick_increments
        ticks = np.arange(tick_start, tick_end + 10*tick_increments, tick_increments)

        label_start = self.image_start_time - self.image_start_time % label_increments + label_increments
        label_end = self.image_end_time - self.image_end_time % label_increments
        labels = np.arange(label_start, label_end + label_increments, label_increments)

        locations = canvas_width * (1 - (ticks - self.image_start_time) / (self.image_end_time - self.image_start_time))
        locations_2 = canvas_width * (
                    1 - (labels - self.image_start_time) / (self.image_end_time - self.image_start_time))

        scaleY = canvas_height - self.scale_height

        for i in range(len(ticks) - 1):
            draw.line([locations[i], scaleY + 5, locations[i], scaleY], fill="black")
            draw.line([locations[i], scaleY, locations[i + 1], scaleY], fill="black")

        for i in range(len(labels)):
            if label_increments >= 1:
                thestr = str(int(labels[i]))
            else:
                thestr = round(labels[i] * (1 / label_increments)) * label_increments
                thestr = str(thestr)
                thestr = thestr.split(".")[0] + "." + thestr.split(".")[-1][
                                                      :int(np.log(1 / label_increments) / np.log(10))]


            bbox = draw.textbbox((0, 0), thestr, font=font)
            text_width = bbox[2] - bbox[0]  # bbox[2] is the x2 coordinate, bbox[0] is the x1 coordinate
            text_height = bbox[3] - bbox[1]  # bbox[3] is the y2 coordinate, bbox[1] is the y1 coordinate

            draw.text((locations_2[i] - text_width / 2, canvas_height - 10 - text_height / 2), thestr, fill="black",
                      font=font)

            draw.line([locations_2[i], canvas_height - 20, locations_2[i], scaleY], fill="black")

        start = self.image_center - 0.5 * 0.75 ** (self.image_zoom_x - 1)
        end = self.image_center + 0.5 * 0.75 ** (self.image_zoom_x - 1)

        if self.zoomed_images:
            height1, width1 = self.zoomed_images[0].shape
            cropped_image = self.zoomed_images[self.image_zoom_x - 1][0:height1,
                            int(width1 * (1 / 0.75) ** (self.image_zoom_x - 1) * start):int(
                                width1 * (1 / 0.75) ** (self.image_zoom_x - 1) * end)]
            cropped_image_pil = Image.fromarray(cropped_image)
            image_pil.paste(cropped_image_pil, (0, 0))

        for i in self.results:
            X = canvas_width * (1 - (i - self.image_start_time) / (self.image_end_time - self.image_start_time))
            draw.line([X, 0, X, canvas_height - self.scale_height], fill=self.hashline_color)

        if self.view_pf_var == False:
            image_pil.save(filename)
        else:
            self.view_pf_var = False
            pf_display = tk.Toplevel(self.root)
            pf_display.title("Photo-finish image")
            pf_display.attributes("-topmost", True)
            pf_display.wm_iconphoto(False, self.main_icon)
            pf_display.resizable(False,False)
            x_dim = self.image_canvas.winfo_width()
            y_dim = self.image_canvas.winfo_height()

            pf_display.geometry(f"{x_dim}x{y_dim}")

            pf_canvas = tk.Canvas(pf_display,width = x_dim, height = y_dim)
            pf_canvas.pack()

            tk_image = ImageTk.PhotoImage(image_pil)
            pf_canvas.create_image(0,0, anchor = tk.NW,image = tk_image,)

            pf_display.mainloop()



    def export_results_table(self):
        def as_txt():
            results_text_file = asksaveasfile(defaultextension = "*.txt",filetypes=[("Text Documents", "*.txt"),("All Files", "*.*")])
            results_text_file.write("Lane\tID\tFull-Name\tAffiliation\tLicense\tTime\tPlace\n")
            for i in self.resultlabels:
                for j in range(7):
                    results_text_file.write(i[j].get()+"\t")
                results_text_file.write("\n")
            return
        def as_xlsx():
            allresults = self.table.data
            df = pd.DataFrame(allresults,columns = ["Lane","ID","Name","Date of Birth","Affiliation","License","Time","Place"])
            results_ex_file = asksaveasfile(defaultextension = "*.xlsx",filetypes=[("Text Documents", "*.xlsx"),("All Files", "*.*")])
            df.to_excel(results_ex_file.name, sheet_name = "Results", index=False)
            return

        def as_photo():
            if self.results_on == 1:
                self.result_window.deiconify()
                self.results_on = 2
            time.sleep(2)
            self.take_canvas_screenshot(mode = 1)
            return

        def onclose():
            self.export_window.destroy()

        self.export_window = tk.Toplevel(self.root)
        self.export_window .title("Export Results...")
        self.export_window.wm_iconphoto(False, self.export_image_icon)
        self.export_window.geometry("270x70")
        self.export_window.resizable(False, False)
        self.export_window.protocol("WM_DELETE_WINDOW", onclose)

        exportresults = tk.Label(self.export_window,text="Export results as: ")
        exportresults.place(x=5,y = 5)
        exporttype = ttk.Combobox(self.export_window,state = "readonly",values=["Excel file (*.xlsx)","Text file (*.txt)","Image file (*.png)"],width = 16)
        exporttype.set("Excel file (*.xlsx)")
        exporttype.place(x = 120, y = 5)

        def export_ok():
            if exporttype.get() == "Excel file (*.xlsx)":
                as_xlsx()
            elif exporttype.get() == "Text file (*.txt)":
                as_txt()
            elif exporttype.get() == "Image file (*.png)":
                if self.results_on == 1:
                    self.result_window.deiconify()
                    self.results_on = 2
                self.take_canvas_screenshot(mode = 1)
            else:
                print("no save type detected",exporttype.get())
            self.export_window.destroy()
            return
        exportok = tk.Button(self.export_window,text="Export",command = export_ok)
        exportok.place ( x = 100, y = 40)

        return

    def results_table(self):
        return
    def options(self):
        self.options_window = tk.Toplevel(self.root)
        self.options_window.title("Options")
        self.options_window.wm_iconphoto(False, options_icon)
        self.options_window.resizable(False, False)
        self.options_window.geometry("355x505")
        self.options_window.option_add('*Background', '#222222')
        self.options_window.option_add('*Foreground', '#FFFFFF')
        self.options_window.option_add('*Button.Background', '#222222')

        self.notebook_options = ttk.Notebook(self.options_window)
        self.notebook_options.pack(expand=True, fill='both')

        self.calibration_options = tk.Frame(self.notebook_options)
        self.display_options = tk.Frame(self.notebook_options)


        self.notebook_options.add(self.calibration_options, text='Calibration')
        self.notebook_options.add(self.display_options , text='Display')


        self.sound_options = tk.Canvas(self.calibration_options, width=350, height=800, bg="#222222",
                                       highlightthickness=0)
        self.sound_options.pack(side=tk.LEFT)

        tk.Label(self.sound_options, text="Sound Calibration").place(x=175, y=10, anchor="center")

        points = [250, 10, 345, 10, 345, 660, 5, 660, 5, 10, 100, 10]
        self.sound_options.create_line(points, fill="#CCCCCC")




        def apply():
            self.gun_mic_var = float(self.gun_mic_entry.get())
            self.gun_start_var = float(self.gun_start_entry.get())
            self.sound_var = float(self.sound_entry.get())
            self.wind_var = float(self.wind_entry.get())
            self.time_var = float(self.time_entry.get())
            return

        self.apply_button = tk.Button(self.sound_options, text = "Apply", command = apply)
        self.apply_button.place(x = 175, y  =450, anchor = "center")



        self.options_window.mainloop()
        #return

    def leave_image_canvas2(self,event):
        try:
            self.preview_frame()
        except:
            pass

    def preview_frame(self):
        try:
            self.image_canvas2.delete(self.zoom_rectangle)
        except:
            pass
        self.line_thickness = int(self.frame_width_entry.get())
        width, height = self.preview_canvas_width, self.preview_canvas_height

        x_ratio = width / self.frame_width
        y_ratio = height / self.frame_height

        #print("preview frame")


        sample_image = self.framess[-1]
        image = ImageTk.PhotoImage(
            Image.fromarray(cv2.resize(sample_image, (width + 1, height + 1))))

        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=image)

        self.preview_canvas.image = image


        image_center_offset = int(self.image_center_entry.get())
        top_y_offset = int(self.top_y_offset_entry.get())
        bottom_y_offset = int(self.bottom_y_offset_entry.get())

        """
        x_min = int(self.frame_width // 2 - self.line_thickness // 2 + image_center_offset)
        x_max = int(self.frame_width // 2 + self.line_thickness // 2 + image_center_offset)
        y_min = top_y_offset
        y_max = self.frame_height - bottom_y_offset

        #print(x_min, x_max, y_min, y_max)


        resized_x = self.line_thickness * x_ratio
        resized_y = y_ratio * (self.frame_height - top_y_offset - bottom_y_offset)
        #print(y_ratio, height, top_y_offset, bottom_y_offset, resized_y)

        cropped_image_array = sample_image[y_min:y_max, x_min:x_max]  # Fix slicing order
        cropped_image = ImageTk.PhotoImage(Image.fromarray(
            cv2.cvtColor(cv2.resize(cropped_image_array, (int(resized_x)+2, int(resized_y))), cv2.COLOR_BGR2RGB)))
        """
        top_y = int(y_ratio * top_y_offset)
        bottom_y = int(y_ratio * (self.frame_height - bottom_y_offset))

        left_x = int(x_ratio * (self.frame_width // 2 - self.line_thickness // 2 + image_center_offset))
        right_x = int(x_ratio * (self.frame_width // 2 + self.line_thickness // 2 + image_center_offset))

        points = [left_x, top_y, right_x, top_y, right_x, bottom_y, left_x, bottom_y, left_x, top_y]


        #self.preview_canvas.create_image(left_x+1, top_y+1, anchor=tk.NW, image=cropped_image)
        self.preview_canvas.create_line(points, fill="#00FF00")
        #print(self.frame_width, points)

        #self.preview_canvas.image2 = cropped_image

    def auto_width(self):
        lower_res = [cv2.resize(i, (int(self.frame_width/4), int(self.frame_height/4))) for i in self.framess]
        """
        for i in range(len(self.framess)-1):
            difference_matrix =
        """
        return





#opticon = Image.open('images/stop.ico')

#array = np.array(Image.open('images/splash.png'))

"""
string = "["

for i in range(len(array)):
    string += "["
    for j in range(len(array[i])):
        string += "[" + ",".join(map(str, array[i][j])) + "]"
        if j < len(array[i]) - 1:
            string += ","
    string += "]"
    if i < len(array) - 1:
        string += ","

string += "]"


file = open("splash.py","w")
file.write(string)
print(string)
"""


root = tk.Tk()
root.title("MY Photo-Finish (host)")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 0
window_height = 0

# Calculate position x and y coordinates
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f'{window_width}x{window_height}+{x}+{y}')
root.overrideredirect(True)

opticon_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,66],[0,0,0,185],[0,0,0,189],[0,0,0,190],[0,0,0,177],[0,0,0,48],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,174],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,150],[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,57],[0,0,0,238],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,228],[0,0,0,44],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,31],[0,0,0,80],[0,0,0,36],[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,136],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,123],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,54],[0,0,0,102],[0,0,0,34],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,37],[0,0,0,190],[0,0,0,253],[0,0,0,224],[0,0,0,157],[0,0,0,72],[0,0,0,21],[0,0,0,67],[0,0,0,218],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,213],[0,0,0,65],[0,0,0,24],[0,0,0,83],[0,0,0,175],[0,0,0,237],[0,0,0,255],[0,0,0,190],[0,0,0,37],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,40],[0,0,0,193],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,244],[0,0,0,212],[0,0,0,239],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,239],[0,0,0,216],[0,0,0,247],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,194],[0,0,0,40],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,154],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,136],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,120],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,252],[0,0,0,94],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,41],[0,0,0,226],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,213],[0,0,0,28],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,146],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,132],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,64],[0,0,0,244],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,242],[0,0,0,197],[0,0,0,161],[0,0,0,161],[0,0,0,197],[0,0,0,242],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,241],[0,0,0,59],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,100],[0,0,0,252],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,194],[0,0,0,72],[0,0,0,13],[0,0,0,1],[0,0,0,1],[0,0,0,13],[0,0,0,72],[0,0,0,194],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,252],[0,0,0,100],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,7],[0,0,0,52],[0,0,0,132],[0,0,0,224],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,189],[0,0,0,31],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,31],[0,0,0,189],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,227],[0,0,0,144],[0,0,0,66],[0,0,0,14],[0,0,0,0]],[[0,0,0,77],[0,0,0,170],[0,0,0,236],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,236],[0,0,0,61],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,61],[0,0,0,236],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,244],[0,0,0,191],[0,0,0,103]],[[0,0,0,243],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,178],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,179],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,250]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,137],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,138],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,137],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,138],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[0,0,0,250],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,178],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,179],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,243]],[[0,0,0,103],[0,0,0,191],[0,0,0,244],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,236],[0,0,0,60],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,61],[0,0,0,236],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,236],[0,0,0,170],[0,0,0,77]],[[0,0,0,0],[0,0,0,14],[0,0,0,67],[0,0,0,145],[0,0,0,227],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,188],[0,0,0,30],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,31],[0,0,0,189],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,224],[0,0,0,133],[0,0,0,52],[0,0,0,7],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,101],[0,0,0,252],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,194],[0,0,0,71],[0,0,0,13],[0,0,0,1],[0,0,0,1],[0,0,0,13],[0,0,0,71],[0,0,0,194],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,252],[0,0,0,99],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,59],[0,0,0,242],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,242],[0,0,0,196],[0,0,0,160],[0,0,0,160],[0,0,0,196],[0,0,0,242],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,243],[0,0,0,64],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,132],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,146],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,213],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,226],[0,0,0,42],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,94],[0,0,0,252],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,120],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,137],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,155],[0,0,0,1],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,40],[0,0,0,194],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,247],[0,0,0,216],[0,0,0,239],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,239],[0,0,0,212],[0,0,0,244],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,193],[0,0,0,40],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,37],[0,0,0,191],[0,0,0,255],[0,0,0,237],[0,0,0,175],[0,0,0,83],[0,0,0,24],[0,0,0,65],[0,0,0,214],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,218],[0,0,0,67],[0,0,0,21],[0,0,0,71],[0,0,0,157],[0,0,0,224],[0,0,0,253],[0,0,0,190],[0,0,0,37],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,34],[0,0,0,102],[0,0,0,54],[0,0,0,8],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,124],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,137],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,36],[0,0,0,81],[0,0,0,31],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,44],[0,0,0,228],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,238],[0,0,0,58],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,150],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,175],[0,0,0,9],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,48],[0,0,0,177],[0,0,0,190],[0,0,0,189],[0,0,0,185],[0,0,0,67],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
array_np = np.array(opticon_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
options_icon = ImageTk.PhotoImage(image)

resultico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,47],[0,0,0,228],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,228],[0,0,0,47],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,73],[0,0,0,249],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,249],[0,0,0,73],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,73],[0,0,0,249],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,249],[0,0,0,73],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,58],[0,0,0,236],[0,0,0,253],[0,0,0,253],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,253],[0,0,0,236],[0,0,0,58],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,64],[0,0,0,82],[0,0,0,145],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,141],[0,0,0,82],[0,0,0,64],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,21],[0,0,0,11],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,91],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,85],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,20],[0,0,0,15],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,66],[0,0,0,205],[0,0,0,160],[0,0,0,24],[0,0,0,0],[0,0,0,2],[0,0,0,29],[0,0,0,82],[0,0,0,172],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,170],[0,0,0,82],[0,0,0,30],[0,0,0,2],[0,0,0,0],[0,0,0,50],[0,0,0,197],[0,0,0,181],[0,0,0,37],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,44],[0,0,0,216],[0,0,0,255],[0,0,0,254],[0,0,0,172],[0,0,0,61],[0,0,0,136],[0,0,0,218],[0,0,0,251],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,251],[0,0,0,218],[0,0,0,136],[0,0,0,74],[0,0,0,201],[0,0,0,255],[0,0,0,255],[0,0,0,188],[0,0,0,21],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,67],[0,0,0,241],[0,0,0,255],[0,0,0,255],[0,0,0,253],[0,0,0,241],[0,0,0,254],[0,0,0,255],[0,0,0,237],[0,0,0,196],[0,0,0,158],[0,0,0,137],[0,0,0,137],[0,0,0,158],[0,0,0,196],[0,0,0,237],[0,0,0,255],[0,0,0,254],[0,0,0,245],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,210],[0,0,0,28],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,5],[0,0,0,109],[0,0,0,239],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,227],[0,0,0,136],[0,0,0,52],[0,0,0,13],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,11],[0,0,0,52],[0,0,0,136],[0,0,0,227],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,223],[0,0,0,68],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,15],[0,0,0,186],[0,0,0,255],[0,0,0,253],[0,0,0,178],[0,0,0,49],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,10],[0,0,0,71],[0,0,0,62],[0,0,0,25],[0,0,0,1],[0,0,0,1],[0,0,0,49],[0,0,0,178],[0,0,0,253],[0,0,0,255],[0,0,0,173],[0,0,0,10],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,107],[0,0,0,247],[0,0,0,254],[0,0,0,156],[0,0,0,19],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,27],[0,0,0,218],[0,0,0,246],[0,0,0,215],[0,0,0,143],[0,0,0,44],[0,0,0,0],[0,0,0,19],[0,0,0,156],[0,0,0,254],[0,0,0,248],[0,0,0,107],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,47],[0,0,0,224],[0,0,0,255],[0,0,0,174],[0,0,0,18],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,222],[0,0,0,93],[0,0,0,2],[0,0,0,18],[0,0,0,174],[0,0,0,255],[0,0,0,224],[0,0,0,46],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,2],[0,0,0,148],[0,0,0,255],[0,0,0,221],[0,0,0,45],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,240],[0,0,0,99],[0,0,0,0],[0,0,0,45],[0,0,0,221],[0,0,0,255],[0,0,0,148],[0,0,0,2],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,38],[0,0,0,225],[0,0,0,255],[0,0,0,125],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,228],[0,0,0,56],[0,0,0,0],[0,0,0,125],[0,0,0,255],[0,0,0,225],[0,0,0,39],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,99],[0,0,0,255],[0,0,0,230],[0,0,0,43],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,165],[0,0,0,3],[0,0,0,42],[0,0,0,230],[0,0,0,255],[0,0,0,99],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,154],[0,0,0,255],[0,0,0,182],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,232],[0,0,0,45],[0,0,0,5],[0,0,0,182],[0,0,0,255],[0,0,0,154],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,188],[0,0,0,255],[0,0,0,139],[0,0,0,0],[0,0,0,2],[0,0,0,6],[0,0,0,5],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,221],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,254],[0,0,0,94],[0,0,0,0],[0,0,0,139],[0,0,0,255],[0,0,0,188],[0,0,0,8],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,16],[0,0,0,204],[0,0,0,255],[0,0,0,116],[0,0,0,0],[0,0,0,55],[0,0,0,184],[0,0,0,152],[0,0,0,13],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,27],[0,0,0,216],[0,0,0,252],[0,0,0,250],[0,0,0,250],[0,0,0,250],[0,0,0,250],[0,0,0,250],[0,0,0,253],[0,0,0,122],[0,0,0,0],[0,0,0,116],[0,0,0,255],[0,0,0,204],[0,0,0,15],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,17],[0,0,0,206],[0,0,0,255],[0,0,0,114],[0,0,0,0],[0,0,0,52],[0,0,0,175],[0,0,0,145],[0,0,0,12],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,67],[0,0,0,78],[0,0,0,77],[0,0,0,77],[0,0,0,77],[0,0,0,77],[0,0,0,77],[0,0,0,78],[0,0,0,40],[0,0,0,0],[0,0,0,114],[0,0,0,255],[0,0,0,206],[0,0,0,17],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,11],[0,0,0,194],[0,0,0,255],[0,0,0,133],[0,0,0,0],[0,0,0,1],[0,0,0,3],[0,0,0,2],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,133],[0,0,0,255],[0,0,0,194],[0,0,0,11],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,2],[0,0,0,164],[0,0,0,255],[0,0,0,172],[0,0,0,4],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,4],[0,0,0,172],[0,0,0,255],[0,0,0,164],[0,0,0,2],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,113],[0,0,0,255],[0,0,0,221],[0,0,0,32],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,32],[0,0,0,221],[0,0,0,255],[0,0,0,113],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,51],[0,0,0,235],[0,0,0,254],[0,0,0,105],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,105],[0,0,0,254],[0,0,0,235],[0,0,0,51],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,168],[0,0,0,255],[0,0,0,205],[0,0,0,28],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,28],[0,0,0,205],[0,0,0,255],[0,0,0,168],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,65],[0,0,0,237],[0,0,0,255],[0,0,0,146],[0,0,0,8],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,35],[0,0,0,37],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,8],[0,0,0,146],[0,0,0,255],[0,0,0,237],[0,0,0,65],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,135],[0,0,0,254],[0,0,0,247],[0,0,0,121],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,4],[0,0,0,170],[0,0,0,179],[0,0,0,7],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,7],[0,0,0,121],[0,0,0,247],[0,0,0,254],[0,0,0,135],[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,19],[0,0,0,173],[0,0,0,255],[0,0,0,246],[0,0,0,142],[0,0,0,24],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3],[0,0,0,160],[0,0,0,169],[0,0,0,6],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,24],[0,0,0,142],[0,0,0,246],[0,0,0,255],[0,0,0,173],[0,0,0,19],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,29],[0,0,0,175],[0,0,0,254],[0,0,0,253],[0,0,0,199],[0,0,0,93],[0,0,0,23],[0,0,0,1],[0,0,0,0],[0,0,0,21],[0,0,0,22],[0,0,0,1],[0,0,0,1],[0,0,0,23],[0,0,0,93],[0,0,0,199],[0,0,0,253],[0,0,0,254],[0,0,0,175],[0,0,0,29],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,21],[0,0,0,141],[0,0,0,241],[0,0,0,255],[0,0,0,250],[0,0,0,211],[0,0,0,156],[0,0,0,113],[0,0,0,91],[0,0,0,90],[0,0,0,113],[0,0,0,156],[0,0,0,211],[0,0,0,250],[0,0,0,255],[0,0,0,241],[0,0,0,141],[0,0,0,21],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,5],[0,0,0,71],[0,0,0,177],[0,0,0,240],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,254],[0,0,0,254],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,240],[0,0,0,177],[0,0,0,71],[0,0,0,5],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,12],[0,0,0,70],[0,0,0,147],[0,0,0,206],[0,0,0,239],[0,0,0,252],[0,0,0,252],[0,0,0,239],[0,0,0,206],[0,0,0,147],[0,0,0,70],[0,0,0,12],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(resultico_array)):
    for j in range(len(resultico_array[0])):
        resultico_array[i][j] = [255,255,255,resultico_array[i][j][3]]
array_np = np.array(resultico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
results_icon = ImageTk.PhotoImage(image)




playico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[7,7,7,255],[3,3,3,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[2,2,2,255],[8,8,8,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[4,4,4,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[4,4,4,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[8,8,8,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[12,12,12,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[6,6,6,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[2,2,2,255],[1,1,1,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[9,9,9,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[2,2,2,255],[3,3,3,255],[3,3,3,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[9,9,9,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[2,2,2,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(playico_array)):
    for j in range(len(playico_array[0])):
        playico_array[i][j] = [255,255,255,playico_array[i][j][3]]

array_np = np.array(playico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
play_icon = ImageTk.PhotoImage(image)

pauseico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[5,5,5,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[10,10,10,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[26,26,26,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[6,6,6,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(pauseico_array)):
    for j in range(len(pauseico_array[0])):
        pauseico_array[i][j] = [255,255,255,pauseico_array[i][j][3]]

array_np = np.array(pauseico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
pause_icon = ImageTk.PhotoImage(image)

stopico_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[6,6,6,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[9,9,9,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[8,8,8,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[3,3,3,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[3,3,3,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[7,7,7,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[5,5,5,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[17,17,17,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(stopico_array)):
    for j in range(len(stopico_array[0])):
        stopico_array[i][j] = [255,255,255,stopico_array[i][j][3]]

array_np = np.array(stopico_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
stop_icon = ImageTk.PhotoImage(image)


undo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[6,6,6,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[7,7,7,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[4,4,4,128],[0,0,0,255],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[3,3,3,255],[0,0,0,128],[2,2,2,128],[0,0,0,128],[6,6,6,128],[8,8,8,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[1,1,1,255],[9,9,9,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[4,4,4,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[2,2,2,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[6,6,6,128],[0,0,0,128],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[8,8,8,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[3,3,3,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[4,4,4,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(undo_array)):
    for j in range(len(undo_array[0])):
        undo_array[i][j] = [210,210,210,undo_array[i][j][3]]

array_np = np.array(undo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
undo_icon = ImageTk.PhotoImage(image)

undo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[6,6,6,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[7,7,7,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[4,4,4,128],[0,0,0,255],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[3,3,3,255],[0,0,0,128],[2,2,2,128],[0,0,0,128],[6,6,6,128],[8,8,8,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[1,1,1,255],[9,9,9,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[0,0,0,255],[1,1,1,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[4,4,4,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[2,2,2,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[1,1,1,255],[0,0,0,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[4,4,4,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[6,6,6,128],[0,0,0,128],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[1,1,1,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[6,6,6,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[8,8,8,255],[0,0,0,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[3,3,3,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[4,4,4,128],[0,0,0,128],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(undo_array)):
    for j in range(len(undo_array[0])):
        undo_array[i][j] = [255,255,255,undo_array[i][j][3]]

array_np = np.array(undo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
undo_icon_w = ImageTk.PhotoImage(image)

redo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[8,8,8,128],[6,6,6,128],[0,0,0,128],[6,6,6,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[2,2,2,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,255],[3,3,3,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[2,2,2,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,128],[6,6,6,128],[0,0,0,128],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[7,7,7,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[5,5,5,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[3,3,3,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,128],[6,6,6,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[28,28,28,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[4,4,4,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(redo_array)):
    for j in range(len(redo_array[0])):
        redo_array[i][j] = [210,210,210,redo_array[i][j][3]]

array_np = np.array(redo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
redo_icon = ImageTk.PhotoImage(image)

redo_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[8,8,8,128],[6,6,6,128],[0,0,0,128],[6,6,6,128],[2,2,2,128],[0,0,0,128],[0,0,0,128],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[2,2,2,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[2,2,2,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[2,2,2,255],[4,4,4,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[0,0,0,255],[3,3,3,255],[3,3,3,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[2,2,2,128],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,128],[0,0,0,128],[6,6,6,128],[0,0,0,128],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[5,5,5,255],[1,1,1,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[7,7,7,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[3,3,3,255],[2,2,2,255],[2,2,2,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[2,2,2,255],[1,1,1,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,2,2,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[2,2,2,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[4,4,4,128],[0,0,0,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[3,3,3,255],[0,0,0,255],[5,5,5,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[2,2,2,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[2,2,2,128],[1,1,1,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[4,4,4,255],[0,0,0,255],[2,2,2,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[1,1,1,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[3,3,3,255],[0,0,0,255],[5,5,5,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[3,3,3,255],[0,0,0,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,128],[0,0,0,128],[6,6,6,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[2,2,2,255],[4,4,4,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,255],[2,2,2,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[1,1,1,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[1,1,1,255],[3,3,3,255],[0,0,0,255],[2,2,2,255],[3,3,3,255],[2,2,2,255],[0,0,0,255],[28,28,28,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,128],[4,4,4,128],[0,0,0,255],[0,0,0,255],[0,0,0,255],[2,2,2,255],[20,20,20,128],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1],[4,4,4,128],[4,4,4,128],[0,0,0,128],[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(redo_array)):
    for j in range(len(redo_array[0])):
        redo_array[i][j] = [255,255,255,redo_array[i][j][3]]

array_np = np.array(redo_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
redo_icon_w = ImageTk.PhotoImage(image)

zoom_in_array = [[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_in_array)):
    for j in range(len(zoom_in_array[0])):
        zoom_in_array[i][j] = [210,210,210,255-zoom_in_array[i][j][0]]

array_np = np.array(zoom_in_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_in_icon = ImageTk.PhotoImage(image)

zoom_in_array = [[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_in_array)):
    for j in range(len(zoom_in_array[0])):
        zoom_in_array[i][j] = [255,255,255,255-zoom_in_array[i][j][0]]

array_np = np.array(zoom_in_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_in_icon_w = ImageTk.PhotoImage(image)

zoom_out_array =[[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_out_array)):
    for j in range(len(zoom_out_array[0])):
        zoom_out_array[i][j] = [210,210,210,255-zoom_out_array[i][j][0]]

array_np = np.array(zoom_out_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_out_icon = ImageTk.PhotoImage(image)

zoom_out_array =[[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[177,177,177,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[229,229,229,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[203,203,203,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[48,48,48,255],[48,48,48,255],[48,48,48,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(zoom_out_array)):
    for j in range(len(zoom_out_array[0])):
        zoom_out_array[i][j] = [255,255,255,255-zoom_out_array[i][j][0]]

array_np = np.array(zoom_out_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
zoom_out_icon_w = ImageTk.PhotoImage(image)


left_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(left_array)):
    for j in range(len(left_array[0])):
        left_array[i][j] = [210,210,210,left_array[i][j][3]]

array_np = np.array(left_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
left_icon = ImageTk.PhotoImage(image)

left_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[182,102,58,255],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,102,144,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[144,102,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,58,0,255],[0,0,0,255],[0,0,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(left_array)):
    for j in range(len(left_array[0])):
        left_array[i][j] = [255,255,255,left_array[i][j][3]]

array_np = np.array(left_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
left_icon_w = ImageTk.PhotoImage(image)


right_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(right_array)):
    for j in range(len(right_array[0])):
        right_array[i][j] = [210,210,210,right_array[i][j][3]]


array_np = np.array(right_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
right_icon = ImageTk.PhotoImage(image)


right_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[182,102,58,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[58,102,144,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,58,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,58,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[102,58,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[144,102,58,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[58,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,102,255],[0,0,0,255],[58,58,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[102,58,102,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(right_array)):
    for j in range(len(right_array[0])):
        right_array[i][j] = [255,255,255,right_array[i][j][3]]


array_np = np.array(right_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
right_icon_w = ImageTk.PhotoImage(image)

mic_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[91,91,91,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[84,84,84,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[46,46,46,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[51,51,51,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[46,46,46,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[36,36,36,255],[39,39,39,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[36,36,36,255],[36,36,36,255],[36,36,36,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(mic_array)):
    for j in range(len(mic_array[0])):
        mic_array[i][j] = [255,255,255,mic_array[i][j][3]]


array_np = np.array(mic_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
mic_icon = ImageTk.PhotoImage(image)

gun_array = [[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]],[[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0],[255,255,255,0]]]
for i in range(len(gun_array)):
    for j in range(len(gun_array[0])):
        gun_array[i][j] = [255,255,255,gun_array[i][j][3]]

array_np = np.array(gun_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
gun_icon = ImageTk.PhotoImage(image)

for i in range(len(gun_array)):
    for j in range(len(gun_array[0])):
        gun_array[i][j] = [255,0,0,gun_array[i][j][3]]

array_np = np.array(gun_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
red_gun_icon = ImageTk.PhotoImage(image)


start_array = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[55,55,55,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[108,108,108,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[8,8,8,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[76,76,76,255],[104,104,104,255],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[91,91,91,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[14,14,14,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[78,78,78,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[49,49,49,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,255],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
for i in range(len(start_array)):
    for j in range(len(start_array[0])):
        start_array[i][j] = [255,255,255,start_array[i][j][3]]

array_np = np.array(start_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
start_icon = ImageTk.PhotoImage(image)


sound_array = [[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[253,253,253],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[252,252,252],[254,254,254],[255,255,255],[250,250,250],[255,255,255],[255,255,255],[252,252,252],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[251,251,251],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[228,228,228],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[254,254,254],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[245,245,245],[255,255,255],[252,252,252],[252,252,252],[255,255,255],[251,251,251],[249,249,249],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[251,251,251],[255,255,255],[253,253,253],[253,253,253],[255,255,255],[253,253,253],[254,254,254],[200,200,200],[252,252,252],[255,255,255],[253,253,253],[255,255,255],[226,226,226],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[250,250,250],[255,255,255],[251,251,251],[255,255,255],[254,254,254],[244,244,244],[246,246,246],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[250,250,250],[255,255,255],[250,250,250],[219,219,219],[249,249,249],[249,249,249],[255,255,255],[247,247,247],[255,255,255],[219,219,219],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[205,205,205],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[254,254,254],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[251,251,251],[118,118,118],[255,255,255],[248,248,248],[255,255,255],[255,255,255],[177,177,177],[253,253,253],[255,255,255],[253,253,253],[250,250,250],[255,255,255],[250,250,250],[254,254,254],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[254,254,254],[208,208,208],[255,255,255],[253,253,253],[254,254,254],[255,255,255],[255,255,255],[183,183,183],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[173,173,173],[255,255,255],[253,253,253],[255,255,255],[254,254,254],[241,241,241],[250,250,250],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[252,252,252],[255,255,255],[255,255,255],[254,254,254],[253,253,253],[253,253,253],[252,252,252],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[109,109,109],[254,254,254],[255,255,255],[254,254,254],[253,253,253],[162,162,162],[253,253,253],[255,255,255],[255,255,255],[252,252,252],[197,197,197],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255]],[[255,255,255],[254,254,254],[253,253,253],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[43,43,43],[252,252,252],[255,255,255],[252,252,252],[254,254,254],[255,255,255],[253,253,253],[255,255,255],[254,254,254],[255,255,255],[238,238,238],[238,238,238],[254,254,254],[248,248,248],[255,255,255],[224,224,224],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255]],[[255,255,255],[253,253,253],[255,255,255],[255,255,255],[103,103,103],[251,251,251],[251,251,251],[253,253,253],[255,255,255],[251,251,251],[75,75,75],[255,255,255],[253,253,253],[255,255,255],[251,251,251],[133,133,133],[254,254,254],[255,255,255],[253,253,253],[254,254,254],[165,165,165],[255,255,255],[255,255,255],[255,255,255],[250,250,250],[244,244,244],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[254,254,254],[255,255,255]],[[250,250,250],[254,254,254],[255,255,255],[255,255,255],[252,252,252],[39,39,39],[255,255,255],[255,255,255],[251,251,251],[255,255,255],[42,42,42],[248,248,248],[255,255,255],[255,255,255],[253,253,253],[96,96,96],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[142,142,142],[255,255,255],[255,255,255],[250,250,250],[255,255,255],[221,221,221],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[201,201,201],[187,187,187],[252,252,252],[255,255,255],[255,255,255],[146,146,146],[68,68,68],[255,255,255],[255,255,255],[253,253,253],[102,102,102],[249,249,249],[255,255,255],[252,252,252],[255,255,255],[167,167,167],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[202,202,202],[252,252,252],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[249,249,249],[255,255,255],[253,253,253],[251,251,251],[252,252,252],[41,41,41],[251,251,251],[253,253,253],[252,252,252],[252,252,252],[45,45,45],[253,253,253],[251,251,251],[254,254,254],[156,156,156],[181,181,181],[255,255,255],[255,255,255],[255,255,255],[204,204,204],[253,253,253],[255,255,255],[251,251,251],[253,253,253],[197,197,197],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[247,247,247],[56,56,56],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[56,56,56],[250,250,250],[254,254,254],[253,253,253],[205,205,205],[123,123,123],[255,255,255],[253,253,253],[255,255,255],[232,232,232],[253,253,253],[255,255,255],[255,255,255],[254,254,254],[201,201,201],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[255,255,255],[254,254,254],[253,253,253],[255,255,255],[249,249,249],[51,51,51],[195,195,195],[253,253,253],[254,254,254],[255,255,255],[50,50,50],[254,254,254],[255,255,255],[253,253,253],[239,239,239],[104,104,104],[254,254,254],[255,255,255],[253,253,253],[244,244,244],[254,254,254],[253,253,253],[255,255,255],[254,254,254],[206,206,206],[255,255,255],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],[[255,255,255],[253,253,253],[255,255,255],[255,255,255],[253,253,253],[247,247,247],[49,49,49],[160,160,160],[253,253,253],[253,253,253],[255,255,255],[48,48,48],[255,255,255],[254,254,254],[255,255,255],[244,244,244],[100,100,100],[253,253,253],[251,251,251],[255,255,255],[249,249,249],[250,250,250],[255,255,255],[254,254,254],[255,255,255],[209,209,209],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[253,253,253]],[[253,253,253],[255,255,255],[255,255,255],[254,254,254],[249,249,249],[249,249,249],[50,50,50],[201,201,201],[251,251,251],[249,249,249],[249,249,249],[54,54,54],[254,254,254],[254,254,254],[251,251,251],[236,236,236],[101,101,101],[255,255,255],[255,255,255],[252,252,252],[245,245,245],[253,253,253],[255,255,255],[254,254,254],[253,253,253],[201,201,201],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[252,252,252],[255,255,255],[244,244,244],[253,253,253],[71,71,71],[248,248,248],[251,251,251],[254,254,254],[251,251,251],[56,56,56],[253,253,253],[255,255,255],[255,255,255],[200,200,200],[133,133,133],[253,253,253],[255,255,255],[255,255,255],[224,224,224],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[197,197,197],[255,255,255],[255,255,255],[255,255,255],[252,252,252],[255,255,255],[255,255,255]],[[252,252,252],[255,255,255],[255,255,255],[252,252,252],[255,255,255],[253,253,253],[33,33,33],[252,252,252],[255,255,255],[253,253,253],[244,244,244],[37,37,37],[255,255,255],[250,250,250],[251,251,251],[148,148,148],[197,197,197],[253,253,253],[254,254,254],[255,255,255],[197,197,197],[255,255,255],[252,252,252],[255,255,255],[255,255,255],[196,196,196],[254,254,254],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[255,255,255]],[[255,255,255],[250,250,250],[255,255,255],[255,255,255],[251,251,251],[124,124,124],[216,216,216],[252,252,252],[249,249,249],[250,250,250],[114,114,114],[94,94,94],[255,255,255],[255,255,255],[255,255,255],[92,92,92],[249,249,249],[255,255,255],[252,252,252],[250,250,250],[164,164,164],[255,255,255],[253,253,253],[255,255,255],[252,252,252],[206,206,206],[252,252,252],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254]],[[253,253,253],[254,254,254],[255,255,255],[254,254,254],[253,253,253],[51,51,51],[255,255,255],[250,250,250],[245,245,245],[250,250,250],[58,58,58],[246,246,246],[254,254,254],[253,253,253],[251,251,251],[96,96,96],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[137,137,137],[253,253,253],[255,255,255],[254,254,254],[255,255,255],[236,236,236],[255,255,255],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[255,255,255]],[[253,253,253],[255,255,255],[254,254,254],[255,255,255],[75,75,75],[255,255,255],[253,253,253],[251,251,251],[252,252,252],[229,229,229],[148,148,148],[252,252,252],[253,253,253],[254,254,254],[247,247,247],[168,168,168],[252,252,252],[253,253,253],[255,255,255],[250,250,250],[175,175,175],[252,252,252],[255,255,255],[254,254,254],[246,246,246],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[254,254,254],[253,253,253],[255,255,255]],[[255,255,255],[255,255,255],[254,254,254],[255,255,255],[253,253,253],[254,254,254],[248,248,248],[249,249,249],[254,254,254],[23,23,23],[241,241,241],[255,255,255],[246,246,246],[249,249,249],[238,238,238],[251,251,251],[253,253,253],[255,255,255],[255,255,255],[222,222,222],[254,254,254],[254,254,254],[254,254,254],[254,254,254],[214,214,214],[253,253,253],[252,252,252],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255]],[[254,254,254],[255,255,255],[255,255,255],[254,254,254],[252,252,252],[250,250,250],[251,251,251],[253,253,253],[255,255,255],[243,243,243],[255,255,255],[255,255,255],[245,245,245],[253,253,253],[96,96,96],[252,252,252],[254,254,254],[255,255,255],[254,254,254],[139,139,139],[255,255,255],[254,254,254],[252,252,252],[255,255,255],[204,204,204],[249,249,249],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[252,252,252],[252,252,252],[252,252,252],[252,252,252],[255,255,255],[249,249,249],[248,248,248],[254,254,254],[228,228,228],[255,255,255],[247,247,247],[251,251,251],[254,254,254],[253,253,253],[240,240,240],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[253,253,253],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[254,254,254],[254,254,254],[255,255,255]],[[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[252,252,252],[253,253,253],[250,250,250],[249,249,249],[255,255,255],[255,255,255],[188,188,188],[252,252,252],[251,251,251],[249,249,249],[254,254,254],[153,153,153],[253,253,253],[255,255,255],[252,252,252],[255,255,255],[250,250,250],[255,255,255],[252,252,252],[252,252,252],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253]],[[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[253,253,253],[247,247,247],[247,247,247],[255,255,255],[249,249,249],[200,200,200],[245,245,245],[253,253,253],[251,251,251],[252,252,252],[245,245,245],[250,250,250],[250,250,250],[250,250,250],[255,255,255],[254,254,254],[202,202,202],[251,251,251],[254,254,254],[255,255,255],[255,255,255],[251,251,251],[254,254,254],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[252,252,252],[250,250,250],[254,254,254],[253,253,253],[253,253,253],[255,255,255],[247,247,247],[249,249,249],[243,243,243],[249,249,249],[255,255,255],[254,254,254],[254,254,254],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[254,254,254],[253,253,253],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[251,251,251],[255,255,255],[250,250,250],[254,254,254],[255,255,255],[248,248,248],[254,254,254],[254,254,254],[248,248,248],[250,250,250],[250,250,250],[255,255,255],[251,251,251],[210,210,210],[255,255,255],[252,252,252],[252,252,252],[253,253,253],[255,255,255],[255,255,255],[255,255,255],[251,251,251],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[255,255,255],[249,249,249],[253,253,253],[255,255,255],[245,245,245],[255,255,255],[252,252,252],[254,254,254],[245,245,245],[254,254,254],[255,255,255],[246,246,246],[255,255,255],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[253,253,253],[255,255,255],[254,254,254],[255,255,255]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[255,255,255],[253,253,253],[251,251,251],[250,250,250],[255,255,255],[248,248,248],[252,252,252],[253,253,253],[248,248,248],[255,255,255],[253,253,253],[239,239,239],[251,251,251],[253,253,253],[255,255,255],[251,251,251],[255,255,255],[255,255,255],[254,254,254],[255,255,255],[255,255,255],[254,254,254]],[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]]]

for i in range(len(sound_array)):
    for j in range(len(sound_array[0])):
        sound_array[i][j] = [255,255,255,255-sound_array[i][j][0]]



array_np = np.array(sound_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
sound_icon = ImageTk.PhotoImage(image)



wind_array =[[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[239,239,239,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[53,53,53,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[230,230,230,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[224,224,224,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[39,39,39,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[230,230,230,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[170,170,170,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[128,128,128,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[89,89,89,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[128,128,128,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[53,53,53,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[153,153,153,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[201,201,201,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[209,209,209,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[246,246,246,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[251,251,251,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[235,235,235,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[128,128,128,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[159,159,159,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[195,195,195,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[224,224,224,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]],[[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[31,31,31,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[0,0,0,255],[136,136,136,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]]

for i in range(len(wind_array)):
    for j in range(len(wind_array[0])):
        wind_array[i][j] = [255,255,255,255-wind_array[i][j][0]]



array_np = np.array(wind_array, dtype=np.uint8)
image = Image.fromarray(array_np, 'RGBA')
wind_icon = ImageTk.PhotoImage(image)


"""
opticon = Image.open('images/options.ico')
iconopt = ImageTk.PhotoImage(opticon)

resultico = Image.open('images/results.ico')
resultpic = ImageTk.PhotoImage(resultico)

backwardico = Image.open('images/backward.ico')
backwardpic = ImageTk.PhotoImage(backwardico)
forwardico = Image.open('images/forward.ico')
forwardpic = ImageTk.PhotoImage(forwardico)
addcursorico = Image.open('images/add_cursor.ico')
addcursorpic = ImageTk.PhotoImage(addcursorico)
addcursorokico = Image.open('images/add_cursor_ok.ico')
addcursorokpic = ImageTk.PhotoImage(addcursorokico)
plusico = Image.open('images/plus.ico')
pluspic = ImageTk.PhotoImage(plusico)
minusico = Image.open('images/minus.ico')
minuspic = ImageTk.PhotoImage(minusico)
startico = Image.open('images/start.ico')
startpic = ImageTk.PhotoImage(startico)
editico = Image.open('images/edit.ico').resize((20, 20))
editpic = ImageTk.PhotoImage(editico)
crossico = Image.open('images/cross.ico').resize((20, 20))
crosspic = ImageTk.PhotoImage(crossico)
okico = Image.open('images/ok.ico').resize((20, 20))
okpic = ImageTk.PhotoImage(okico)
"""
#icon = Image.open('images/icon.ico')
#iconbg = ImageTk.PhotoImage(icon)
#root.state("zoomed")
root.resizable(False,False)
root.geometry(f'{window_width}x{window_height}+{99999}+{99999}')
#root.iconphoto(False,main_icon)
root.deiconify()
total_instances = 0
def create_instance():
    global total_instances
    total_instances += 1
    video_recorder = Instance(root)
    video_recorder.root.mainloop()
#tk.Button(text = "Create Instance", command = create_instance).place(x=0,y = 0, anchor = "nw")

create_instance()
root.mainloop()

