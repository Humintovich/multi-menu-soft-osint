cd ~ && rm -rf osint_toolkit && mkdir osint_toolkit && cd osint_toolkit && pkg update -y && pkg install python -y && pip install requests beautifulsoup4 colorama fake-useragent phonenumbers email-validator dnspython python-whois -q && cat > osint.py << 'EOF'
import os, sys, time, hashlib, requests, socket, whois, dns.resolver, phonenumbers, json
from phonenumbers import carrier, geocoder, timezone
from email_validator import validate_email, EmailNotValidError
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
init(autoreset=True)
RED, GREEN, YELLOW, CYAN, RESET, BOLD = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Style.RESET_ALL, Style.BRIGHT

VALID_KEYS_HASH = [
    hashlib.sha256("admin".encode()).hexdigest(),
    hashlib.sha256("root".encode()).hexdigest(),
    hashlib.sha256("12345".encode()).hexdigest(),
    hashlib.sha256("osint".encode()).hexdigest(),
    hashlib.sha256("webuga".encode()).hexdigest(),
]
KEY_FILE = "license.key"
def check_license():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE,'r') as f:
            return hashlib.sha256(f.read().strip().encode()).hexdigest() in VALID_KEYS_HASH
    return False
def save_key(k):
    with open(KEY_FILE,'w') as f: f.write(k)
def clear(): os.system('clear')
def banner():
    clear()
    print(f"{RED}{BOLD}\n  ██████╗ ███████╗██╗███╗   ██╗████████╗\n  ██╔══██╗██╔════╝██║████╗  ██║╚══██╔══╝\n  ██████╔╝███████╗██║██╔██╗ ██║   ██║   \n  ██╔══██╗╚════██║██║██║╚██╗██║   ██║   \n  ██║  ██║███████║██║██║ ╚████║   ██║   \n  ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   {RESET}")
    print(f"{RED}{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{RED}{BOLD}║              ☠  OSINT TOOLKIT v5.0  ☠                        ║{RESET}")
    print(f"{RED}{BOLD}║                by @webuga | @vetrovsnos                      ║{RESET}")
    print(f"{RED}{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}\n")
def menu():
    print(f"{RED}{BOLD}┌─────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{RED}{BOLD}│  {YELLOW}1.{GREEN} 👤 Поиск по нику    {YELLOW}2.{GREEN} 📧 Поиск по email    {YELLOW}3.{GREEN} 📞 Поиск по номеру    {RED}│{RESET}")
    print(f"{RED}{BOLD}│  {YELLOW}4.{GREEN} 🌐 Анализ домена   {YELLOW}5.{GREEN} 🖥️  Анализ IP       {YELLOW}6.{GREEN} 🔗 Анализ ссылки     {RED}│{RESET}")
    print(f"{RED}{BOLD}│  {YELLOW}7.{GREEN} 📱 Telegram ник    {YELLOW}8.{GREEN} 🐙 GitHub ник      {YELLOW}9.{GREEN} 🔍 Проверка утечек  {RED}│{RESET}")
    print(f"{RED}{BOLD}│  {YELLOW}10.{GREEN}🔐 Анализ хэша     {YELLOW}11.{GREEN}📄 Метаданные      {YELLOW}12.{GREEN}🤖 Поиск по ботам    {RED}│{RESET}")
    print(f"{RED}{BOLD}│  {YELLOW}13.{GREEN}🔍 Google Dorks    {YELLOW}14.{GREEN}🤖 ИИ Ассистент    {YELLOW}15.{GREEN}📖 Мануалы          {RED}│{RESET}")
    print(f"{RED}{BOLD}├─────────────────────────────────────────────────────────────┤{RESET}")
    print(f"{RED}{BOLD}│  {YELLOW}0.{RED} ❌ Выход                                              {RED}│{RESET}")
    print(f"{RED}{BOLD}└─────────────────────────────────────────────────────────────┘{RESET}")
