import tkinter as tk
import tkinter.messagebox, tkinter.filedialog
from datetime import date
from PIL import Image, ImageTk
import requests
import os
import base64
from io import StringIO
import numpy as np
import json

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

    txtbx_name = None
    txtbx_age = None
    txtbx_phone = None
    txtbx_gender = None
    txtbx_note = None
    txtbx_place = None

    chbttn_sketch = None
    chbttn_add_photo = None
    radio_lost = None
    radio_found = None
    radio_male = None
    radio_female = None

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
    lbl_val_note = None
    lbl_val_place = None
    threshold = 0 #max number of matches to display

    res_name = tk.StringVar()
    res_age = tk.IntVar()
    res_phone = tk.StringVar()
    res_gender = tk.StringVar()
    res_note = tk.StringVar()
    res_place = tk.StringVar()

    res_list = None
    res_index = 0

    person_name = tk.StringVar()
    person_age = tk.IntVar()
    person_phone = tk.StringVar()
    person_radio_gender = tk.StringVar()
    person_note = tk.StringVar()
    person_place = tk.StringVar()
    person_radio_lost = tk.StringVar()

    sketch = tk.IntVar()
    add_photo = tk.IntVar()
    x_left_col = 25
    x_right_col = 560
    size = 265
    y_row0 = 25
    y_row1 = y_row0 + size + 25
    y_row2 = y_row1 + 50
    y_row3 = y_row2 + 50
    y_row4 = y_row3 + 50
    xspace = 150
    bttn_size = 50
    bgcolor = "white"
    current_image= None

    Person_id = 3
    List = 'found'
    addpersonURL =  'http://192.168.1.22:5021/Addperson/'
    addphotoURL = 'http://192.168.1.22:5021/addPhoto/'
    get_similar_peopleURL = 'http://192.168.1.22:5021/get_similar_people/'
    get_infoURL = 'http://192.168.1.22:5021/get_info/'

    #addPhotoURL =  + str(Person_id) + '/' + List
    #get_similar_peopleURL = 'http://localhost:8000/get_similar_people/' + str(Person_id) + '/' + List

    def __init__(self):
        self.setup()
        self.show()

    def fillUI(self, lost_one_data):
        current_date = date.today()
        d1 = current_date.strftime("%d/%m/%Y")
        year = d1.split("/")
        year = int(year[-1])
        #msg = tk.messagebox.showinfo("data",lost_one_data[:100])
        data0 = json.loads(lost_one_data)
        data = json.loads(data0)
        birth_year = int(data["birth_year"])

        self.res_name.set(data["name"])
        self.res_age.set(year - birth_year)
        self.res_place.set(data["found_lost_place"])
        self.res_phone.set(data["contact_number"])
        self.res_gender.set(data["gender"])
        self.res_note.set(data["notes"])
        imgS_str = data["image"]
        image_ext = data["image_ext"]
        fh = open("temp." + image_ext, "wb")
        fh.write(base64.b64decode(imgS_str))
        fh.close()
        opened = Image.open("temp."+image_ext)
        render = ImageTk.PhotoImage(opened.resize((self.size, self.size)))
        if render is not None:
            self.image_result.configure(image=render)
            self.image_result.image = render
            return

    def bttn_choose_image_onclick(self, a):
        currdir = os.getcwd()
        tempdir = tk.filedialog.askopenfile(parent=self.window, initialdir=currdir, title='Please select a directory')
        self.current_image = tempdir.name

        if len(self.current_image) > 0:
            opened = Image.open(self.current_image)
            render = ImageTk.PhotoImage(opened.resize((self.size, self.size)))
            if render is not None:
                self.image_static.configure(image=render)
                self.image_static.image = render
                return
            else:
                msg = tk.messagebox.showinfo("invalid image path")

    def bttn_next_onclick(self, a):
        if self.res_index > 0 :
            if self.res_index<self.threshold:
                newURL = self.get_infoURL + self.res_list[self.res_index].replace(' ', '')
                info = requests.post(newURL).text
                self.res_index = self.res_index + 1
                self.fillUI(info)
            else:
                msg = tk.messagebox.showinfo("no Next found" ,"no more matches")
        else:
            msg = tk.messagebox.showinfo("no Next found" ,"please use Match first")


    def bttn_start_onclick(self, a):
        lost_one_data = {}
        AddpersonURL = self.addpersonURL + self.person_radio_lost.get()

        current_date = date.today()
        d1 = current_date.strftime("%d/%m/%Y")
        year = d1.split("/")
        year = int(year[-1])
        birth_year = year - int(self.person_age.get())
        if self.current_image is None:
            msg = tk.messagebox.showinfo("data not ready","please select a photo first")
            return
        Person_id = None
        img_str = None

        with open(self.current_image, "rb") as imageFile:
            img_str = base64.b64encode(imageFile.read())
        split = self.current_image.split('.')


        if not self.add_photo.get():
            lost_one_data["name"] = self.person_name.get()
            lost_one_data["birth_year"] = birth_year
            lost_one_data["lost_found_date"] = current_date
            lost_one_data["sketch"] = self.sketch.get()
            lost_one_data["found_lost_place"] = self.person_place.get()
            lost_one_data["contact_number"] = self.person_phone.get()
            lost_one_data["gender"] = self.person_radio_gender.get()
            lost_one_data["notes"] = self.person_note.get()
            lost_one_data["image"] = img_str
            lost_one_data["image_ext"] = split[-1]

            Person_id = requests.post(AddpersonURL, data=lost_one_data).text
            msg = tk.messagebox.showinfo("id recived",
                                         "your id is : " + Person_id+
                                         "\nplease insert it in case you want to add more images of the same person and retry the search")

        else:
            Person_id = self.person_name.get()
            newURL = self.addphotoURL + Person_id + '/' + self.person_radio_lost.get()
            lost_one_data["image"] = img_str
            lost_one_data["image_ext"] = split[-1]
            requests.post(newURL, lost_one_data)

        newURL = self.get_similar_peopleURL + Person_id + '/'+ self.person_radio_lost.get()
         
        # call the function that returns json using res_list[0]
        list_result = requests.post(newURL).text
        if list_result.replace('"','').replace('\n','') == "no matches after age and gender filtering":
            msg = tk.messagebox.showinfo("no match","no matches after age and gender filtering")
        else:
            s = StringIO(list_result[1:len(list_result) - 2].replace('\n', '').replace('"', ''))
            #msg = tk.messagebox.showinfo("list",list_result[1:len(list_result) - 2])
            self.res_list = np.genfromtxt(s,delimiter =',',dtype ='str', skip_header=False)
            self.threshold = len(self.res_list)
            #msg = tk.messagebox.showinfo("list",str(self.res_list[0]))
            newURL = self.get_infoURL + self.res_list[self.res_index].replace(' ', '')

            #msg = tk.messagebox.showinfo("list",newURL)
            info = requests.post(newURL).text

            self.res_index = 1
            self.fillUI(info)

    def setup(self):
        darkblue = "#a0c2ff"
        self.window.configure(background=self.bgcolor)
        self.window.tk_setPalette(background='white', foreground='black',
                           activeBackground='grey', activeForeground='black')
        btnsize = self.bttn_size
        space = self.xspace
        self.window.geometry("900x550")
        midcol = x=self.x_left_col + self.size +25

        load = Image.open("logo.png").resize((256, 256))
        render = ImageTk.PhotoImage(load)
        self.image_static = tk.Label(self.window, image=render)
        self.image_static.image = render
        self.image_static.place(x=self.x_left_col, y=self.y_row0)

        self.bttn_chooseimage = tk.Button(self.window, text="Browse", bg=darkblue)
        self.bttn_chooseimage.place(x=midcol, y=self.y_row0)
        # supossed to browse and change the image displayed
        self.bttn_chooseimage.bind("<Button-1>", self.bttn_choose_image_onclick)

        lbl_lostfound = tk.Label(self.window, text="Person is:")
        lbl_lostfound.place(x=midcol, y=self.y_row0+50)
        self.radio_lost = tk.Radiobutton(self.window, text="Lost", variable=self.person_radio_lost, value='lost')
        self.radio_lost.place(x=midcol, y=self.y_row0+75)
        self.radio_found = tk.Radiobutton(self.window, text="Found", variable=self.person_radio_lost, value='found')
        self.radio_found.place(x=midcol, y=self.y_row0+100)


        lbl_lost_name = tk.Label(self.window, text="Name")
        lbl_lost_name.place(x=self.x_left_col, y=self.y_row1)

        self.txtbx_name = tk.Entry(self.window, textvariable=self.person_name)
        self.txtbx_name.place(x=self.x_left_col, y=self.y_row1 + 25)

        lbl_lost_age = tk.Label(self.window, text="Age")
        lbl_lost_age.place(x=self.x_left_col + space, y=self.y_row1)

        self.txtbx_age = tk.Entry(self.window, textvariable=self.person_age)
        self.txtbx_age.place(x=self.x_left_col + space, y=self.y_row1 + 25)

        lbl_place = tk.Label(self.window, text="Place")
        lbl_place.place(x=self.x_left_col, y=self.y_row2)
        self.txtbx_place = tk.Entry(self.window, textvariable=self.person_place)
        self.txtbx_place.place(x=self.x_left_col, y=self.y_row2 + 25)

        lbl_lost_phone = tk.Label(self.window, text="Contact phone number")
        lbl_lost_phone.place(x=self.x_left_col + space, y=self.y_row2)
        self.txtbx_phone = tk.Entry(self.window, textvariable=self.person_phone)
        self.txtbx_phone.place(x=self.x_left_col + space, y=self.y_row2 + 25)

        lbl_lost_gender = tk.Label(self.window, text="Gender")
        lbl_lost_gender.place(x=self.x_left_col, y=self.y_row3)
        # self.txtbx_gender = tk.Entry(self.window, textvariable=self.person_gender)
        # self.txtbx_gender.place(x=self.x_left_col, y=self.y_row2 + 25)
        self.radio_male = tk.Radiobutton(self.window, text="Male", variable=self.person_radio_gender, value="M")
        self.radio_male.place(x=self.x_left_col, y=self.y_row3 + 25)#x=self.x_left_col, y=self.y_row3 + 25
        self.radio_female = tk.Radiobutton(self.window, text="Female", variable=self.person_radio_gender, value="F")
        self.radio_female.place(x=self.x_left_col + 50, y=self.y_row3 + 25)

        lbl_notes = tk.Label(self.window, text="Notes")
        lbl_notes.place(x=self.x_left_col + space, y=self.y_row3)
        self.txtbx_note = tk.Entry(self.window, textvariable=self.person_note)
        self.txtbx_note.place(x=self.x_left_col + space, y=self.y_row3 + 25)

        lbl_sketch = tk.Label(self.window, text="Sketch?")
        lbl_sketch.place(x=self.x_left_col, y=self.y_row4)
        self.chbttn_sketch = tk.Checkbutton(self.window, variable=self.sketch)
        self.chbttn_sketch.place(x=self.x_left_col + 50, y=self.y_row4)

        lbl_chbttn_add_photo = tk.Label(self.window, text="Add photo?")
        lbl_chbttn_add_photo.place(x=self.x_left_col + 150, y=self.y_row4)
        self.chbttn_add_photo = tk.Checkbutton(self.window, variable=self.add_photo)
        self.chbttn_add_photo.place(x=self.x_left_col + 250, y=self.y_row4)

        # right side ----------------------------
        load = Image.open("names.jpg").resize((256, 256))
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

        lbl_res_place = tk.Label(self.window, text="Place")
        lbl_res_place.place(x=self.x_right_col, y=self.y_row3)
        self.lbl_val_place = tk.Label(self.window, textvariable=self.res_place)
        self.lbl_val_place.place(x=self.x_right_col, y=self.y_row3 + 25)

        lbl_res_notes = tk.Label(self.window, text="Notes")
        lbl_res_notes.place(x=self.x_right_col + space, y=self.y_row3)
        self.lbl_val_note = tk.Label(self.window, textvariable=self.res_note)
        self.lbl_val_note.place(x=self.x_right_col + space, y=self.y_row3 + 25)

        self.res_phone.set("055484654654")
        # lower part ----------------------------

        bttn_next = tk.Button(self.window, text="Next",bg=darkblue)
        bttn_next.place(x=self.x_right_col+space, y=self.y_row4, height=btnsize, width=1.5*btnsize)
        bttn_next.bind("<Button-1>", self.bttn_next_onclick)  # <Button-1> = left click

        bttn_start = tk.Button(self.window, text="Match",bg=darkblue)
        bttn_start.place(x=midcol+75, y=self.y_row0+self.size, height=btnsize, width=1.5*btnsize)
        bttn_start.bind("<Button-1>", self.bttn_start_onclick)  # <Button-1> = left click

    def show(self):
        self.window.mainloop()


'''class DemoIntro:
    window = tk.Tk()
   # main_screen = GUI()
    def startbutton_onclick(self,a):
        main = tk.Toplevel(GUI)

    def setup(self):
        bttn_chooseimage = tk.Button(self.window, text="Browse", bg="white")
        bttn_chooseimage.place(x=0, y=0)
        bttn_chooseimage.bind("<Button-1>", self.startbutton_onclick)



    def show(self):
        self.window.mainloop()

    def __init__(self):
        self.setup()
        self.show()

'''
# window = DemoIntro()
window = GUI()
