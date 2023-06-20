from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
import json
from pydantic import BaseModel, Field
from typing import List
from collections import OrderedDict
import logging
from langchain.output_parsers import RetryOutputParser

logger = logging.getLogger(__name__)

template = """You're an experienced smart contract developer.

You are asked to design specifications of smart contract in Solidity for certain use case.
You must define all information defined in the schema like public_fields, public_functions, and view_functions of contract.

Use-case: {query}

Requirements: {requirements}

{format_instructions}
"""

class MyEncoder(json.JSONEncoder):
    def default(cls, o):
        # if isinstance(o, Enum):
        #     return o.to_record()
        if isinstance(o, ContractField):
            return o.to_record()
        elif isinstance(o, FunctionArgument):
            return o.to_record()
        elif isinstance(o, FunctionReturn):
            return o.to_record()
        elif isinstance(o, ContractFunction):
            return o.to_record()
        # elif isinstance(o, Struct):
        #     return o.to_record()
        elif isinstance(o, Contract):
            return o.to_record()
        elif isinstance(o, Specification):
            return o.to_record()

        return json.JSONEncoder.default(cls, o)

# class Enum(BaseModel):
#     name: str = Field(description="name of enum type")
#     values: List[str] = Field(description="list of enum values")
#
#     def to_record(cls):
#         return OrderedDict([
#             ('name', cls.name),
#             ('values', cls.values)
#         ])

class ContractField(BaseModel):
    name: str = Field(description="name of field")
    type: str = Field(description="type of field")

    def to_record(cls):
        return OrderedDict([
            ('name', cls.name),
            ('type', cls.type)
        ])

class FunctionArgument(BaseModel):
    name: str = Field(description="name of argument")
    type: str = Field(description="type of argument")

    def to_record(cls):
        return OrderedDict([
            ('name', cls.name),
            ('type', cls.type)]
        )

class FunctionReturn(BaseModel):
    type: str = Field(description="type of the value")

    def to_record(cls):
        return OrderedDict([
            ('type', cls.type)
        ])

class Constructor(BaseModel):
    arguments: List[FunctionArgument] = Field(description="arguments of the function")
    # returns: List[FunctionReturn] = Field(description="return values of the function")

    def to_record(cls):
        return OrderedDict([
            ('arguments', [c.to_record() for c in cls.arguments]),
            # ('returns', map(lambda c: c.to_record(), cls.returns))
        ])

class ContractFunction(BaseModel):
    name: str = Field(description="name of the function")
    arguments: List[FunctionArgument] = Field(description="arguments of the function")
    returns: List[FunctionReturn] = Field(description="return values of the function")
    assertions: List[str] = Field(description="conditions for the arguments and contract's states to meet inside the function")

    def to_record(cls):
        return OrderedDict([
            ('name', cls.name),
            ('arguments', [c.to_record() for c in cls.arguments]),
            ('returns', [c.to_record() for c in cls.returns]),
            ('assertions', cls.assertions)
        ])

# class Struct(BaseModel):
#     name: str = Field(description="name of the struct")
#     fields: List[ContractField] = Field(description="fields of the struct")
#
#     def to_record(cls):
#         return OrderedDict([('name', cls.name), ('fields', map(lambda c: c.to_record(), cls.fields))])

class Contract(BaseModel):
    name: str = Field(description="name of the contract")
    # inherits: List[str] = Field(description="parent classes or interfaces to be inherited by the contract")
    # enums: List[Enum] = Field(description="enum types to be defined in the contract")
    # structs: List[Struct] = Field(description="custom struct types to be defined in the contract")
    public_fields: List[ContractField] = Field(description="public fields in the contract")
    # private_fields: List[ContractField] = Field(description="private fields in the contract")
    # constructor: Constructor = Field(description="constructor of contract")
    public_functions: List[ContractFunction] = Field(description="public functions to be implemented in contract")
    view_functions: List[ContractFunction] = Field(description="view functions to be implemented in contract")
    # internal_functions: List[ContractFunction] = Field(description="private functions to be implemented")
    # private_functions: List[ContractFunction] = Field(description="internal functions to be implemented")

    def to_record(cls):
        return OrderedDict([
            ('name', cls.name),
            # ('inherits', cls.inherits),
            # ('enums', map(lambda c: c.to_record(), cls.enums)),
            # ('structs', map(lambda c: c.to_record(), cls.structs)),
            ('public_fields', [c.to_record() for c in cls.public_fields]),
            # ('private_fields', map(lambda c: c.to_record(), cls.private_fields)),
            # ('constructor', cls.constructor.to_record()),
            ('public_functions', [c.to_record() for c in cls.public_functions]),
            ('view_functions', [c.to_record() for c in cls.view_functions]),
            # ('internal_functions', map(lambda c: c.to_record(), cls.internal_functions)),
            # ('private_functions', map(lambda c: c.to_record(), cls.private_functions))
        ])

class Specification(BaseModel):
    name: str = Field(description="application name")
    # description: str = Field(description="application description")
    contract: Contract = Field(description="contract to be implemented")

    def to_record(cls):
        return OrderedDict([
            ('name', cls.name),
            # ('description', cls.description),
            ('contract', cls.contract.to_record()),
        ])

def generate_specification(query, requirements, specification_path):
    logger.info('generate_specification specification_path=%s, query=%s, requirements=%s', specification_path, query, requirements)

    model = OpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0.3)

    parser = PydanticOutputParser(pydantic_object=Specification)
    retry_parser = RetryOutputParser.from_llm(
        parser=parser, llm=OpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0.3)
    )

    prompt = PromptTemplate(
        template=template,
        input_variables=["query", "requirements"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    _input = prompt.format_prompt(
        query=query,
        requirements=requirements
    )

    for i in range(3):
        try:
            print('prompt:\n{}'.format(_input.to_string()))

            output = model(_input.to_string())

            result = retry_parser.parse_with_prompt(output, _input)

            json_result = result.to_record()

            with open(specification_path, "w") as f:
                f.write(json.dumps(json_result, indent=1))

            logger.info('generate_specification completed')

            return json.dumps(json_result)
        except Exception as e:
            logger.warning("generate_specification threw error")
            print(e)
            logger.info("retry generate_specification")

    raise Exception("reached retry limit in generate_specification!!")
