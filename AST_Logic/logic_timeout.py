import time
import threading
import queue
# def funcuion1(name):
#     while (True):
#         print(threading.current_thread().getName() ," ",name)
#
#
# name_list = ['AA']
#
# t = threading.Timer()
# t.daemon = True
# t.start()
#
# class MultiThreading:
#
#     def __init__(self):
#         self.thread = None
#         self.started = True
#     def threaded_program(self):
#         while self.started:
#             print("running")
#             # time.sleep(10)
#     def run(self):
#         self.thread = threading.Thread(target=self.threaded_program, args=())
#         self.thread.start()
#     def stop(self):
#         self.started = False
#         self.thread.join()
#         print('Stop')
#
# t = MultiThreading()
# t.run()
# time.sleep(2)
# t.stop()


def doit(arg):
    t = threading.current_thread()
    while getattr(t, "do_run", True):
        print("working on %s" % arg)
        time.sleep(1)
    if(t.do_run == False):
        raise RuntimeError(t.getName() + ' ' + 'RuntimeError!!!')


def main():
    bucket = queue.Queue()
    try:
        t = threading.Thread(target=doit, args=("task",))
        t.start()
        print('A ',t.is_alive())
        time.sleep(5)
        t.do_run = False
        t.join()

    except RuntimeError:
        print('RuntimeError')

    finally:
        print('B ', t.is_alive())

if __name__ == "__main__":
    main()

















