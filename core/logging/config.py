import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

log_dir = 'error'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


log_file = os.path.join(log_dir, 'error.log')

handler = TimedRotatingFileHandler(
    log_file,
    when="midnight",
    interval=1,
    backupCount=30,
    encoding='utf-8'
)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 로거 설정
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.addHandler(handler)


def namer(name):
    return name.replace(".log", "") + "-" + datetime.now().strftime("%Y-%m-%d") + ".log"


handler.namer = namer