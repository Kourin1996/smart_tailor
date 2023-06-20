import re
import logging
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser

logger = logging.getLogger(__name__)

template = """You're an experienced smart contract developer.

You are asked to define up to 7 required functionalities of a smart contract for certain use case.

Use-case: {query}

{format_instructions}
"""

class Requirement(BaseModel):
    requirements: List[str] = Field(description="list of requirements")

def generate_requirements(query, requirements_path):
    logger.info('generate_requirements::requirements_path=%s, query=%s', query, requirements_path)

    model = OpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

    parser = PydanticOutputParser(pydantic_object=Requirement)
    fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=model)

    format_instructions = fixing_parser.get_format_instructions()
    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
        partial_variables={"format_instructions": format_instructions}
    )

    _input = prompt.format_prompt(query=query)

    print('prompt:\n{}'.format(_input.to_string()))

    output = model(_input.to_string())
    result = fixing_parser.parse(output)

    reqs = result.requirements

    reqs = [line if re.match(r'^[1-9]+\.\s+', line) is not None else "{}. {}".format(index + 1, line) for index, line in enumerate(reqs)]
    reqs = [line.rstrip('\n') for line in reqs if len(line.strip()) > 0]

    result_txt = '\n'.join(reqs)

    with open(requirements_path, "w") as f:
        f.write(result_txt)

    logger.info('generate_requirements completed')

    return result_txt
