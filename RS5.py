import os
import getpass
from colorama import Fore, Back, Style
from colorama import init
init()
print(Back.GREEN);print (Fore.BLACK + "Before use this script. Must start the winrm service(Run as administrator 'winrm quickconfig')")
print(Style.RESET_ALL)
print(Style.BRIGHT);print(Fore.CYAN + "___________ $$$$$$$$______$$$$$$$$$")
print("__________$$$$$$$$$$$$__$$$$$$$__$$$$")
print("_________$$$$$$$$$$$$$$$$$$$$$$$$__$$$")
print("_________$$$$$$$$$$$$$$$$$$$$$$$$__$$$")
print("_________$$$$$$$$$$$$$$$$$$$$$$$$__$$$")
print("__________$$$$$$$$$$$$$$$$$$$$$$__$$$")
print("____________$$$$$$$$$$$$$$$$$$$$$$$")
print("_______________$$$$$$$$$$$$$$$$$")
print("_________________$$$$$$$$$$$$$")
print("____________________$$$$$$$")
print("______________________$$$")
print("________________________$")
print(Style.RESET_ALL)
print("\t   Remote Shell ver 1.0 by Dmitriy.Belorukov@rusal.com")
name_pc = input("Введи имя компа:")
ping = os.system("ping %s -n 1 -w 1" % name_pc)
while ping == 1:
    print(Fore.RED + "%s не пингуется" % name_pc)
    print(Style.RESET_ALL)
    name_pc = input("Введи имя компа:")
    ping = os.system("ping %s -n 1 -w 1" % name_pc)
try_connect = os.system("winrs -r:%s cmd" % name_pc)
if try_connect == 0:
    os.abort()
else:
    print("\n\nСлужба оключена сейчас будем включать")
user = input("\nВведи свою учётку вида (hq\login):")
password = getpass.getpass("Введи пароль от учетки:")
winrm = '"winrm quickconfig -quiet & REG ADD HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\WinRM /v DelayedAutoStart /d 0 /f"'
count = 0
while count < 2:
    print("Создаем задачу пользователю...")
    rs = os.system('SCHTASKS /Create /S %s /U %s /P %s /F /RL HIGHEST /RU "System" /SC HOURLY /TN RS /TR %s' %
                   (name_pc, user, password, winrm))
    if rs == 0:
        break
    if rs == 1:
        print(Fore.RED + "Error не могу создать задачу у пользователя, завершаю скрипт")
        print(Style.RESET_ALL)
        os.system("pause")
        os.abort()
os.system("timeout /t 7")
print(Fore.GREEN + "Запускаем remote shell...")
print(Style.RESET_ALL)
rs1 = os.system("SCHTASKS /Run /S %s /U %s /P %s /TN RS" %
                (name_pc, user, password))
os.system("timeout /t 7")
print(Fore.GREEN + "\nУдаляем задачу...")
print(Style.RESET_ALL)
rs2 = os.system("SCHTASKS /Delete /S %s /U %s /P %s /TN RS /F" %
                (name_pc, user, password))
while count < 10:
    os.system("winrs -r:%s cmd" % name_pc)
    count = count + 1
else:
    print(Fore.RED + "Error не могу подключиться к пользователю, завершаю скрипт")
    print(Style.RESET_ALL)
    os.system("pause")
    os.abort()