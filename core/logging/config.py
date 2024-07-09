import logging
import os
import queue
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler, QueueHandler, QueueListener


log_dir = os.path.join(os.getcwd(), 'error')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'error.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def namer(name):
    base_filename = os.path.basename(name)
    dir_name = os.path.dirname(name)
    date_str = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(dir_name, f"{os.path.splitext(base_filename)[0]}-{date_str}.log")


file_handler = TimedRotatingFileHandler(
    log_file,
    when="midnight",
    interval=1,
    backupCount=30,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)
file_handler.namer = namer


log_queue = queue.Queue(-1)
queue_handler = QueueHandler(log_queue)

root_logger = logging.getLogger()
root_logger.setLevel(logging.ERROR)  # 필요에 따라 DEBUG로 변경
root_logger.addHandler(queue_handler)


listener = QueueListener(log_queue, file_handler, respect_handler_level=True)
listener.start()


