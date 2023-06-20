import os

import subprocess
import logging

logger = logging.getLogger(__name__)

class ReactExecutor:
    def __init__(self, contracts_path):
        logger.info("ReactExecutor::__init__ contracts_path=%s", contracts_path)
        self.contracts_path = contracts_path

    def setup(self):
        logger.info("ReactExecutor::setup")

        p = subprocess.Popen(["npm", "install"], cwd=self.contracts_path)
        p.wait()

        logger.info("ReactExecutor::setup npm install is done")

    def compile(self):
        logger.info("ReactExecutor::compile")

        p = subprocess.Popen(["npm", "run", "build"], cwd=self.contracts_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

        logger.info("ReactExecutor::compile is done, status=%d", p.returncode)

        if p.returncode == 0:
            return None

        return p.stderr.read().decode()
