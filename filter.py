import threading, queue
from writer import AsyncCsvWriter

class AsyncFilter(threading.Thread):

    EOF = ()

    FORBIDDEN_TITLE = [
        "lead",
        "senior",
        "sr",
        "staff",
        "chief",
        "vp",
        "manager",
        "director",
        "principal",
        "ii", "iii", "iv", "v", "vi",
        "mid",
        "intermediate",
        "advanced",
        "master",
        "ms",
        "principle"
    ]

    FORBIDDEN_BODY = [
        "masters",
        "ms",
        "master",
        "lead",
        "senior",
        "sr",
        "staff",
        "chief",
        "vp",
        "manager",
        "director",
        "principal"
    ]

    def __init__(self, writer, logger):
        threading.Thread.__init__(self)
        self.q = queue.Queue()
        self.writer = writer
        self.logger = logger
        self.num_filtered = 0
        self.seen = set([])

    def queue_job(self,job):
        self.q.put(job)

    def filter(self,job):
        if (job.title, job.comp, job.loc) in self.seen:
            return False
        if any([i in job.title.lower() for i in AsyncFilter.FORBIDDEN_TITLE]):
            return False
        #if any([i in job.desc.lower() for i in AsyncFilter.FORBIDDEN_BODY]):
        #    return False
        #if "years" in job.desc.lower() and "experience" in job.desc.lower():
        #    return False
        self.seen.add((job.title, job.comp, job.loc))
        return True

    def run(self):
        while True:
            top = self.q.get()
            if top is AsyncFilter.EOF:
                self.writer.writerow(AsyncCsvWriter.EOF)
                break
            if self.filter(top):
                top.write_to_csv(self.writer)
            self.num_filtered += 1
            self.logger.info("Filtered "+str(self.num_filtered))
