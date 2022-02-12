import webbrowser
import pyautogui as pag
import pyperclip
from time import sleep


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
            pag.click(x,y, 2,0.2)
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




def main():
    start_whatsapp()
    chat_name="Домашнее задание 6 Г"
    text=get_last_messeg(chat_name)
    chat_name="Папа Мегафон"
    send_masseg(chat_name,text)

if __name__ == '__main__':
    main()
