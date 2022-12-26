import random
from tkinter import *
from tkmacosx import Button
from PIL import Image, ImageTk
main = Tk()
main.geometry("621x560")
main.resizable(width=False, height=False)
main.title("° ˖✧ Keyboard Prediction ✧˖ °")
main.iconbitmap("icon.ico")
load=Image.open("main_bg.jpg")
render=ImageTk.PhotoImage(load)
img=Label(main, image=render)
img.place(x=0,y=0)

def _window_1():
    win = Toplevel(main)
    import PySimpleGUI as sg
    sg.theme('LightGreen10')

    font=("Montserrat", 17)

    def keyboard():
        key = int(radio.get())
        first_word = str(wordArea.get("1.0","end-1c"))


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

        layout = [[sg.Text("Word you want instead:", size =(17, 1), font=font),sg.InputText(key="-Response-", font=font, size=(18,10))],
        [sg.Button('Agree',font=font),
        sg.pin(sg.Button('Append word',font=font)),
        sg.pin(sg.Button('End',font=font))],
        ]

        window = sg.Window('Keyboard', layout, finalize=True)

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
            
            if event == "Agree":
                result.delete(1.0, END)
                message = message + " " + predicted_next_word
                result.delete(1.0, END)
            if event == "Append word":
                result.delete(1.0, END)
                value = values['-Response-']
                message = message + " " + value
                result.delete(1.0, END)

            if event == "End":
                result.delete(1.0, END)
                result.insert(1.0, message)
                break
            if event == sg.WIN_CLOSED:
                break

    def clear():
        result.delete(1.0, END)
        wordArea.delete(1.0, END)

    win.geometry('1205x560')
    win.resizable(width=False, height=False)
    win.title("° ˖✧ Keyboard Prediction ✧˖ °")
    win.iconbitmap("icon.ico")
    load=Image.open("kb_bg.jpg")
    render=ImageTk.PhotoImage(load)
    img=Label(win, image=render)
    img.place(x=0,y=0)

    radio = IntVar()
    rad = Label(win, text = "Choose the Accuracy level", font=font,fg="white", bg="#339C16", width=22)
    rad.place(y=353, x=85)
    r1 = Radiobutton(win, text="Accuracy level 1", variable=radio, value=1,font=font, bg="white")
    r1.place(y=245, x=130)
    r2 = Radiobutton(win, text="Accuracy level 2", variable=radio, value=2,font=font, bg="white")
    r2.place(y=275, x=130)
    r3 = Radiobutton(win, text="Accuracy level 3", variable=radio, value=3,font=font, bg="white")
    r3.place(y=305, x=130)

    wlbl = Label(win, text = "Input the first word",  font=font,fg="white", bg="#339C16", width=22)
    wlbl.place(y=503, x=125)
    wordArea = Text(win, width=10,bg="white",font=("Montserrat", 35), highlightthickness=0)
    wordArea.place(x=110, y=430,width=320, height=50)

    result = Text(win, font=('Montserrat', 17), bg="white", fg="black", borderwidth=0, highlightthickness=0, wrap=WORD)
    result.place(y=60, x=600, width=530, height=400)
    button_s = Button(win, text=' Submit ', font=('Montserrat', 20),bg="#339C16", fg="white", width=150,height=40,highlightbackground="white", activebackground="#1cbd17", borderwidth=0, highlightthickness=0,command=keyboard)
    button_s.place(x=695,y=480)

    button_c = Button(win, text=' Clear ', font=('Montserrat', 20),bg="#339C16", fg="white", width=150,height=40,highlightbackground="white", activebackground="#1cbd17", borderwidth=0, highlightthickness=0,command=clear)
    button_c.place(x=895,y=480)
    win.mainloop()


