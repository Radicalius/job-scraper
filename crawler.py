import logging
from handlers import *
from pipeline.writer import AsyncCsvWriter
from pipeline.worker import AsyncWorker
from pipeline.filter import AsyncFilter

logger = logging.getLogger("Crawler")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('jobfeed.log')
fh.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s/%(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

writer = AsyncCsvWriter("jobs.csv", logger)
writer.start()

filter = AsyncFilter(writer, logger)
filter.start()

AsyncWorker.logger = logger
AsyncWorker.filter = filter

logger.info("Beginning Ingestion")

tot_jobs = 0

for handler in handlers:

    jobs = 0

    logger.info("Scanning jobs from "+handler.type)

    AsyncWorker.create(20)

    try:
        h = handler()
        AsyncWorker.handler = h
        logger.info("Initialized handler successfully")
    except:
        logger.warn("Error while initializing handler", exc_info=True)
        continue

    try:
        pages = h.get_num_pages()
        logger.info("Found {0} pages of jobs".format(pages))
    except:
        logger.warn("Error while finding number of pages", exc_info=True)
        continue

    for page in range(pages):
        logger.info("Scanning page "+str(page))
        try:
            meta = h.scan_page(page)
            logger.info("Found {0} jobs".format(len(meta)))
        except:
            logger.warn("Error while scanning page "+str(page), exc_info=True)
            continue

        for i,job in enumerate(meta):
            AsyncWorker.queue_job(job)

    AsyncWorker.done()
    AsyncWorker.wait()

    logger.info("Finished scanning jobs from {0}; added {1} jobs".format(handler.type, jobs))

filter.queue_job(AsyncFilter.EOF)

logger.info("Ingestion Finished; added {0} jobs".format(tot_jobs))

requests.get("http://localhost:{0}/update".format(os.environ["PORT"]))
