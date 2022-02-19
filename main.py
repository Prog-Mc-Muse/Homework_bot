import webbrowser
import pyautogui as pag
import pyperclip
from time import sleep

math_key_words = ("МАТИМАТИКЕ","МАТКЕ")
rus_key_words = ("РУССКОМУ","РУСКОМУ","РУС ЯЗ")
subject_dict = {"РУССКИЙ": rus_key_words,
                "МАТИМАТИКА": math_key_words,}
task_request = ("ЧТО","ЧЁ","КАКОЕ","КАКИЕ")
task_dict = {"РУССКИЙ": "упр 146",
             "МАТИМАТИКА": "№ 578,579"}




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

def get_last_messeg(chat_name):
    chat_select(chat_name)
    sleep(2)
    Text = None
    x_y = pag.locateOnScreen("masseg.png", confidence = 0.7)
    print(x_y)
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

def send_masseg(chat_name, masseg):
    chat_select(chat_name)
    pyperclip.copy(masseg)
    pag.hotkey("ctrl", "v")
    pag.hotkey("enter")

def task_responder(subj,chat):
    print(subj)
    send_masseg(chat,task_dict[subj])

def task_saver(subj, big_masseg):
    global task_dict
    print(subj,big_masseg)
    for i,char in enumerate(big_masseg):
        if char == "@":
            start_point = i
            break
    task_msg = big_masseg[start_point:]
    task_dict[subj] = task_msg

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
            if task_flg:
                task_responder(subj,chat)
    else:
        give_task_flg = ("БОТ, ПРИМИ ЗАДАНИЕ" in big_masseg)
        if give_task_flg:
            for subj in subject_dict:
                 if subj in big_masseg:
                    task_saver(subj,big_masseg)

def main():
    start_whatsapp()

    chat_name="Папа Мегафон"
    while True:
        text=get_last_messeg(chat_name)
        if text:
            masseg_parser(text, chat_name)
        sleep(2)

if __name__ == '__main__':
    main()
