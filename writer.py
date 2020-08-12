import queue, csv, threading

class AsyncCsvWriter(threading.Thread):

    def __init__(self, fname):
        threading.Thread.__init__(self)
        self.jobs = 0
        self.q = queue.Queue()
        self.csv = csv.writer(open("jobs.csv", "w"))

    def writerow(self, row):
        self.q.put(row)

    def run(self):
        while True:
            try:
                row = self.q.get(timeout=10)
                self.csv.writerow(row)
                self.jobs+=1
                print("Written "+str(self.jobs))
            except:
                break
