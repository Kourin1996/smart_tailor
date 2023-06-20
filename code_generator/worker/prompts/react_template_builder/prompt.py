from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import logging

logger = logging.getLogger(__name__)

THEME="Collect money for charity and mint NFT to supporters"
ABI="""{{"_format":"hh-sol-artifact-1","contractName":"CharityNFTContract","sourceName":"worker/Test.sol","abi":[{{"inputs":[{{"internalType":"uint256","name":"_donationDeadline","type":"uint256"}},{{"internalType":"uint256","name":"_minDonation","type":"uint256"}},{{"internalType":"uint256","name":"_maxDonation","type":"uint256"}},{{"internalType":"address","name":"_charityAddress","type":"address"}}],"stateMutability":"nonpayable","type":"constructor"}},{{"anonymous":false,"inputs":[{{"indexed":true,"internalType":"address","name":"owner","type":"address"}},{{"indexed":true,"internalType":"address","name":"approved","type":"address"}},{{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"Approval","type":"event"}},{{"anonymous":false,"inputs":[{{"indexed":true,"internalType":"address","name":"owner","type":"address"}},{{"indexed":true,"internalType":"address","name":"operator","type":"address"}},{{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}}],"name":"ApprovalForAll","type":"event"}},{{"anonymous":false,"inputs":[{{"indexed":true,"internalType":"address","name":"from","type":"address"}},{{"indexed":true,"internalType":"address","name":"to","type":"address"}},{{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"Transfer","type":"event"}},{{"inputs":[{{"internalType":"address","name":"to","type":"address"}},{{"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"}},{{"inputs":[{{"internalType":"address","name":"owner","type":"address"}}],"name":"balanceOf","outputs":[{{"internalType":"uint256","name":"","type":"uint256"}}],"stateMutability":"view","type":"function"}},{{"inputs":[],"name":"donate","outputs":[],"stateMutability":"payable","type":"function"}},{{"inputs":[{{"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"getApproved","outputs":[{{"internalType":"address","name":"","type":"address"}}],"stateMutability":"view","type":"function"}},{{"inputs":[{{"internalType":"address","name":"_donor","type":"address"}}],"name":"getDonationAmount","outputs":[{{"internalType":"uint256","name":"","type":"uint256"}}],"stateMutability":"view","type":"function"}},{{"inputs":[{{"internalType":"address","name":"_donor","type":"address"}}],"name":"getNFTToken","outputs":[{{"internalType":"uint256","name":"","type":"uint256"}}],"stateMutability":"view","type":"function"}},{{"inputs":[],"name":"getTotalDonations","outputs":[{{"internalType":"uint256","name":"","type":"uint256"}}],"stateMutability":"view","type":"function"}},{{"inputs":[{{"internalType":"address","name":"owner","type":"address"}},{{"internalType":"address","name":"operator","type":"address"}}],"name":"isApprovedForAll","outputs":[{{"internalType":"bool","name":"","type":"bool"}}],"stateMutability":"view","type":"function"}},{{"inputs":[],"name":"name","outputs":[{{"internalType":"string","name":"","type":"string"}}],"stateMutability":"view","type":"function"}},{{"inputs":[{{"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"ownerOf","outputs":[{{"internalType":"address","name":"","type":"address"}}],"stateMutability":"view","type":"function"}},{{"inputs":[{{"internalType":"address","name":"from","type":"address"}},{{"internalType":"address","name":"to","type":"address"}},{{"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}},{{"inputs":[{{"internalType":"address","name":"from","type":"address"}},{{"internalType":"address","name":"to","type":"address"}},{{"internalType":"uint256","name":"tokenId","type":"uint256"}},{{"internalType":"bytes","name":"data","type":"bytes"}}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}},{{"inputs":[{{"internalType":"address","name":"operator","type":"address"}},{{"internalType":"bool","name":"approved","type":"bool"}}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"}},{{"inputs":[{{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}}],"name":"supportsInterface","outputs":[{{"internalType":"bool","name":"","type":"bool"}}],"stateMutability":"view","type":"function"}},{{"inputs":[],"name":"symbol","outputs":[{{"internalType":"string","name":"","type":"string"}}],"stateMutability":"view","type":"function"}},{{"inputs":[{{"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"tokenURI","outputs":[{{"internalType":"string","name":"","type":"string"}}],"stateMutability":"view","type":"function"}},{{"inputs":[],"name":"totalDonations","outputs":[{{"internalType":"uint256","name":"","type":"uint256"}}],"stateMutability":"view","type":"function"}},{{"inputs":[{{"internalType":"address","name":"from","type":"address"}},{{"internalType":"address","name":"to","type":"address"}},{{"internalType":"uint256","name":"tokenId","type":"uint256"}}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}}],"linkReferences":{{}},"deployedLinkReferences":{{}}}}"""

template = """You're an experienced React developer with knowledge of Smart Contract.

You are asked to implement a web page implemented by React to interact with a smart contract.
You can use ethers to call smart contract.
You are given use case and ABI of the smart contract.
You need to export a root component as default.
You need to style a page by inlined CSS.
You should embed given 'ABI' in the code.
You should implement all functions.
You must add input tag for contract address.

Usecase: {query}
ABI: {abi}

You need to return only JSX code and you don't need to explain.
"""


def generate_react_template(query, abi_str, react_component_path):
    logging.info("generate_react_template react_component_path=%s, query=%s, abi=%s", react_component_path, query, abi_str)

    prompt = PromptTemplate(
        template=template,
        input_variables=["query", "abi"],
    )

    model = OpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0.0)
    _input = prompt.format(
        query=query,
        abi=abi_str,
    )

    output = model(_input)
    print('output', output)

    with open(react_component_path, "w") as f:
        code = output
        if "```" in output:
            lines = output.splitlines()

            indecies = []
            for i, line in enumerate(lines):
                if "```" in line:
                    indecies.append(i)

            if len(indecies) != 2:
                raise Exception('invalid format!!')

            code = '\n'.join(lines[indecies[0] + 1:indecies[1]])

        f.write(code)



