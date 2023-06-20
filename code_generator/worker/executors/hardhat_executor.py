import os

import subprocess
import logging

logger = logging.getLogger(__name__)

class HardhatExecutor:
    def __init__(self, contracts_path):
        logger.info("HardhatExecutor::__init__ contracts_path=%s", contracts_path)
        self.contracts_path = contracts_path

    def setup(self):
        logger.info("HardhatExecutor::setup")


        p = subprocess.Popen(["npm", "install"], cwd=self.contracts_path)
        p.wait()

        logger.info("HardhatExecutor::setup npm install is done")

    def format(self):
        logger.info("HardhatExecutor::format")

        p = subprocess.Popen(["npm", "run", "prettier"], cwd=self.contracts_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

        if p.returncode == 0:
            return None

        return p.stderr.read().decode()

    def compile(self):
        logger.info("HardhatExecutor::compile")

        p = subprocess.Popen(["npm", "run", "compile"], cwd=self.contracts_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

        logger.info("HardhatExecutor::compile is done, status=%d", p.returncode)

        if p.returncode == 0:
            return None

        return p.stderr.read().decode()
