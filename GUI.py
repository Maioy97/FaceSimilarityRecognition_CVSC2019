import tkinter as tk
import tkinter.messagebox , tkinter.filedialog
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import os


class Person:
    name = ""
    age = 0
    phone = "04564688864"
    gender = "female"

    def __init__(self, name, age, phone, gender):
        self.name = name
        self.age = age
        self.phone = phone
        self.gender= gender


class GUI:
    window = tk.Tk()
    module = None
    txtbx_name = None
    txtbx_age = None
    txtbx_phone = None
    txtbx_gender = None
    chbttn_sketch= None
    selection = None
    bttn_showlist = None
    bttn_nextmatch = None
    bttn_compare = None
    bttn_chooseimage = None
    image_static = None
    image_result = None
    lbl_val_name = None
    lbl_val_age = None
    lbl_val_phone = None
    lbl_val_gender = None


    res_name = tk.StringVar()
    res_age = tk.IntVar()
    res_phone = tk.StringVar()
    res_gender = tk.StringVar()

    res_list = None
    res_index = 0

    person_name = tk.StringVar()
    person_age = tk.IntVar()
    person_phone = tk.StringVar()
    person_gender = tk.StringVar()
    sketch = tk.IntVar()
    x_left_col = 25
    x_right_col = 500
    size = 265
    y_row0 = 25
    y_row1 = y_row0 + size + 25
    y_row2 = y_row1 + 50
    y_row3 = y_row2 + 50
    y_row4 = y_row3 + 50
    xspace = 150

    def __init__(self):
        self.setup()
        self.show()

    def bttn_choose_image_onclick(self, a):
        currdir = os.getcwd()
        tempdir = tk.filedialog.askopenfile(parent=self.window, initialdir=currdir, title='Please select a directory')
        if len(tempdir.name) > 0:
            opened = Image.open(tempdir.name)
            render = ImageTk.PhotoImage(opened.resize((self.size, self.size)))
            if render is not None:
                self.image_static.configure(image = render)
                self.image_static.image = render
                return
            else:
                msg = tk.messagebox.showinfo("invalid image path")

    def bttn_next_onclick(self, a):
        current_res = self.res_list[self.res_index]
        temp = Person()

        print("warning: next no click not done yet")
        # retrieve res with given id from database
        # this syntax should be changed to match
        self.res_phone.set(temp.phone)
        self.res_age.set(temp.age)
        self. res_gender.set(temp.gender)
        self. res_name.set(temp.name)

    def bttn_start_onclick(self, a):
        # check which classes and features are selected
        shapes_list = []
        l_numOfEpochs = int(self.numOfEpochs.get())
        l_bias = int(self.bias.get())
        l_rate = float(self.rate.get())
        l_shapes_string = self.layershapes.get()
        l_shapes_string = l_shapes_string.split(',')
        l_functionnum = self.functionNum.get()
        l_numoflayers = self.numOfLayers.get()
        if l_numoflayers == len(l_shapes_string):
            if l_numOfEpochs > 0:
                for shape in l_shapes_string:
                    r = int(shape)
                    shapes_list.append(r)

                self.module = classification.BackPropagation(l_numoflayers, shapes_list, l_bias)
                # call read data with said classes and features
                x1features, x2features, x3features, x4features, labels = self.read_data()

                # organise data : divide it into train and test data
                x1features = np.array(x1features)
                tr_x1, ts_1 = x1features[0:30], x1features[30:50]
                tr_x1, ts_1 = np.append(tr_x1, x1features[50:80]), np.append(ts_1, x1features[80:100])
                tr_x1, ts_1 = np.append(tr_x1, x1features[100:130]), np.append(ts_1, x1features[130:150])

                x2features = np.array(x2features)
                tr_x2, ts_2 = x2features[0:30], x2features[30:50]
                tr_x2, ts_2 = np.append(tr_x2, x2features[50:80]), np.append(ts_2, x2features[80:100])
                tr_x2, ts_2 = np.append(tr_x2, x1features[100:130]), np.append(ts_2, x2features[130:150])

                x3features = np.array(x3features)
                tr_x3, ts_3 = x3features[0:30], x3features[30:50]
                tr_x3, ts_3 = np.append(tr_x3, x3features[50:80]), np.append(ts_3, x3features[80:100])
                tr_x3, ts_3 = np.append(tr_x3, x3features[100:130]), np.append(ts_3, x3features[130:150])

                x4features = np.array(x4features)
                tr_x4, ts_4 = x4features[0:30], x4features[30:50]
                tr_x4, ts_4 = np.append(tr_x4, x4features[50:80]), np.append(ts_4, x4features[80:100])
                tr_x4, ts_4 = np.append(tr_x4, x4features[100:130]), np.append(ts_4, x4features[130:150])

                labels = np.array(labels)
                train_labels = labels[0:30, :], labels[50:80, :], labels[130:150, :]
                train_labels, test_labels = labels[0:30, :], labels[30:50, :]
                train_labels, test_labels = np.append(train_labels, labels[50:80, :], axis=0),\
                                            np.append(test_labels, labels[80:100, :], axis=0)
                train_labels, test_labels = np.append(train_labels, labels[100:130, :], axis=0),\
                                            np.append(test_labels, labels[130:150, :], axis=0)

                # -------------------------
                self.module.train(train_labels, l_numOfEpochs, tr_x1, tr_x2, tr_x3, tr_x4, l_rate, l_functionnum)
                # call test and output the percentage
                confusion_mat, error = self.module.test(test_labels, ts_1, ts_2, ts_3, ts_4)
                # show accuracy
                accuracy = (1 - error)*100
                msg_str = 'model is ,', accuracy, ' % accurate'
                msg = tk.messagebox.showinfo("model accuracy", msg_str)
                print(confusion_mat)
            else:
                stri = "number of epochs can't be 0"
                msg = tk.messagebox.showinfo("layer specifics", stri)
        else:
            strx = "number of layer and layer neurons per layer don't match , please fix it and try again"
            msg = tk.messagebox.showinfo("layer specifics", strx)

    def setup(self):
        space = self.xspace
        self.window.geometry("850x550")

        load = Image.open("34AD2.jpg").resize((256, 256))
        render = ImageTk.PhotoImage(load)
        self.image_static = tk.Label(self.window, image=render)
        self.image_static.image = render
        self.image_static.place(x=self.x_left_col, y=self.y_row0)

        self.bttn_chooseimage = tk.Button(self.window, text="Browse")
        self.bttn_chooseimage.place(x=self.x_left_col + self.size, y=self.y_row0 + self.size)

        # supossed to browse and change the image displayed
        self.bttn_chooseimage.bind("<Button-1>", self.bttn_choose_image_onclick)

        lbl_lost_name = tk.Label(self.window, text="Name")
        lbl_lost_name.place(x=self.x_left_col, y=self.y_row1)

        self.txtbx_name = tk.Entry(self.window, textvariable=self.person_name)
        self.txtbx_name.place(x=self.x_left_col, y=self.y_row1 + 25)

        lbl_lost_age = tk.Label(self.window, text="Age")
        lbl_lost_age.place(x=self.x_left_col + space, y=self.y_row1)

        self.txtbx_age = tk.Entry(self.window, textvariable=self.person_age)
        self.txtbx_age.place(x=self.x_left_col + space, y=self.y_row1 + 25)

        lbl_lost_gender = tk.Label(self.window, text="Gender")
        lbl_lost_gender.place(x=self.x_left_col, y=self.y_row2)
        self.txtbx_gender = tk.Entry(self.window, textvariable=self.person_gender)
        self.txtbx_gender.place(x=self.x_left_col, y=self.y_row2 + 25)

        lbl_lost_phone = tk.Label(self.window, text="Contact phone number")
        lbl_lost_phone.place(x=self.x_left_col + space, y=self.y_row2)
        self.txtbx_phone = tk.Entry(self.window, textvariable=self.person_phone)
        self.txtbx_phone.place(x=self.x_left_col + space, y=self.y_row2 + 25)

        lbl_sketch = tk.Label(self.window, text="Sketch?")
        lbl_sketch.place(x=self.x_left_col, y=self.y_row3)

        self.chbttn_sketch = tk.Checkbutton(self.window, variable=self.sketch)
        self.chbttn_sketch.place(x=self.x_left_col + 50, y=self.y_row3)

        # right side ----------------------------
        load = Image.open("34AD2.jpg").resize((256, 256))
        render = ImageTk.PhotoImage(load)
        self.image_result = tk.Label(self.window, image=render)
        self.image_result.image = render
        self.image_result.place(x=self.x_right_col, y=self.y_row0)

        lbl_res_name = tk.Label(self.window, text="Name")
        lbl_res_name.place(x=self.x_right_col, y=self.y_row1)

        self.lbl_val_name = tk.Label(self.window, textvariable=self.res_name)
        self.lbl_val_name.place(x=self.x_right_col, y=self.y_row1 + 25)

        lbl_res_age = tk.Label(self.window, text="Age")
        lbl_res_age.place(x=self.x_right_col + space, y=self.y_row1)

        self.lbl_val_age = tk.Label(self.window, textvariable=self.res_age)
        self.lbl_val_age.place(x=self.x_right_col + space, y=self.y_row1 + 25)

        lbl_res_gender = tk.Label(self.window, text="Gender")
        lbl_res_gender.place(x=self.x_right_col, y=self.y_row2)
        self.lbl_val_gender = tk.Label(self.window, textvariable=self.res_gender)
        self.lbl_val_gender.place(x=self.x_right_col, y=self.y_row2 + 25)

        lbl_res_phone = tk.Label(self.window, text="Contact phone number")
        lbl_res_phone.place(x=self.x_right_col + space, y=self.y_row2)
        self.lbl_val_phone = tk.Label(self.window, textvariable=self.res_phone)
        self.lbl_val_phone.place(x=self.x_right_col + space, y=self.y_row2 + 25)

        self.res_phone.set("055484654654")


        # lower part ----------------------------
        bttn_next = tk.Button(self.window, text="Next")
        bttn_next.place(x=self.x_right_col, y=self.y_row4)
        bttn_next.bind("<Button-1>", self.bttn_next_onclick)  # <Button-1> = left click

        bttn_start = tk.Button(self.window, text="start")
        bttn_start.place(x=self.x_left_col, y=self.y_row4)
        bttn_start.bind("<Button-1>", self.bttn_start_onclick)  # <Button-1> = left click

    def show(self):
        self.window.mainloop()

window = GUI()
