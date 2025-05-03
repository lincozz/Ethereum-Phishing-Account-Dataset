import requests
import csv
from datetime import datetime
import time
import os


api_key = '13FTZ4KQGPIEEIFF5Y7VTG5SYQDWVCH7XA'


account_address = '0x15e0fd25db971ce2951d5d2b20ac3ebf34525a3c'
# 0x49d42f74393e74b7acbce54a28dd0966a6449bfd


page = 1
tx_per_page = 1000 


folder_path = 'data/phishing'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


csv_file_name = os.path.join(folder_path, f"{account_address}.csv")


csv_columns = [
    'blockNumber', 'timeStamp', 'hash', 'nonce', 'blockHash', 'transactionIndex',
    'from', 'to', 'value (ETH)', 'gas', 'gasPrice (Gwei)', 'isError', 'txreceipt_status',
    'input', 'contractAddress', 'cumulativeGasUsed', 'gasUsed', 'confirmations',
    'methodId', 'functionName'
]
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()

    while True:

        base_url = 'https://api.etherscan.io/api'
        api_endpoint = f'/?module=account&action=txlist&address={account_address}&startblock=0&endblock=99999999&page={page}&offset={tx_per_page}&sort=asc&apikey={api_key}'
        url = base_url + api_endpoint


        response = requests.get(url)
        data = response.json()


        if data['status'] == '1' and len(data['result']) > 0:
            transactions = data['result']
            for tx in transactions:

                tx['value (ETH)'] = int(tx['value']) / 10 ** 18
                tx['gasPrice (Gwei)'] = int(tx['gasPrice']) / 10 ** 9
                del tx['value']
                del tx['gasPrice']

                writer.writerow(tx)

            page += 1
        else:

            break
print(f"交易数据已保存到 {csv_file_name}")
