import webbrowser
from flask import Flask, render_template, request, redirect
import pyautogui as pag
import pyperclip
import json
import datetime
from time import sleep

app = Flask(__name__)

@app.route('/')
def tasks():
    return render_template('tasks.html', task_dict = task_dict)


@app.route('/update/<subj>', methods = ['POST','GET'])
def update(subj):
    print(subj)
    if request.method =='POST':
        print('POST')
        stp_datetime = datetime.datetime.now()
        task_dict[subj]['задание'] = request.form['task']
        task_dict[subj]['год'] = stp_datetime.year
        task_dict[subj]['месяц'] = stp_datetime.month
        task_dict[subj]['день'] = stp_datetime.day
        task_dict[subj]['час'] = stp_datetime.hour
        json_save()
        return redirect('/')
    else:
        return render_template('subj.html', task_dict = task_dict, subj = subj)


math_key_words = ("МАТИМАТИКЕ","МАТКЕ", "МАТЕМАТИКЕ")
rus_key_words = ("РУССКОМУ","РУСКОМУ","РУС ЯЗ")
bio_key_words = ("БИОЛОГИИ")
geo_key_words = ("ГЕОГРАФИИ","ГИОГРАФИИ")
info_key_words = ("ИНФОРМАТИКЕ","ИНФАРМАТИКЕ","ИНФАРМАТИКИ", "ИНФЕ")
history_key_words = ("ИСТОРИИ"),
lit_key_words = ("ЛИТРЕ", "ЛИТИРАТУРЕ", "ЛИТЕРАТУРЕ")
nat_rus_key_words = ("РОДНОМУ РУССКОМУ", "РОДНОМУ РУССКОМУ ЯЗЫКУ", "РОД РУС", "РОДНОМУ РУС", "РОД РУССКОМУ")
nat_lit_key_words = ("РОДНОЙ ЛИТЕРАТУРЕ", "РОДНОЙ ЛИТИРАТУРЕ", "РОДНОЙ ЛИТРЕ", "РОД ЛИТРЕ", "РОД ЛИТЕРАТУРЕ")
subject_dict = {"РУССКИЙ": rus_key_words,
                "МАТЕМАТИКА": math_key_words,
                "БИОЛОГИЯ": bio_key_words,
                "ГЕОГРАФИЯ": geo_key_words,
                "ИНФАРМАТИКА": info_key_words,
                "ИСТОРИЯ": history_key_words,
                "ЛИТЕРАТУРА": lit_key_words,
                "РОДНАЯ ЛИТЕРАТУРА": nat_lit_key_words,
                "РОДНОЙ РУССКИЙ": nat_rus_key_words,}
task_request = ("ЧТО","ЧЁ","КАКОЕ","КАКИЕ")
schedule_dict = {"РУССКИЙ": [1,1,1,1,1,0,0],
                 "МАТЕМАТИКА": [1,1,1,1,1,0,0],
                 "БИОЛОГИЯ": [0,0,1,1,0,0,0],
                 "ГЕОГРАФИЯ": [0,0,1,0,0,0,0],
                 "ИНФАРМАТИКА": [0,0,0,1,0,0,0],
                 "ИСТОРИЯ": [1,0,0,1,0,1,0],
                 "ЛИТЕРАТУРА": [0,1,0,0,1,0,0],
                 "РОДНАЯ ЛИТЕРАТУРА": [0,0,0,0,1,0,0],
                 "РОДНОЙ РУССКИЙ": [0,0,0,0,1,0,0],}

def actualyty_chaker(subj):
    year = task_dict[subj]['год']
    month = task_dict[subj]['месяц']
    day = task_dict[subj]['день']
    task_date = datetime.date(year, month, day)
    task_week_day = task_date.weekday()
    for ii in range(7):
        cur_day = (task_week_day + ii + 1) % 7
        if schedule_dict[subj][cur_day]:
            actualyty_days = ii
            break
    cur_date = datetime.date.today()
    dt = cur_date - task_date
    print(dt)
    delta_days = int(dt.days)
    if delta_days > actualyty_days:
        return False
    else:
        return True