def _window_2():
    win = Toplevel(main)

    def _text_generator():
        choice = var.get()
        key = int(radio.get())
        
        character1 = str(wordArea.get("1.0","end-1c"))

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

        if choice == "Make a sentence":
            sentence_stopper = ['.', '?', '!']
            message = character1.capitalize()
            while message[-1] not in sentence_stopper:
                try:
                    character2 = random.choice(markov_lib[character1.lower()])
                    message += " " + character2
                    character1 = " ".join((message.split())[-(key):])
                except KeyError as e:
                    result.insert(1.0, "-------------------------\nThe training text is not big enough to generate the next word. Exited")
                    return(result.insert(1, message))
            return(result.insert(1.0, message))

        if choice == "Make a paragraph with\nchosen number of words":
            word_count = int(numArea.get("1.0","end-1c"))
            message = character1.capitalize()
            #print(len(message.split()))
            for i in range(word_count):
                try:
                    character2 = random.choice(markov_lib[character1.lower()])
                except KeyError as e:
                    result.insert(1.0,"-------------------------\nThe training text is not big enough to generate the next word. Exited")
                    return(result.insert(1.0, message))
                message += " " + character2
                #print(message)
                character1 = " ".join((message.split())[-(key):])
                #print(len(message.split()))
                '''except KeyError as e:
                    print("-------------------------\nThe training text is not big enough to generate the next word. Exited")
                    return(message)'''
            #print(len(message))
            return(result.insert(1.0, message))

    def clear():
        result.delete(1.0, END)
        wordArea.delete(1.0, END)
        numArea.delete(1.0, END)

    win.title("° ˖✧ Paragraph Generator ✧˖ °")
    win.geometry('1205x560')
    win.resizable(width=False, height=False)
    win.iconbitmap("icon.ico")
    load=Image.open("para_bg (1).jpg")
    render=ImageTk.PhotoImage(load)
    img=Label(win, image=render)
    img.place(x=0,y=0)
    win.geometry('1205x560')
    font=("Montserrat", 17)
    var = StringVar();
    options = [
        "Make a sentence" ,
        "Make a paragraph with\nchosen number of words"
        ]
    var.set("Choose the functionality")

    menu=OptionMenu(win, var, *options)
    menu.config(bg="white", font=font,highlightthickness=0, borderwidth=0)
    menu["menu"].config(bg="white",activeforeground="#339C16",font=font)
    menu.place(y=165,x=60)

    radio = IntVar()
    rad = Label(win, text = "Choose the Accuracy level", font=font,fg="white", bg="#339C16", width=21)
    rad.place(y=340, x=40)
    r1 = Radiobutton(win, text="Accuracy level 1", variable=radio, value=1,font=font, bg="white")
    r1.place(y=230, x=85)
    r2 = Radiobutton(win, text="Accuracy level 2", variable=radio, value=2,font=font, bg="white")
    r2.place(y=260, x=85)
    r3 = Radiobutton(win, text="Accuracy level 3", variable=radio, value=3,font=font, bg="white")
    r3.place(y=290, x=85)

    wlbl = Label(win, text = "Input the first word", font=font,fg="white", bg="#339C16", width=22)
    wlbl.place(y=505, x=136)
    wordArea = Text(win, width=10,bg="white",font=("Montserrat", 35), highlightthickness=0)
    wordArea.place(x=95, y=420,width=390, height=70)

    now = Label(win, text = "Number of words",font=font,fg="white", bg="#339C16", width=12)
    now.place(y=340, x=365)
    numArea = Text(win, width=10,bg="white",font=("Montserrat", 35), highlightthickness=0)
    numArea.place(x=390, y=245,width=100, height=70)


    button_s = Button(win, text=' Submit ', font=('Montserrat', 20),bg="#339C16", fg="white", width=150,height=40,highlightbackground="white", activebackground="#1cbd17", borderwidth=0, highlightthickness=0,command=_text_generator)
    button_s.place(x=695,y=480)

    button_c = Button(win, text=' Clear ', font=('Montserrat', 20),bg="#339C16", fg="white", width=150,height=40,highlightbackground="white", activebackground="#1cbd17", borderwidth=0, highlightthickness=0,command=clear)
    button_c.place(x=895,y=480)

    result=Text(win,font=('Montserrat', 17), bg="white", fg="black", borderwidth=0, highlightthickness=0, wrap=WORD)
    result.place(y=85, x=620, width=500, height=380)
    win.mainloop()    



button_1 = Button(main,
             text ="Keyboard",font=('Montserrat', 20),bg="#339C16", fg="white", width=150,height=40,
             highlightbackground="#e3e3e3", activebackground="#1cbd17", borderwidth=0, highlightthickness=0,
             command =_window_1)
button_1.place(x=150,y=400)

button_2 = Button(main,
             text ="Paragraph",font=('Montserrat', 20),bg="#339C16", fg="white", width=150,height=40,
             highlightbackground="#e3e3e3", activebackground="#1cbd17", borderwidth=0, highlightthickness=0,
             command = _window_2)
button_2.place(x=350,y=400)
main.mainloop()