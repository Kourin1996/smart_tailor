import os
import logging
from dotenv import load_dotenv
from celery import Celery
from worker.runner import Runner
import redis

red = redis.StrictRedis(host='localhost', port=6379, db=0)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

print('database for job queue', os.path.abspath(os.path.join(os.getcwd(), "database.json")))

app = Celery('tasks', broker='redis://localhost')

app.conf.update(
    result_expires=3600,
)

logger = logging.getLogger(__name__)

projects_path = os.path.abspath(os.path.join(os.getcwd(), "projects"))

@app.task
def start_project(id, query):
    project_root = os.path.join(projects_path, id)

    logger.info("start project id=%s, project_root=%s", id, project_root)

    try:
        runner = Runner(red, id, project_root)
        runner.setup()
        runner.execute(query)

        logger.info("finish project project project_root=%s", id)
    except Exception as e:
        logger.info("project failed id=%s, e=%s", id, str(e))

if __name__ == '__main__':
    app.start()