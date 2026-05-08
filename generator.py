import wikipedia
import re
import requests
import random
from tkinter import *
from tkmacosx import Button
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings("ignore")

count = 0
while count < 10:
    try:
        titles = wikipedia.random(10)
        for title in titles:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                if len(page.content) > 5000:
                    text = ""
                    text += page.content + " "
                    text = re.sub(r'== References ==.*', '', text, flags=re.DOTALL)
                    text = re.sub(r'=+.*?=+', '', text)
                    text = re.sub(r'\[[\d,\s–-]+\]', '', text)
                    text = re.sub(r'\([\d,\s–-]+\)', '', text)
                    text = re.sub(r'\{\|.*?\|\}', '', text, flags=re.DOTALL)
                    text = re.sub(r'\n+', '\n', text)
                    count += 1
                    if count >= 10:
                        break
            except wikipedia.exceptions.DisambiguationError as e:
                try:
                    options = [option for option in e.options]
                    choice = random.choice(options)
                    page = wikipedia.page(choice, auto_suggest=False)
                    if len(page.content) > 5000:
                        text = " "
                        text += page.content + " "
                        text = re.sub(r'== References ==.*', '', text, flags=re.DOTALL)
                        text = re.sub(r'=+.*?=+', '', text)
                        text = re.sub(r'\[[\d,\s–-]+\]', '', text)
                        text = re.sub(r'\([\d,\s–-]+\)', '', text)
                        text = re.sub(r'\{\|.*?\|\}', '', text, flags=re.DOTALL)
                        text = re.sub(r'\n+', '\n', text)
                        count += 1
                        print(f"Collected: {page.title}")
                except Exception:
                    print(f"Skipp: {title}")
            except wikipedia.exceptions.PageError:
                    print(f"Page not found: {title}")
            except Exception as e:
                print(f"Error:'{title}': {e}")
    except requests.exceptions.JSONDecodeError:
        print("Error: Wikipedia API returned invalid JSON.")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
   
print("Collected Articles:", count)

urls = ["https://raw.githubusercontent.com/Phylliida/Dialogue-Datasets/master/MovieCorpus.txt",
    "https://raw.githubusercontent.com/Phylliida/Dialogue-Datasets/master/TwitterLowerAsciiCorpus.txt",
    "https://raw.githubusercontent.com/Phylliida/Dialogue-Datasets/master/TwitterConvCorpus.txt",
    "https://raw.githubusercontent.com/Phylliida/Dialogue-Datasets/master/BNCCorpus.txt",
    "https://raw.githubusercontent.com/Phylliida/Dialogue-Datasets/master/BNCSplitWordsCorpus.txt"]

for url in urls:
        r = requests.get(url)
        text += r.text + " "

main = Tk()
main.geometry("621x560")
main.resizable(width=False, height=False)
main.title("° ˖✧ A Cool Text Generator ✧˖ °")
icon = PhotoImage(file='icon.png')
main.iconphoto(True, icon)
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
        text_data = ''.join([i.lower() for i in text if not i.isdigit()]).replace("\n", " ")
        text_data = text_data.split()

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
            find_input = " ".join(message.split()[-key:]).lower()
            next_words = markov_lib.get(find_input)
            if not next_words and key > 1:
                find_input = message.split()[-1].lower()
                next_words = markov_lib.get(find_input)
            if not next_words:
                result.insert(1.0, "-------------------------\nThe training text is not big enough to generate the next word. Exited")
                return
            predicted_next_word = random.choice(next_words)
    

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
    icon = PhotoImage(file='icon.png')
    main.iconphoto(True, icon)
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

        text_data = ''.join([i.lower() for i in text if not i.isdigit()]).replace("\n", " ")
        text_data = text_data.split()
        
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
            while message and message[-1] not in sentence_stopper:
                find_input = " ".join(message.split()[-key:]).lower()
                next_words = markov_lib.get(find_input)
                if not next_words and key > 1:
                    find_input = message.split()[-1].lower()
                    next_words = markov_lib.get(find_input)
                if not next_words:
                    result.insert(1.0, "-------------------------\nThe training text is not big enough to generate the next word. Exited")
                    return
                character2 = random.choice(next_words)
                message += " " + character2
                
            return(result.insert(1.0, message))

        if choice == "Make a paragraph with\nchosen number of words":
            try:
                word_count = int(numArea.get("1.0","end-1c"))
            except ValueError:
                result.insert(1.0, "Please enter a valid number.")
                return
            message = character1.capitalize()
            #print(len(message.split()))
            for i in range(word_count):
                find_input = " ".join(message.split()[-key:]).lower()
                next_words = markov_lib.get(find_input)
                if not next_words and key > 1:
                    find_input = message.split()[-1].lower()
                    next_words = markov_lib.get(find_input)
                if not next_words:
                    result.insert(1.0, "-------------------------\nThe training text is not big enough to generate the next word. Exited")
                    return
                character2 = random.choice(next_words)
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
    icon = PhotoImage(file='icon.png')
    main.iconphoto(True, icon)
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
