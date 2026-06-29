#!/usr/bin/env python3
import subprocess, sys, importlib
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def check_and_install():
    required = ['requests', 'whois']
    for pkg in required:
        try:
            importlib.import_module(pkg)
        except ImportError:
            print(f"Module '{pkg}' not found. Installing...")
            install_package(pkg)
check_and_install()

import os, time, random, shutil, re, json, base64, hashlib, requests, whois
from datetime import datetime
from urllib.parse import urlparse

ENCRYPTED_KEY = "UFlUSE9OU09DSUFMIEtFWQ=="
def check_key(input_key):
    try:
        decrypted = base64.b64decode(ENCRYPTED_KEY).decode('utf-8')
        return input_key.strip() == decrypted
    except:
        return False

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

def key_screen():
    sys.stdout.write(CLEAR)
    print(f"{PURPLE}{LOGO}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print(f"{PURPLE_BOLD}   FPYTHONSOCIAL v18.0{RESET}")
    print(f"{PURPLE_DIM}   Enter license key to continue{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print()
    attempt = 0
    while attempt < 3:
        key = input(f"{PURPLE}┌─ Enter key: {RESET}").strip()
        if check_key(key):
            print(f"{PURPLE_BOLD}✅ Key accepted! Loading...{RESET}")
            time.sleep(1)
            return True
        else:
            attempt += 1
            print(f"{RED}❌ Invalid key. Attempt {attempt} of 3.{RESET}")
            time.sleep(1)
            sys.stdout.write(CLEAR)
            print(f"{PURPLE}{LOGO}{RESET}")
            print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
            print(f"{PURPLE_BOLD}   FPYTHONSOCIAL v18.0{RESET}")
            print(f"{PURPLE_DIM}   Enter license key to continue{RESET}")
            print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
            print()
    print(f"{RED}❌ Too many attempts. Exiting.{RESET}")
    sys.exit(1)

class DB:
    def __init__(self):
        self.data = []
        self.files = []
    def load(self, fp):
        try:
            if fp.endswith('.json'):
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
            print(f"Error: {e}")
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

def check_email_breach(email):
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        r = requests.get(url, headers={'hibp-api-key': ''}, timeout=10)
        if r.status_code == 200:
            breaches = r.json()
            if breaches:
                return f"Found breaches: {len(breaches)}. List: " + ", ".join([b['Name'] for b in breaches])
            else:
                return "No breaches found."
        elif r.status_code == 404:
            return "No breaches found."
        else:
            return f"API error: {r.status_code}"
    except Exception as e:
        return f"Error: {e}"

def get_ip_info(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            return f"IP: {data.get('ip')}\nCity: {data.get('city')}\nRegion: {data.get('region')}\nCountry: {data.get('country')}\nOrg: {data.get('org')}\nPostal: {data.get('postal')}\nLoc: {data.get('loc')}"
        else:
            return f"API error: {r.status_code}"
    except Exception as e:
        return f"Error: {e}"

def whois_domain(domain):
    try:
        w = whois.whois(domain)
        result = []
        for key, value in w.items():
            if value:
                result.append(f"{key}: {value}")
        return "\n".join(result[:20])
    except Exception as e:
        return f"WHOIS error: {e}"

def check_phone_activity(phone):
    return "Use PhoneInfoga or manual search for phone activity."

def search_username(username):
    try:
        url = f"https://api.checkusernames.com/v1/username/{username}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            found = [s for s, v in data.items() if v.get('available') == False]
            if found:
                return f"Found on: {', '.join(found)}"
            else:
                return "Not found anywhere."
        else:
            return f"API error: {r.status_code}"
    except Exception as e:
        return f"Error: {e}"

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
                    return f"Password found in {count} breaches."
            return "Password not found in breaches."
        else:
            return f"API error: {r.status_code}"
    except Exception as e:
        return f"Error: {e}"

def combined_analysis(email=None, phone=None, ip=None):
    result = []
    if email:
        result.append(f"Email {email}: {check_email_breach(email)}")
    if phone:
        result.append(f"Phone {phone}: {check_phone_activity(phone)}")
    if ip:
        result.append(f"IP {ip}: {get_ip_info(ip)}")
    return "\n\n".join(result)

def print_header():
    sys.stdout.write(CLEAR)
    print(f"{PURPLE}{LOGO}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print(f"{PURPLE_BOLD}   FPYTHONSOCIAL v18.0     {PURPLE_DIM}by {AUTHOR}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
    print(f"{PURPLE_DIM}   Records: {len(db.data)} | Files: {len(db.files)}{RESET}")
    print(f"{PURPLE_BOLD}{'═'*60}{RESET}")

def menu_loop():
    global db
    while True:
        print_header()
        items = [
            "1.Name", "2.Phone", "3.Email", "4.Address", "5.Passport",
            "6.IP", "7.Login", "8.Date", "9.Car", "10.SNILS",
            "11.INN", "12.OKVED", "13.Company", "14.Position", "15.Telegram",
            "16.VK", "17.Instagram", "18.Twitter", "19.Domain", "20.General",
            "24.Email-breach", "25.IP-geo", "26.WHOIS", "27.Phone-act", "28.Username",
            "29.Password-breach", "30.Combo"
        ]
        for i in range(0, len(items), 4):
            row = items[i:i+4]
            line = ""
            for item in row:
                line += f"{PURPLE_BOLD}{item:<16}{RESET} "
            print(line)
        print()
        print(f"{PURPLE_DIM}  21-Load  22-Files  23-Clear  0-Exit{RESET}")
        print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
        choice = input(f"{PURPLE}┌─ Enter command or query:{RESET}\n{PURPLE}└─> {RESET}").strip()

        if choice == '0':
            break
        elif choice == '21':
            fp = input("File path: ").strip()
            if db.load(fp):
                print(f"Loaded. Total: {len(db.data)}")
            time.sleep(1)
            continue
        elif choice == '22':
            print("Files:")
            for f in db.files:
                print(f"  {f}")
            print(f"Total records: {len(db.data)}")
            time.sleep(1)
            continue
        elif choice == '23':
            db.data = []
            db.files = []
            print("Database cleared.")
            time.sleep(1)
            continue
        elif choice == '24':
            email = input("Enter email: ").strip()
            if email:
                print(check_email_breach(email))
            input("Press Enter...")
            continue
        elif choice == '25':
            ip = input("Enter IP: ").strip()
            if ip:
                print(get_ip_info(ip))
            input("Press Enter...")
            continue
        elif choice == '26':
            domain = input("Enter domain (example.com): ").strip()
            if domain:
                print(whois_domain(domain))
            input("Press Enter...")
            continue
        elif choice == '27':
            phone = input("Enter phone (+79991234567): ").strip()
            if phone:
                print(check_phone_activity(phone))
            input("Press Enter...")
            continue
        elif choice == '28':
            username = input("Enter username: ").strip()
            if username:
                print(search_username(username))
            input("Press Enter...")
            continue
        elif choice == '29':
            password = input("Enter password: ").strip()
            if password:
                print(check_password_breach(password))
            input("Press Enter...")
            continue
        elif choice == '30':
            email = input("Email (or Enter to skip): ").strip() or None
            phone = input("Phone (or Enter): ").strip() or None
            ip = input("IP (or Enter): ").strip() or None
            if email or phone or ip:
                print(combined_analysis(email, phone, ip))
            input("Press Enter...")
            continue

        if not db.data:
            print("Database empty! Load file (21).")
            time.sleep(1)
            continue
        types_map = {
            '1':'name','2':'phone','3':'email','4':'address','5':'passport',
            '6':'all','7':'all','8':'all','9':'all','10':'all',
            '11':'all','12':'all','13':'all','14':'all','15':'all',
            '16':'all','17':'all','18':'all','19':'all','20':'all'
        }
        st = types_map.get(choice, 'all')
        query = input(f"{PURPLE}┌─ Enter query:{RESET}\n{PURPLE}└─> {RESET}").strip()
        if not query:
            continue
        results = db.search(query, st)
        print(f"\n{PURPLE_BOLD}=== Results for '{query}' ({len(results)} records) ==={RESET}")
        if not results:
            print(f"{PURPLE_DIM}Nothing found.{RESET}")
        else:
            for i, r in enumerate(results[:30], 1):
                print(f"{PURPLE}[{i:2}]{RESET} {r}")
            if len(results) > 30:
                print(f"{PURPLE_DIM}... and {len(results)-30} more.{RESET}")
        print(f"{PURPLE_BOLD}{'═'*60}{RESET}")
        input(f"{PURPLE_DIM}Press Enter to continue...{RESET}")

if __name__ == '__main__':
    startup_rain()
    key_screen()
    menu_loop()
