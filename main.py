
from tkinter import *
import requests
import time
from itertools import count, cycle
from PIL import ImageTk, Image
from tkinter import messagebox
import pyodbc

server = 'RISHI\SQLEXPRESS'
database = 'p'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER=' + server + ';\
                        DATABASE=' + database + ';\
                        Trusted_Connection=yes;')


global cursor
cursor = conn.cursor()


class ImageLabel(Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 10

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


def start3():
    frame.destroy()
    start1()


def start4():
    fr1.destroy()
    start1()


def start12():
    fr2.destroy()
    start2()


def know_more():
    fr1.destroy()
    global fr2
    fr2 = Frame(canvas)
    fr2.pack()
    bg = PhotoImage(file='Forecast Terms_page.png')
    km_bck = Label(fr2, image=bg)
    km_bck.pack()
    img10 = PhotoImage(file='GET-STARTED-6.png')
    back1 = Button(fr2, text='  <= Back  ', font=('Comic Sans MS', 10),
                   fg='white', bg="black", border=10, command=lambda: start12())
    back1.pack()
    back1.place(x=660, y=520)
    canvas.mainloop()


def getweather(city):
    api = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        city+"&appid=06c921750b9a82d8f5d1294e1586276f"

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime('%I:%M:%S', time.gmtime(
        json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime('%I:%M:%S', time.gmtime(
        json_data['sys']['sunset'] - 21600))

    final_info = condition + "\n" + str(temp) + "°C"
    final_data = "\n" + "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" + "\n" + "Pressure: " + str(
        pressure) + "\n" + "Humidity: " + str(humidity) + "\n" + "Wind Speed: " + str(wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset
    label1.config(text=final_info)
    label2.config(text=final_data)
    txt = ('City:', city)
    label4.config(text=txt)


def getWeather1():
    try:
        city = textfield.get()
        getweather(city)

    except:
        messagebox.showinfo("Error in g2", "City Not Found")


def getWeather():
    try:
        cursor.execute("select city from login where userid='%s'" % userid)
        for row in cursor:
            city = row[0]
        getweather(city)

    except:
        messagebox.showinfo("Error in g1", "City Not Found")


def afterlgn():
    global userid, password

    userid = e1.get()
    password = e2.get()
    print(userid, password)
    cursor.execute(
        "select * from login where userid='%s' and pass='%s' " % (userid, password))
    flag = cursor.fetchall()
    if flag:

        fr11.destroy()
        start2()
    else:
        messagebox.showinfo("Error", "Incorrect UserId or Password!")


def add_values():
    try:
    

        global name1, userid1, pass1, dob1, city1
        name1 = name.get()
        userid1 = useridc.get()
        pass1 = passwc.get()
        dob1 = dob.get()
        city1 = city.get()

        cursor1 = conn.cursor()

        cursor1.execute("insert into login VALUES ('%s','%s','%s','%s','%s')" % (userid1, pass1, name1, dob1, city1))
        cursor1.commit()
    
        messagebox.showinfo("Success", "Successfully created new profile!")
        frame.destroy()
        start1()
    

    except:
        messagebox.showinfo("Error", "Something went wrong!")


def add():
    fr11.destroy()
    add1()


def add1():
    global frame, name, useridc, passwc, dob, city
    frame = Frame(canvas)
    frame.pack()
    bg1 = PhotoImage(file='bg4.png')
    bag = Label(frame, image=bg1)
    bag.pack()

    name = Entry(frame, width=40, font=('Comic Sans', 15))

    name.place(x=220, y=70)
    useridc = Entry(frame, width=40, font=('Comic Sans', 15))

    useridc.place(x=220, y=170)
    passwc = Entry(frame, width=40, font=('Comic Sans', 15))

    passwc.place(x=220, y=270)
    dob = Entry(frame, width=40, font=('Comic Sans', 15))
    dob.place(x=220, y=380)

    city = Entry(frame, width=40, font=('Comic Sans', 15))

    city.place(x=220, y=480)

    btn = Button(frame, text='Create profile', command=lambda: add_values())
    btn.pack()
    btn.place(x=600, y=550)

    btn = Button(frame, text='<< Back ', command=lambda: start3())
    btn.pack()
    btn.place(x=50, y=550)
    canvas.mainloop()


def start():
    fr.destroy()
    start1()


def mainpg():
    fr11.destroy()
    start2()


def start1():

    global fr11
    fr11 = Frame(canvas)
    fr11.pack()
    bg = PhotoImage(file='bg.png')
    bacg = Label(fr11, image=bg)
    bacg.pack()

    global e1, e2
    e1 = Entry(fr11, width=20, font=('Georgia 20'),border=5)
    e1.place(x=300, y=210)
    e2 = Entry(fr11, width=20, font=('Georgia 20'),border=5)
    e2.place(x=300, y=330)
    e2.config(show="*")

    btn1 = Button(fr11, text='Create profile', font=(
        'Comic Sans MS',12), fg='white', bg="black", border=8, command=lambda: add())
    btn1.pack()
    btn1.place(x=300, y=480)

    btn = Button(fr11, text= '     Login     ', font=('Comic Sans MS', 12),
                 fg='white', bg="black", border=8, command=lambda: afterlgn())
    btn.pack()
    btn.place(x=500, y=480)
    canvas.mainloop()


def start2():

    global fr1, textfield
    fr1 = Frame(canvas)
    fr1.pack()
    lbl1 = ImageLabel(fr1)
    lbl1.pack()
    lbl1.load("weathernew.gif")

    cursor.execute("select name from login where userid='%s' and pass='%s' " % (
        userid, password))
    for row in cursor:
        txt = row[0]
    txt = ("Welcome", txt, "!")
    name = Label(fr1, text=txt, font=(
        "Constantia", 25), fg='white', bg="#1c1d2f")
    name.pack()
    name.place(x=30, y=50)

    global label1, label2, label4
    label1 = Label(fr1, font=('Bahnschrift', 15), fg='white', bg="#1c1d2f")
    label1.pack()
    label1.place(x=50, y=130)
    label2 = Label(fr1, font=('Bahnschrift', 15), fg='white', bg="#1c1d2f")
    label2.pack()
    label2.place(x=50, y=350)
    label3 = Label(fr1, text='Forecast Terms', font=(
        'Algerian', 30), fg='white', bg="#1c1d2f")
    label3.pack()
    label3.place(x=400, y=450)

    label4 = Label(fr1, font=('Bahnschrift', 17), fg='white', bg="#1c1d2f")
    label4.pack()
    label4.place(x=50, y=100)
    km = Button(fr1, text='KNOW MORE', font=('Comic Sans MS', 10),
                fg='white', bg="black", border=10, command=lambda: know_more())
    km.pack()
    km.place(x=650, y=520)
    lo = PhotoImage(file='lo2.png')
    back = Button(fr1, image=lo, font=('Comic Sans MS', 10),
                  fg='white', bg="black", border=10, command=lambda: start4())
    back.pack()
    back.place(x=750, y=20)
    getWeather()
    textfield = Entry(fr1, font=("Constantia", 25), fg='white', bg="#1c1d2f")
    textfield.place(x=300, width=250, y=100)
    search = Button(fr1, text='Q', font=('Quantico', 25),
                    fg='white', bg="#1c1d2f", border=0, command=lambda: getWeather1())
    search.pack()
    search.place(x=550, y=90)

    canvas.mainloop()


global canvas
canvas = Tk()
canvas.geometry("800x600+200+100")
canvas.title("Forecast Terms")
global fr
fr = Frame(canvas)
fr.pack()

global lbl1
lbl1 = ImageLabel(fr)
lbl1.pack()
lbl1.load("weather.gif")
img = PhotoImage(file='GET-STARTED-6.png')
btn = Button(fr, image=img, command=lambda: start())
btn.pack()
btn.place(x=600, y=500)


canvas.mainloop()
