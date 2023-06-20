import logging
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.schema import BaseOutputParser, OutputParserException
from langchain.output_parsers import RetryOutputParser
from typing import Any

logger = logging.getLogger(__name__)

template = """You're an experienced smart contract developer.

You are asked to implement a smart contract for certain use case.
You are given use case, requirements, and specifications in JSON.
You must not implement smart contract.
You must implement all functions in the contract which meets the requirements and specifications.

Use-case: {query}

Requirements: {requirements}

Specifications: {specifications}

You need to return only Solidity code and you don't need to explain.
"""

def extract_codes(text):
    if "```" in text:
        lines = text.splitlines()

        indecies = []
        for i, line in enumerate(lines):
            if "```" in line:
                indecies.append(i)

        if len(indecies) != 2:
            raise OutputParserException(
                f"Failed to parse solidity from completion {text}. Got: code is not wrapped with {{}}"
            )

        return '\n'.join(lines[indecies[0] + 1:indecies[1]])
    else:
        return text


# class SolidityParser(BaseOutputParser[str]):
#     hardhat_executor: Any
#     solidity_file_path: str
#
#     def parse(self, text: str) -> str:
#         codes = extract_codes(text)
#         with open(self.solidity_file_path, "w") as f:
#             f.write(codes)
#
#         format_result = self.hardhat_executor.format()
#         # if format_result is not None:
#         #     raise OutputParserException(
#         #         f"Failed to parse Solidity from completion {text}. Got syntax errors: {format_result}"
#         #     )
#
#         compile_result = self.hardhat_executor.compile()
#         if compile_result is not None:
#             raise OutputParserException(
#                 f"Failed to parse Solidity from completion {text}. Got compile errors: {compile_result}"
#             )
#
#     @property
#     def _type(self) -> str:
#         return "solidity"

def generate_solidity_template(hardhat_executor, query, requirements, specifications, solidity_file_path):
    logger.info('generate_solidity_template solidity_file_path=%s, query=%s, requirements=%s, specifications=%s', solidity_file_path, query, requirements, specifications)

    prompt = PromptTemplate(
        template=template,
        input_variables=["query", "specifications", "requirements"],
    )

    model = OpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0)
    _input = prompt.format_prompt(
        query=query,
        requirements=requirements,
        specifications=specifications,
    )

    print('prompt:\n{}'.format(_input.to_string()))

    output = model(_input.to_string())

    with open(solidity_file_path, "w") as f:
        codes = extract_codes(output)
        f.write(codes)

    logger.info('generate_solidity_template completed')