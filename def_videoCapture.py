#def_videoCapture.py
'''
Разработка программы (прим.: с алгоритмом): Фасетка
Разработать программу с параллельной разработкой алгоритма, выполняющую задачу:
1. первая функция, проверка подключения и доступности камеры (и повторного (прим.: раз в 5 секунд) опроса камеры (прим.: проверка на подключение камеры);
2. вторая функция, определение количества подключённых видеокамер;
3. третья функция захват видеопотока с каждой камеры в отдельном потоке 
4. четвертая функция вывод видеопотока с ip камеры без детектирования объектов;
5. пятая функция, вывод видеопотока с каждой камеры в одном окне;
6. шестая функция, измерения времени методами: time.perf_counter(), time.process_time(), time.thread_time() (прим.: Энциклопедия Харриса/Python -> https://wiki.yandex.ru/homepage/otdel-razvitija-texnologijj/jenciklopedija-xarrisa/python/ )
алгоритм программы должен выполнять задачу следующими методами:
1. treading - многопточность;
2. multiprocessing - запуск нескольких параллельных процессов на CPU;
3. asyncio - асинхронное выполнение функций (прим.: задач)
время выполнения задачи нужно будет подсчитать в двух видах: глобальном; потоковом/процессном (прим.:(time.perf_counter_ns(), time.process_time(), time.thread_time())
При разработке, уровень готовности разработки, вести в соответсвии с таблицей 3 -> https://wiki.yandex.ru/homepage/otdel-razvitija-texnologijj/jenciklopedija-xarrisa/
'''
#повторный опрос на подключение камеры через 5 секунд
#вывод количества подключенных камер
#одно окно закрывается по кнопке "q", другое по кнопке "esc"
#вывод двух видеопотоков в одном окне
#вывод сообщения о не выводе потока
#время

# Импорт библиотек
import threading
import datetime
import time
import cv2
import numpy as np

""" Объявление глобальных переменных"""
# Переменная фиксирует значение отсчёта времени
t0 = time.perf_counter_ns()
# Переменная блокировки потока
lock = threading.Lock()
# Количество захваченных кадров
count_totalcadr=0
#
frames_dict={}

# 1 Функция проверка подключения и доступности камеры, и захват видеопотока с каждой камеры в отдельном потоке через функцию run_threads()
def video_stream(num_thread, url, window_name="Видеопоток с IP_камеры"):
    """
    Захватывает видеопоток в отдельное окно.
    :параметр num_thread: обозначает номер потока
    :параметр url: зазватывает видеопоток по url-адресу.
    :параметр window_name: Название графического окна.
    """
    # Инициализация источника видео
    cap = cv2.VideoCapture(url)

    # Если не установилась связь с видеопотоком, тогда выводим сообщение об ошибке соединения, иначе связь с источником видеопотока устанавливается и видеопоток запускается в окне
    if not cap.isOpened():
        print(f"Ошибка: Не удалось открыть Поток {num_thread} источника видео: {url}")
    #else:
        #print(f"Поток {num_thread} запущен. Нажмите 'q' для выхода")
        return
    print(f"Поток {num_thread} запущен. Нажмите 'q' для выхода")

    try:
        while True:
            with lock:
                # Последовательное считывание кадров
                ret, frame = cap.read()

                # Если кадр не получен, завершаем работу
                if not ret:
                    print("Видеопоток отпущен")
                    break

                # Вывод кадра на экран
                else:
                    global frames_dict
                    global count_totalcadr
                    count_totalcadr +=1
                    print(f"[Поток {num_thread}] |", count_totalcadr)
                    # Задаем размер кадра
                    #frame_size = (frame.shape[1] // 2, frame.shape[0] // 2)
                    frame_resized = cv2.resize(frame, (640,480))
                    # В словарь записан кадр
                    #frames_dict[num_thread]=frame_resized

                    cv2.imshow(window_name, frame_resized)

                # Отслеживание нажатия клавиши 'q' для закрытия окна с видеопотоком
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # Закрытия окна с видеопотоком через клавишу ESC. 27 - код клавиши ESC
                elif cv2.waitKey(1) & 0xFF == 27:
                    break

    finally:
        # Освобождение ресурсов
        cap.release()
        # Вывод времени затрачиваемого на [Поток №]
        print( f"[Поток {num_thread}] | время выполнения потока {times_end()}", count_totalcadr)

# 3 Функция формирования потоков в цикле, запуск потоков и ожидание завершения работы потока
def run_threads():
    threads = [
        threading.Thread(target=video_stream, args=(1, "rtsp://dhhe:ca4h5w@192.168.0.143:554/snl/live/1/2")),
        threading.Thread(target=video_stream, args=(2, 0, "Камера RTSP"))
    ]
    # Запуск потока
    for thread in threads:
        thread.start()

    #global frames_dict
    #while True:
    #    #cv2.imshow("window_name", frames_dict[1])
    #    if frames_dict.get(1) is not None:
    #        cv2.imshow("window_name", frames_dict[1])

    # Ожидание завершения работы потока
    for thread in threads:
        thread.join()

# 6 Функция подсчета затраченного времени от времени начала отсчета
def times_end():
    #global t0
    # Переменная, вычисляющая время интервала работы всех потоков
    seconds = (time.perf_counter_ns()-t0)/ 10**9
    # Преобразование формы записи времени для отображения в формате ч:мм:сс.мкс
    readable_time = str(datetime.timedelta(seconds=seconds))
    # Вывод времени затрачиваемого на все процессы
    return readable_time

# Точка входа в программу
if __name__=="__main__":

    # Вызов функции формирования потоков в цикле с передачей параметров 
    run_threads()
    #video_stream(1, url=0)
    #cv2.destroyAllWindows()
    # Вызов функции подсчета затраченного времени
    print(f"Время выполнения всех потоков {times_end()} секунд. Всего открыто кадров:", count_totalcadr)