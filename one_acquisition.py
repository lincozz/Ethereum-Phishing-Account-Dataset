import requests
import csv
from datetime import datetime
import time
import os

# 你的 Etherscan API 密钥
api_key = '13FTZ4KQGPIEEIFF5Y7VTG5SYQDWVCH7XA'

# 要查询的账户地址
account_address = '0x15e0fd25db971ce2951d5d2b20ac3ebf34525a3c'
# 0x49d42f74393e74b7acbce54a28dd0966a6449bfd

# 初始化页码和交易记录数量
page = 1
tx_per_page = 1000  # 每页最多获取1000条交易记录

# 确保 data/phishing 文件夹存在，如果不存在则创建
folder_path = 'data/phishing'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 指定文件保存路径为 data/phishing 目录下
csv_file_name = os.path.join(folder_path, f"{account_address}.csv")

# 创建 CSV 文件并写入表头
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
        # 构建 API 请求
        base_url = 'https://api.etherscan.io/api'
        api_endpoint = f'/?module=account&action=txlist&address={account_address}&startblock=0&endblock=99999999&page={page}&offset={tx_per_page}&sort=asc&apikey={api_key}'
        url = base_url + api_endpoint

        # 发送请求并获取响应
        response = requests.get(url)
        data = response.json()

        # 解析响应数据并写入 CSV 文件
        if data['status'] == '1' and len(data['result']) > 0:
            transactions = data['result']
            for tx in transactions:
                # 对 value、gas 和 gasPrice 进行格式化处理
                tx['value (ETH)'] = int(tx['value']) / 10 ** 18
                tx['gasPrice (Gwei)'] = int(tx['gasPrice']) / 10 ** 9
                del tx['value']
                del tx['gasPrice']

                writer.writerow(tx)
            # 增加页码，继续下一页数据的获取
            page += 1
        else:
            # 如果没有更多交易数据或API请求失败，结束循环
            break
print(f"交易数据已保存到 {csv_file_name}")
