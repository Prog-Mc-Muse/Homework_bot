import webbrowser
import pyautogui as pag
from time import sleep

def main():
    webbrowser.open_new("https://web.whatsapp.com/")
    #sleep(10)
    coord = pag.locateOnScreen("find.png")
    print(coord)
    x,y = pag.center(pag.locateOnScreen("find.png", confidence = 0.5))

    pag.moveTo(x,y,1)
    pag.moveRel(20,10, 1)

if __name__ == '__main__':
    main()
