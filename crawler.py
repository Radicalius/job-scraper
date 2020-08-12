import logging
from handlers import *
from writer import AsyncCsvWriter

logger = logging.getLogger("Crawler")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('jobfeed.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s/%(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

writer = AsyncCsvWriter("jobs.csv")
writer.start()

logging.info("Beginning Ingestion")

tot_jobs = 0

for handler in handlers:

    jobs = 0

    logger.info("Scanning jobs from "+handler.type)

    try:
        h = handler()
        logger.info("Initialized handler successfully")
    except:
        logging.warn("Error while initializing handler", exc_info=True)
        continue

    try:
        pages = h.get_num_pages()
        logger.info("Found {0} pages of jobs".format(pages))
    except:
        logging.warn("Error while finding number of pages", exc_info=True)
        continue

    for page in range(pages):
        logger.info("Scanning page "+str(page))
        try:
            meta = h.scan_page(page)
            logging.info("Found {0} jobs".format(len(meta)))
        except:
            logging.warn("Error while scanning page "+str(page), exc_info=True)
            continue

        for i,job in enumerate(meta):
            logger.info("Scanning job "+str(i))
            try:
                job = h.scan_posting(job)
                job.write_to_csv(writer)
                jobs += 1
                tot_jobs += 1
            except:
                logging.warn("Error while scanning job "+str(i), exc_info=True)
                continue

    logger.info("Finished scanning jobs from {0}; added {1} jobs".format(handler.type, jobs))

logger.info("Ingestion Finished; added {0} jobs".format(tot_jobs))
