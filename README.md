# Ethereum Phishing Account Transaction Network Dataset

## Overview
This repository contains a comprehensive transaction network dataset of Ethereum phishing accounts and their associated transaction counterparts. The dataset is constructed through systematic crawling of blockchain transaction records using the Etherscan API, starting from 7,057 known phishing addresses. A breadth-first search (BFS) algorithm with 2-hop network expansion is implemented to capture multi-level transaction relationships. The dataset provides two data versions:  
1) **Edge-truncated version** retaining the first 100 transactions per account  
2) **Complete version** with no transaction count limitations.

## Dataset Characteristics

### Network Structure
- **Seed nodes**: 7,057 verified phishing addresses (Layer 0)  
- **1-hop neighbors**: Direct transaction counterparties (Layer 1)  
- **2-hop neighbors**: Secondary transaction counterparties (Layer 2)  

### Data Schema
Each address is stored as a CSV file containing the following fields:

| Column       | Type    | Description                  |
|--------------|---------|------------------------------|
| timestamp    | int64   | UNIX epoch time              |
| tx_hash      | string  | Transaction hash             |
| from         | string  | Sender address               |
| to           | string  | Receiver address             |
| value        | float64 | Transferred ETH value        |
| gas_used     | int64   | Gas consumption              |
| gas_price    | int64   | Gas price in Wei             |
| block_number | int64   | Containing block height      |

## Data Acquisition

### Automated Crawling System
- **BFS implementation**: Network expansion with configurable hop distance (`k=2`)  
- **Recursive storage**:

```
/data
├── <address_1>.csv
├── <address_1>
│   ├── <neighbor_a>.csv
│   └── <neighbor_a>
│       ├── <2-hop_neighbor_x>.csv
│       └── ...
├── <address_2>.csv
```

- **Rate limiting**: Compliant with Etherscan API throttling policies (5 requests/sec)

## Data Availability

Three dataset variants are provided:

1. [Phishing Accounts Full Records]([URL](https://drive.google.com/file/d/1p0j8Ex7CJAcaqrc6Zmfqv0MJhOtvxLex/view?usp=sharing)) – Complete transaction history of seed phishing addresses  
2. [2-hop Network (Truncated)]([URL](https://drive.google.com/file/d/1SBw_FM-FrhrDelNxgT7Q5B-zg_SxUzYj/view?usp=sharing)) – First 100 transactions per 2-hop node  
3. [2-hop Network (Unlimited)]([URL](https://drive.google.com/file/d/1qnauJQisZ_M776kpVq9ompflJP9r81Fz/view?usp=sharing)) – Full transaction records without truncation

## Repository Structure

```
├── src/
│   ├── one_acquisition.py       # Single address data collector
│   └── k_order.py               # Batch k-hop network crawler
├── config.py                    # API key configuration
├── requirements.txt             # Python dependencies
└── data/                        # Default storage directory
```

## Usage Instructions

### Environment Setup

```bash
pip install -r requirements.txt
```

Add your Etherscan API key to the environment:

```bash
export ETHERSCAN_API_KEY="your_api_key"
```

Or set it directly in `config.py`.

### Data Collection

**Single address acquisition:**

```bash
python one_acquisition.py
```

**Batch processing (k-hop network):**

```bash
python k_order.py
```
