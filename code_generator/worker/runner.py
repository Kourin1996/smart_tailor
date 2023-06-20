import os
import json
import logging
import shutil
import re

from worker.executors.hardhat_executor import HardhatExecutor
from worker.executors.react_executor import ReactExecutor
from worker.prompts.requirements_planner.prompt import generate_requirements
from worker.prompts.specification_designer.prompt import generate_specification
from worker.prompts.solidity_template_builder.prompt import generate_solidity_template
from worker.prompts.solidity_fixer.prompt import fix_solidity_code
from worker.prompts.react_template_builder.prompt import generate_react_template

logger = logging.getLogger(__name__)

next_project_root = os.path.abspath(os.path.join(os.getcwd(), "site_generator"))
contract_template_path = os.path.abspath(os.path.join(os.getcwd(), "templates/contracts"))
app_template_path = os.path.abspath(os.path.join(os.getcwd(), "templates/app"))

class Runner:
    def __init__(self, redis, id, project_root):
        logger.info("Runner::__init__ projectRoot=%s", project_root)
        self.project_root = project_root
        self.id = id
        self.redis = redis

        self.contracts_path = os.path.join(self.project_root, "contracts")
        self.app_path = os.path.join(self.project_root, "app")
        self.hardhat = HardhatExecutor(self.contracts_path)
        self.react = ReactExecutor(self.app_path)

    def get_record(self):
        raw_value = self.redis.get(self.id)
        if raw_value is None:
            return None

        decoded = raw_value.decode()

        print('load by {}'.format(self.id), decoded)

        return json.loads(decoded)

    def save_record(self, new_record):
        print('save into {}'.format(self.id), new_record)

        self.redis.set(self.id, json.dumps(new_record))

    def update_status(self, new_status):
        record = self.get_record()
        if record is not None:
            record['status'] = new_status
            self.save_record(record)
            logger.info('updated status id=%s, new_status=%s', self.id, new_status)

    def save_code_to_record(self, contract_path, react_path, contract_build_error):
        react_build_error = self.react.compile()
        solidity_abi = self.load_abi(has_bytecode=True, has_deployed_bytecode=False)

        solidity_code = ''
        with open(contract_path, 'r') as f:
            solidity_code = f.read()

        react_code = ''
        with open(react_path, 'r') as f:
            react_code = f.read()

        solidity_build_result = contract_build_error if contract_build_error is not None else ''
        react_build_result = react_build_error if react_build_error is not None else ''

        record = self.get_record()
        if record is not None:
            record['status'] = 'COMPLETE'
            record['solidity_code'] = solidity_code
            record['react_code'] = react_code
            record['solidity_abi'] = solidity_abi
            record['solidity_build_result'] = solidity_build_result
            record['react_build_result'] = react_build_result
            self.save_record(record)
            logger.info('saved codes to DB id=%s', self.id)


    def clone_contracts(self, contracts_path):
        logger.info("Runner::clone_contracts")
        shutil.copytree(contract_template_path, contracts_path)
        logger.info("Runner::clone_contracts copied template contract project")

    def clone_apps(self, apps_path):
        logger.info("Runner::clone_apps")
        shutil.copytree(app_template_path, apps_path)
        logger.info("Runner::clone_apps copied template app project")

    def setup(self):
        logger.info("Runner::setup")

        os.mkdir(self.project_root)

        logger.info("Runner::setup directory created")

        self.clone_contracts(self.contracts_path)
        self.clone_apps(self.app_path)

        logger.info("Runner::setup project is ready")

    def load_abi(self, has_bytecode = False, has_deployed_bytecode = False):
        artifacts_path = os.path.join(self.contracts_path, "artifacts/src/Main.sol")
        for path in os.listdir(artifacts_path):
            file_path = os.path.join(artifacts_path, path)
            if os.path.isfile(file_path) and not path.endswith('.dbg.json'):
                abi_path = file_path

        logger.info('ABI path: %s', abi_path)

        with open(abi_path, "r") as f:
            abi = json.loads(f.read())

        if "bytecode" in abi and has_bytecode is False:
            abi.pop("bytecode")
            logger.info("remove bytecode from ABI")

        if "deployedBytecode" in abi and has_deployed_bytecode is False:
            abi.pop("deployedBytecode")
            logger.info("remove deployedBytecode from ABI")

        return json.dumps(abi)

    # Returns str or None
    def compile_hardhat(self):
        self.hardhat.format()
        return self.hardhat.compile()

    # Returns str or None
    def compile_react(self):
        return self.react.compile()

    def upload_to_next(self, id, react_component_path):
        page_dir_path = os.path.join(next_project_root, "src/pages/{}".format(id))
        page_file_path = os.path.join(page_dir_path, "index.jsx")
        logger.info('upload react component to Next.js id=%s, react_component_path=%s', id, react_component_path)

        if not os.path.exists(page_dir_path):
            os.mkdir(page_dir_path)

        shutil.copyfile(react_component_path, page_file_path)

        current_code = ''
        with open(page_file_path, "r") as f:
            current_code = f.read()

        new_code = "import withNoSSR from '../../../utils/nossr';\n" + current_code
        captured = re.search(r"export default (\w+)", new_code)

        logger.info("export default is found")

        component_name = captured.group(1)
        new_code = re.sub(r"export default \w+", 'export default withNoSSR({})'.format(component_name), new_code)

        with open(page_file_path, "w") as f:
            f.write(new_code)

        logger.info('overwrote file for Next.js')


    def execute(self, query):
        logger.info("Runner::execute query=%s", query)

        self.update_status('GENERATE_REQUIREMENTS')

        requirements_path = os.path.join(self.project_root, "requirements.txt")
        specification_path = os.path.join(self.project_root, "specifications.json")
        contract_path = os.path.join(self.contracts_path, "src/Main.sol")
        react_component_path = os.path.join(self.app_path, "src/App.js")

        requirements = generate_requirements(query, requirements_path)

        self.update_status('GENERATE_SPECIFICATIONS')

        specifications = generate_specification(query, requirements, specification_path)

        self.update_status('GENERATE_SOLIDITY')

        # Generate solidity code
        generate_solidity_template(self.hardhat, query, requirements, specifications, contract_path)

        self.hardhat.setup()
        self.hardhat.format()

        self.update_status('FIX_SOLIDITY')

        for i in range(10):
            compile_error = self.hardhat.compile()
            if compile_error is None:
                break

            print('fixing at {} times'.format(i))

            source_code = ''
            with open(contract_path, mode='r') as f:
                source_code = f.read()

            fix_solidity_code(query, requirements, specifications, source_code, compile_error, contract_path, min(0.1*i, 0.7))
            self.hardhat.format()

        self.hardhat.format()
        compile_error = self.hardhat.compile()
        if compile_error is not None:
            self.update_status('ERROR')
            raise Exception('failed to fix codes')

        self.update_status('GENERATE_REACT')

        self.react.setup()

        # Generate React application
        abi = self.load_abi(has_bytecode=False, has_deployed_bytecode=False)
        generate_react_template(query, abi, react_component_path)
        self.upload_to_next(self.id, react_component_path)

        self.save_code_to_record(contract_path, react_component_path, compile_error)