def search_username():
    banner(); username=input(f"{CYAN}Ник: {RESET}"); print(f"{YELLOW}Поиск...{RESET}")
    sites=[("Twitter",f"https://twitter.com/{username}"),("Instagram",f"https://instagram.com/{username}"),("GitHub",f"https://github.com/{username}"),("Telegram",f"https://t.me/{username}"),("VK",f"https://vk.com/{username}"),("Reddit",f"https://reddit.com/user/{username}")]
    for n,u in sites:
        try:
            if requests.get(u,timeout=5).status_code==200: print(f"{GREEN}[+] {n}: {u}{RESET}")
        except: pass
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_email():
    banner(); email=input(f"{CYAN}Email: {RESET}")
    try:
        valid=validate_email(email); email=valid.email; print(f"{GREEN}[+] Email валиден{RESET}")
    except: print(f"{RED}[-] Невалиден{RESET}")
    print(f"{GREEN}https://haveibeenpwned.com/account/{email}{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_phone():
    banner(); phone=input(f"{CYAN}Номер (+7...): {RESET}")
    try:
        p=phonenumbers.parse(phone)
        print(f"{GREEN}Страна: {geocoder.description_for_number(p,'ru')}, Оператор: {carrier.name_for_number(p,'ru')}{RESET}")
    except: print(f"{RED}Неверный формат{RESET}")
    print(f"{GREEN}https://t.me/{phone}{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_domain():
    banner(); domain=input(f"{CYAN}Домен: {RESET}")
    os.system(f"whois {domain} 2>/dev/null | head -30")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_ip():
    banner(); ip=input(f"{CYAN}IP: {RESET}")
    os.system(f"curl -s http://ip-api.com/json/{ip}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_url():
    banner(); url=input(f"{CYAN}URL: {RESET}")
    print(f"{GREEN}VirusTotal: https://www.virustotal.com/gui/home/url{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_telegram():
    banner(); username=input(f"{CYAN}Username: {RESET}")
    print(f"{GREEN}https://t.me/{username}{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_github():
    banner(); username=input(f"{CYAN}Username: {RESET}")
    print(f"{GREEN}https://github.com/{username}{RESET}")
    try:
        r=requests.get(f"https://api.github.com/users/{username}")
        if r.status_code==200:
            data=r.json()
            print(f"{GREEN}Репозиториев: {data.get('public_repos',0)}, Подписчиков: {data.get('followers',0)}{RESET}")
    except: pass
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def check_breaches():
    banner(); email=input(f"{CYAN}Email: {RESET}")
    print(f"{GREEN}https://haveibeenpwned.com/account/{email}{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def hash_analysis():
    banner(); h=input(f"{CYAN}Хэш: {RESET}")
    print(f"{GREEN}VirusTotal: https://www.virustotal.com/gui/search/{h}{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def meta_analysis():
    banner(); print(f"{YELLOW}Отправьте файл @webuga{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def search_through_bots():
    banner(); query=input(f"{CYAN}Запрос: {RESET}")
    print(f"{GREEN}https://t.me/OVERLOADRobot?start={query}{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def dork_search():
    banner(); query=input(f"{CYAN}Ник: {RESET}")
    print(f"{GREEN}https://www.google.com/search?q=%22{query}%22+site:twitter.com{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def ai_assistant():
    banner(); print(f"{CYAN}ИИ Ассистент (0 для выхода){RESET}")
    while True:
        q=input(f"{CYAN}> {RESET}")
        if q=='0': break
        print(f"{GREEN}Ответ по OSINT, хакингу, безопасности, Telegram.{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def manuals():
    banner(); print(f"{YELLOW}Мануалы: OSINT, соц. инженерия, безопасность Telegram, анонимность, карты, Android, топ инструментов.{RESET}")
    input(f"\n{YELLOW}Нажмите Enter...{RESET}")
def main():
    if check_license():
        while True:
            banner(); menu()
            c=input(f"{CYAN}Выберите: {RESET}")
            if c=='1': search_username()
            elif c=='2': search_email()
            elif c=='3': search_phone()
            elif c=='4': search_domain()
            elif c=='5': search_ip()
            elif c=='6': search_url()
            elif c=='7': search_telegram()
            elif c=='8': search_github()
            elif c=='9': check_breaches()
            elif c=='10': hash_analysis()
            elif c=='11': meta_analysis()
            elif c=='12': search_through_bots()
            elif c=='13': dork_search()
            elif c=='14': ai_assistant()
            elif c=='15': manuals()
            elif c=='0': clear(); print(f"{RED}До свидания!{RESET}"); sys.exit(0)
            else: print(f"{RED}Неверный выбор{RESET}"); time.sleep(1)
    else:
        while True:
            banner()
            print(f"{RED}{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{RED}{BOLD}║                     {YELLOW}АВТОРИЗАЦИЯ{RED}                                 ║{RESET}")
            print(f"{RED}{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
            k=input(f"{CYAN}Ключ: {RESET}")
            if hashlib.sha256(k.encode()).hexdigest() in VALID_KEYS_HASH:
                save_key(k); print(f"{GREEN}Активировано{RESET}"); time.sleep(1); main(); break
            else: print(f"{RED}Неверный ключ{RESET}"); time.sleep(1)
if __name__=="__main__": main()
EOF
python osint.py
