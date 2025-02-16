import sys
import os
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from engine.tool_framework.tool_runner import ToolRunner
from engine.tool_framework import simple_tool

from solders.keypair import Keypair
from eth_account import Account
from solders.keypair import Keypair
from eth_account import Account
import json

def generate_solana_keypair():
    keypair = Keypair()
    return str(keypair)

def generate_eth_keypair():
    account = Account.create()
    private_key = account.key.hex()
    return private_key



@simple_tool("Generate Keypair Tool")
def generate_keypair(type: str, num_keys: int):
    if(type !='solana' and type !='eth'):
        return 'Invalid type'
    private_keys = []
    for i in range(num_keys):
        private_key = ''
        if type == 'solana':
            private_key = generate_solana_keypair()
        elif type == 'eth':
            private_key = generate_eth_keypair()

        private_keys.append(private_key)
    return json.dumps(private_keys)


def main():
    tool = generate_keypair()
    runner = ToolRunner(tool)
    runner.run()


if __name__ == "__main__":
    main()