def init():
    global task_dict
    with open("tasks.json", "r") as f:
        task_dict = json.load(f)


def start_whatsapp():
    webbrowser.open_new("https://web.whatsapp.com/")
    whatsapp_on = None
    while not whatsapp_on:
        whatsapp_on = pag.locateOnScreen("redy.png", confidence = 0.9)
        sleep(1)
    return  True


def chat_select(chat_name):
    x,y = pag.center(pag.locateOnScreen("find.jpg", confidence = 0.9))
    pag.moveTo(x,y)
    pag.click(x,y)
    pyperclip.copy(chat_name)
    pag.hotkey("ctrl", "v")
    pag.hotkey("enter")

def get_last_messeg_in_open_chat():
    Text = None
    x_y = pag.locateOnScreen("masseg.png", confidence = 0.7)
    if x_y:
        pag.moveTo(x_y[0],x_y[1])
        pag.moveRel(35,-40)
        x,y = pag.position()
        colour = pag.pixel(x,y)
        white = (255,255,255)
        if colour == white:
            pag.click(x,y, 3,0.2)
            pag.hotkey("ctrl", "c")
            Text = pyperclip.paste()
        return Text
    else:
        return None


def get_last_messeg(chat_name):
    chat_select(chat_name)
    sleep(2)
    Text = None
    x_y = pag.locateOnScreen("masseg.png", confidence = 0.7)
    if x_y:
        pag.moveTo(x_y[0],x_y[1])
        pag.moveRel(35,-40)
        x,y = pag.position()
        colour = pag.pixel(x,y)
        white = (255,255,255)
        if colour == white:
            pag.click(x,y, 3,0.2)
            pag.hotkey("ctrl", "c")
            Text = pyperclip.paste()
        return Text
    else:
        return None

def send_masseg_in_open_chat(chat_name, masseg):
    pyperclip.copy(masseg)
    pag.hotkey("ctrl", "v")
    pag.hotkey("enter")

def send_masseg(chat_name, masseg):
    chat_select(chat_name)
    pyperclip.copy(masseg)
    pag.hotkey("ctrl", "v")
    pag.hotkey("enter")

def task_responder(subj,chat):
    print(subj)
    send_masseg_in_open_chat(chat,task_dict[subj]['задание'])

def task_saver(subj, big_masseg):
    global task_dict
    print(subj,big_masseg)
    cur_date = datetime.datetime.now()
    for i,char in enumerate(big_masseg):
        if char == "@":
            start_point = i
            break
    task_msg = big_masseg[start_point:]
    task_dict[subj]['задание'] = task_msg
    task_dict[subj]['год'] = cur_date.year
    task_dict[subj]['месяц'] = cur_date.month
    task_dict[subj]['день'] = cur_date.day
    task_dict[subj]['час'] = cur_date.hour
    json_save()


def json_save():
    with open("tasks.json", "w") as f:
        json.dump(task_dict, f, ensure_ascii= False, indent= 2, sort_keys= True)


def masseg_parser(masseg, chat):
    big_masseg = masseg.upper()
    question_flg = False
    for str in task_request:
        question_flg = question_flg or (str in big_masseg)
    if question_flg:
        for subj in subject_dict:
            task_flg = False
            for str in subject_dict[subj]:
                task_flg = task_flg or (str in big_masseg)
            if task_flg and actualyty_chaker(subj):
                task_responder(subj,chat)
            else:
                print("не сохранено актуального задания")
    else:
        give_task_flg = ("БОТ, ПРИМИ ЗАДАНИЕ" in big_masseg)
        if give_task_flg:
            for subj in subject_dict:
                 if subj in big_masseg:
                    task_saver(subj,big_masseg)

def main():
    print(actualyty_chaker("ГЕОГРАФИЯ"))
    start_whatsapp()

    chat_name="Папа Мегафон"
    chat_select(chat_name)
    while True:
        text=get_last_messeg_in_open_chat()
        if text:
            masseg_parser(text, chat_name)
        sleep(2)

if __name__ == '__main__':
    init()
    app.run(debug=True)
    #main()
