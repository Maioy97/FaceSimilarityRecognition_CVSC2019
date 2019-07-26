import tkinter as tk
import tkinter.messagebox
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import os
# from task3_backpropagation import classification


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

    def bttn_choose_image_onclick(self):
        currdir = os.getcwd()
        tempdir = tk.tkFileDialog.askdirectory(parent=self.window, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            image = Image.open(tempdir)
            if image is not None:
                self.image_static.image = ImageTk.PhotoImage(image.resize((self.size, self.size)))
                return
            else:
                msg = tk.messagebox.showinfo("model accuracy", "invalid image path")

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
        self.bttn_chooseimage.place(x=self.x_left_col +self.size, y=self.y_row0+self.size)

        # supossed to browse and change the image displayed
        self.bttn_chooseimage.bind("<Button-1>", self.bttn_choose_image_onclick)

        lbl_lost_name = tk.Label(self.window, text="Name")
        lbl_lost_name.place(x=self.x_left_col, y=self.y_row1)

        self.txtbx_name = tk.Entry(self.window, textvariable=self.person_name)
        self.txtbx_name.place(x=self.x_left_col, y=self.y_row1+25)

        lbl_lost_age = tk.Label(self.window, text="Age")
        lbl_lost_age.place(x=self.x_left_col+space, y=self.y_row1)

        self.txtbx_age = tk.Entry(self.window, textvariable=self.person_age)
        self.txtbx_age.place(x=self.x_left_col+space, y=self.y_row1+25)

        lbl_lost_gender = tk.Label(self.window, text="Gender")
        lbl_lost_gender.place(x=self.x_left_col, y=self.y_row2)
        self.txtbx_gender = tk.Entry(self.window, textvariable=self.person_gender)
        self.txtbx_gender.place(x=self.x_left_col, y=self.y_row2+25)

        lbl_lost_phone = tk.Label(self.window, text="Contact phone number")
        lbl_lost_phone.place(x=self.x_left_col+space, y=self.y_row2)
        self.txtbx_phone = tk.Entry(self.window, textvariable=self.person_phone)
        self.txtbx_phone.place(x=self.x_left_col+space, y=self.y_row2+25)

        lbl_sketch = tk.Label(self.window, text="Sketch?")
        lbl_sketch.place(x=self.x_left_col, y=self.y_row3)

        self.chbttn_sketch = tk.Checkbutton(self.window, variable=self.sketch)
        self.chbttn_sketch.place(x=self.x_left_col+50, y=self.y_row3)

        # right side ----------------------------
        load = Image.open("34AD2.jpg").resize((256, 256))
        render = ImageTk.PhotoImage(load)
        self.image_static = tk.Label(self.window, image=render)
        self.image_static.image = render
        self.image_static.place(x=self.x_right_col, y=self.y_row0)

        lbl_lost_name = tk.Label(self.window, text="Name")
        lbl_lost_name.place(x=self.x_right_col, y=self.y_row1)

        self.txtbx_name = tk.Entry(self.window, textvariable=self.person_name)
        self.txtbx_name.place(x=self.x_right_col, y=self.y_row1+25)

        lbl_lost_age = tk.Label(self.window, text="Age")
        lbl_lost_age.place(x=self.x_right_col+space, y=self.y_row1)

        self.txtbx_age = tk.Entry(self.window, textvariable=self.person_age)
        self.txtbx_age.place(x=self.x_right_col+space, y=self.y_row1+25)

        lbl_lost_gender = tk.Label(self.window, text="Gender")
        lbl_lost_gender.place(x=self.x_right_col, y=self.y_row2)
        self.txtbx_gender = tk.Entry(self.window, textvariable=self.person_gender)
        self.txtbx_gender.place(x=self.x_right_col, y=self.y_row2+25)

        lbl_lost_phone = tk.Label(self.window, text="Contact phone number")
        lbl_lost_phone.place(x=self.x_right_col+space, y=self.y_row2)
        self.txtbx_phone = tk.Entry(self.window, textvariable=self.person_phone)
        self.txtbx_phone.place(x=self.x_right_col+space, y=self.y_row2+25)



        # lower part ----------------------------
        bttn_start = tk.Button(self.window, text="Next")
        bttn_start.place(x=self.x_right_col, y=self.y_row4)

        bttn_start = tk.Button(self.window, text="start")
        bttn_start.place(x=self.x_left_col, y=self.y_row4)
        bttn_start.bind("<Button-1>", self.bttn_start_onclick)  # <Button-1> = left click

    def show(self):
        self.window.mainloop()

    @staticmethod
    def plot_class_(feature_num, feature1, feature2, decision_line, class_names):
        # for the showing output
        plt.figure(class_names[0] + " vs " + class_names[1])
        plt.xlabel('X%d' % (feature_num[0] + 1))
        plt.ylabel('X%d' % (feature_num[1] + 1))
        x = np.array(feature1)
        y = np.array(feature2)
        plt.scatter(x[0:50], y[0:50])
        plt.scatter(x[50:100], y[50:100])
        print(decision_line)
        plt.plot([decision_line[0][1], decision_line[1][1]], [decision_line[0][0], decision_line[1][0]])
        # consists of two points x1 x2 y1 y2

        plt.show()

    def plot_class(self, features1, features2):
        # for the first part of the task
        # will be called 6 times
        x, y, labels, class_names = self.read_data(GUI, features1, features2)
        plt.figure(class_names[0]+" vs "+class_names[1]+" vs "+class_names[2])
        plt.xlabel('X%d' % (features1 + 1))
        plt.ylabel('X%d' % (features2 + 1))
        x = np.array(x)
        y = np.array(y)
        plt.scatter(x[0:50], y[0:50])
        plt.scatter(x[50:100], y[50:100])
        plt.scatter(x[100:150], y[100:150])

        plt.show()

    @staticmethod
    def read_data_(class1, class2, features1, features2):

        # reads data based on class number and feature number
        # reads selected features starting at row classnumber*50 till row class number*50+50
        Xfeatures = []
        Yfeatures = []
        labels = []

        fp = open('IrisData.txt')  # Open file on read mode
        lines = fp.read().split("\n")  # Create a list containing all lines
        fp.close()  # Close file
        class_names = ['', '']
        start = class1*50+1   # since line 1 is table labels
        end = start+50
        line = lines[start].split(',')
        class_names[0] = line[4]
        for i in range(start, end):
            line = lines[i].split(',')
            Xfeatures.append(float(line[features1]))
            Yfeatures.append(float(line[features2]))
            labels.append(1)

        start = class2 * 50+1
        end = start + 50
        line = lines[start].split(',')
        class_names[1] = line[4]
        for i in range(start, end):
            line = lines[i].split(',')
            Xfeatures.append(float(line[features1]))
            Yfeatures.append(float(line[features2]))
            labels.append(-1)

        return Xfeatures, Yfeatures, labels, class_names

    @staticmethod
    def read_data():
        # reads all data (all classes)
        X1features = []
        X2features = []
        X3features = []
        X4features = []
        labels = []

        fp = open('IrisData.txt')  # Open file on read mode
        lines = fp.read().split("\n")  # Create a list containing all lines
        fp.close()  # Close file
        for line in lines:
            line = line.split(',')
            if line[0] == "X1":
                continue
            X1features.append(float(line[0]))
            X2features.append(float(line[1]))
            X3features.append(float(line[2]))
            X4features.append(float(line[3]))
            if line[4] == "Iris-setosa":
                labels.append([1, 0, 0])
            elif line[4] == "Iris-versicolor":
                labels.append([0, 1, 0])
            elif line[4] == "Iris-virginica":
                labels.append([0, 0, 1])
        return X1features, X2features, X3features, X4features, labels


def test_training_only():
    bias = 1
    mod = classification.tr()
    x1features, x2features, labels, class_names = GUI.read_data_(GUI, 0, 1, 0, 1)
    # organise data : divide it into train and test data
    x1features = np.array(x1features).astype(float)

    tr_x1 = np.array(x1features[0:31])   # .astype(float))
    tr_x1 = np.append(tr_x1, x1features[50:81])  # .astype(float))

    ts_1 = np.array(x1features[31:50].astype(float))
    ts_1 = np.append(ts_1, x1features[81::].astype(float))

    x2features = np.array(x2features).astype(float)
    tr_x2 = np.array(x2features[0:31].astype(float))
    tr_x2 = np.append(tr_x2, x2features[50:81].astype(float))

    ts_2 = np.array(x2features[31:50].astype(float))
    ts_2 = np.append(ts_2, x2features[81::].astype(float))

    labels = np.array(labels).astype(int)
    train_labels = np.array(labels[0:31].astype(int))
    train_labels = np.append(train_labels, labels[50:81].astype(int))

    test_labels = np.array(labels[31:50].astype(int))
    test_labels = np.append(test_labels, labels[81::].astype(int))

    weights = mod.train(train_labels, 50, bias, tr_x1, tr_x2, .2)
    print("weight:", weights)
    # get line points
    decision_line = []
    x = x2features[0]
    y = (-weights[0] * x - 1) / weights[1]
    decision_line.append((x, y))
    x = x2features[50]
    y = (-weights[0] * x - bias) / weights[1]
    decision_line.append((x, y))
    # output graph (decision boundary visible)
    feature1 = 0
    feature2 = 1
    GUI.plot_class_(GUI,[feature1, feature2], x1features, x2features, decision_line, class_names)
    # call test and output the percentage
    conmat, error = mod.test(test_labels, ts_1, ts_2)
    # show accuracy
    accuracy = (1 - error) * 100
    msg_str = "model is %d % accurate", accuracy
    msg = tk.messagebox.showinfo("model accuracy", msg_str)
    print(conmat)


#  test_training_only()
window = GUI()
