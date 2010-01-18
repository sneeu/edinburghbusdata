import Queue
import threading
import urllib2


SERVICE_MNEMONICS = '1,2,3,3A,4,5,7,8,10,11,12,14,15,15A,16,18,19,20,21,22,23,24,25,X25,26,X26,27,29,X29,30,31,X31,32,33,34,35,36,37,38,41,42,44,44A,45,47,X47,48,X48,49,61,67,69,100,109,N3,N8,N16,N22,N25,N26,N30,N31,N37,N44'
SERVICE_URL = 'http://mybustracker.co.uk/getServicePoints.php?serviceMnemo=%s'


def get_xml(*args):
    service = args[0]
    url = SERVICE_URL % service
    writer = open('data/%s.xml' % service, 'a')
    writer.write(''.join(urllib2.urlopen(url).readlines()))
    writer.close()


number_of_workers = 20
work_queue = Queue.Queue()


def worker():
    while True:
        item = work_queue.get()
        get_xml(*item)
        work_queue.task_done()


def main():
    for __ in range(number_of_workers):
         t = threading.Thread(target=worker)
         t.setDaemon(True)
         t.start()

    for item in SERVICE_MNEMONICS.split(','):
        work_queue.put([item])

    work_queue.join()


if __name__ == '__main__':
    main()
