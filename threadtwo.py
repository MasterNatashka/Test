import re
import threading
import time
import subprocess


received_packages = re.compile(r"получено = (\d+)")
status = ("не доступен", "доступен с потерями", "доступен")

# функция проверки ip-адресов 
def ip_address(ip):
    # время начала отсчета выполнения функции
    t0 = time.time_ns()
    # Запуск команды безопасным способом (списком аргументов)
    result = subprocess.run(
        ['ping', '-n', '2', '-w', '200', ip], capture_output=True, encoding='cp866'
        )
    # Поиск регулярного выражения сразу во всем тексте вывода
    n_received = received_packages.findall(result.stdout)
    print(f'{ip}: {status[int(n_received[0])]} | время выполнения {(time.time_ns() - t0) / 10**9:.2f} с')

#запуск параллельного поиска ip-адресов
def ip_end():
    # Создаем объекты потоков
    thread1 = threading.Thread(target=ip_address, args=("192.168.0.1",))
    thread2 = threading.Thread(target=ip_address, args=("192.168.0.2",))
    
    # Запускаем выполнение потоков
    thread1.start()
    thread2.start()

    # Ожидание завершения потоков главным потоком программы
    thread1.join()
    thread2.join()

ip_end()

print('Основная программа успешно завершена!')
    
