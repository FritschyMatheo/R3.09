import threading
import time

def task(i):
    print(f"Tâche {i} commence pour {i+1} seconde(s)")
    time.sleep(1)
    print(f"Tâche {i} terminée")

T = []

for i in range(10):
    T.append(threading.Thread(target=task, args=[i]))

if __name__ == "__main__":
    for i in range(len(T)):
        T[i].start()
    for i in range(len(T)):
        T[i].join()