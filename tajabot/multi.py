from multiprocessing import Process, Queue, Array, Manager
import multiprocessing
from threading import Thread, Lock
import threading
import time
import pika
abc = 0
# define functions
def workerProcess(workerId, queue):
    print("inited worker Id : " + str(workerId))
    
    time.sleep(1)
    print(processList)

    while True:
        if queue.empty():
            continue
        data = queue.get()
        
        global abc
        #print('catch job worker id : ' + str(workerId) + ' thread count : ' + str(processList[workerId]['threadCount']))
        abc+=1
        thread = Thread(target = workerThread, args=(workerId, data))
        thread.start()
        

def workerThread(workerId, data):
    increaseThreadCount(workerId)
    
    threadId = threading.current_thread().ident

    print(processList)
    print('work job worker id : ' + str(workerId) + ' thread count : ' + str(processList[workerId]['threadCount']) + ' ' + data)
    time.sleep(10)
    
    decreaseThreadCount(workerId)
    return

def increaseThreadCount(workerId):
    lock.acquire()
    processList[workerId]['threadCount'] = processList[workerId]['threadCount'] + 1
    lock.release()

def decreaseThreadCount(workerId):
    lock.acquire()
    processList[workerId]['threadCount'] -= 1
    lock.release()

def getLazyWorkerId():
    workerId = 0
    threadCount = -1

    for processObject in processList:
        if processObject['threadCount'] > threadCount:
            workerId = processObject['workerId']
            threadCount = processObject['threadCount']

    return workerId

lock = Lock()

# init rabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='workqueue')


# multi processing

manager = Manager()

cpu_num = multiprocessing.cpu_count()
processList = manager.dict()

print("cpu num : " + str(cpu_num))
for i in range(cpu_num):
    queue = Queue()
    process = Process(target=workerProcess, args=(i,queue))
    processList[i] = {'workerId'     : i,
         'process'      : process,
         'threadCount'  : 0,
         'queue'        : queue}
    process.start()

# test code 
time.sleep(3)

for i in range(100):
    lazyWorkerId = getLazyWorkerId()
    processList[lazyWorkerId]['queue'].put('hello-'+str(i))
    print(abc)
    time.sleep(1)


