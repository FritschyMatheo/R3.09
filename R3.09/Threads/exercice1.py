import threading
import time

def task(i, x):
    for y in range(x):
        print(f"Je suis la thread {i}")
    time.sleep(0.1)


if __name__ == "__main__":
    start = time.perf_counter()
    t1 = threading.Thread(target=task, args=(1,5))
    t1.start()

    t2 = threading.Thread(target=task, args=(2,5))
    t2.start()

    t1.join()
    t2.join()
    
    end = time.perf_counter()
    print(f"Les tâches ont été exécutées en {round(end - start, 2)} seconde(s)")