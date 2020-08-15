import queue, threading
from filter import AsyncFilter

class AsyncWorker(threading.Thread):

    q = queue.Queue()
    logger = None
    filter = None
    handler = None

    EOF = ()
    workers = []

    @staticmethod
    def queue_job(meta):
        AsyncWorker.q.put(meta)

    @staticmethod
    def create(n):
        AsyncWorker.workers = [AsyncWorker() for i in range(n)]
        for i in AsyncWorker.workers:
            i.start()

    @staticmethod
    def done():
        for i in range(len(AsyncWorker.workers)):
            AsyncWorker.q.put(AsyncWorker.EOF)

    @staticmethod
    def wait():
        for i in AsyncWorker.workers:
            i.join()
        AsyncWorker.workers = []

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            meta = AsyncWorker.q.get()
            if meta is AsyncWorker.EOF:
                #AsyncWorker.filter.queue_job(AsyncFilter.EOF)
                break

            #AsyncWorker.logger.info("Scanning job")
            try:
                job = AsyncWorker.handler.scan_posting(meta)
                AsyncWorker.filter.queue_job(job)
            except:
                AsyncWorker.logger.warn("Error while scanning job", exc_info=True)
                continue
