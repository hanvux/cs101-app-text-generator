import random
import sys
from tkinter import *
from tkinter.ttk import *
#https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/?ref=gcse connect two pages
import PySimpleGUI as sg



win = Tk()



# type this if want the button shown on output field
#prediction.set(expression)

def keyboard():
    layout = [[sg.Text('Response', size =(15, 1)),sg.InputText(key="-Response-")],
    [sg.Button('Tab')],
    [sg.Button('Nobe')],
    [sg.Button('End')],
    ]

    window = sg.Window('Keyboard', layout, finalize=True, return_keyboard_events=True)


    key = int(radio.get())
    first_word = str(wordArea.get())


    message = first_word

    data_sample = "215.txt"
    text_data = open(data_sample, 'r').read()
    text_data = ''.join([i for i in text_data if not i.isdigit()]).replace("\n", " ").split(' ')
    markov_lib = {}

    for i in range(len(text_data) - key):
        word = " ".join(text_data[i:i + key])
        if word.lower() in markov_lib.keys():
            markov_lib[word.lower()].append(text_data[i + key])
        else:
            markov_lib[word.lower()] = [text_data[i + key]]


    while(True):
        first_word = " ".join(message.split()[0-key:])
        try:
            predicted_next_word = random.choice(markov_lib[first_word.lower()])
        except KeyError as e:
            result.insert(1.0, "-------------------------\nThe training text is not big enough to predict the next word. Exited")
            sys.exit(1)
        
        r = message +" ["+predicted_next_word+"] "
        result.insert(1.0, r)
        event, values = window.read()

        if event == "Tab":
            result.delete(1.0, END)
            message = message + " " + predicted_next_word
        if event == "Nobe":
            result.delete(1.0, END)
            value = values['-Response-']
            message = message + " " + value
            result.delete(1.0, END)

        if event == "End":
            result.delete(1.0, END)
            result.insert(1.0, message)
            break



win.geometry('600x600')
prediction = StringVar()

radio = IntVar()
Label(text="Accuracy level", font=('Aerial 11')).pack()
r1 = Radiobutton(win, text="Accuracy level 1", variable=radio, value=1)
r1.pack(anchor=N)
r2 = Radiobutton(win, text="Accuracy level 2", variable=radio, value=2)
r2.pack(anchor=N)
r3 = Radiobutton(win, text="Accuracy level 3", variable=radio, value=3)
r3.pack(anchor=N)


wlbl = Label(win, text = "Input word")
wlbl.pack()
wordArea = Entry(win, width=10)
wordArea.pack()


lbl = Label(win, text = "Result")
lbl.pack()
result = Text(win)
result.place(y=370, relx=.5, anchor="c", width=450, height=70)
button_s = Button(win, text=' Submit ', command=keyboard).pack()
win.mainloop()