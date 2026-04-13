<div align="center">

# 🏎️ AiModelAdministration

An intelligent collection management tool designed for racing model enthusiasts. Combining Elasticsearch search engine with OpenAI semantic understanding technology, it supports multi-dimensional categorization, intelligent retrieval (keyword/fuzzy/semantic), and Excel batch import/export, making your model collection management easier and more efficient.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.15-green.svg)](https://www.elastic.co/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-red.svg)](https://openai.com/)
[![PyWebIO](https://img.shields.io/badge/PyWebIO-Web%20UI-purple.svg)](https://pywebio.readthedocs.io/)
[![pandas](https://img.shields.io/badge/pandas-Data%20Processing-orange.svg)](https://pandas.pydata.org/)

[中文](README.md) | [English](README_EN.md)

</div>

---

## 🔍 Project Overview

**AiModelAdministration** is an open-source tool designed for racing model enthusiasts, combining Elasticsearch search engine with OpenAI semantic understanding technology to provide efficient and intelligent model collection management solutions. The system supports multi-dimensional categorization, intelligent retrieval, and batch data processing, making your model collection management effortless.

---

## ✨ Core Features
1. Comprehensive Inventory Management
- Full lifecycle management of model information (add, modify, query, delete)
- Built-in default model attributes (brand, scale, season, team, etc.)
- Custom field configuration to adapt to different collection needs
2. Intelligent Retrieval System
- Keyword Search: Precise lookup by specific attributes
- Fuzzy Search: Approximate matching with tolerance for input errors
- Semantic Search: Based on OpenAI vector embeddings, understands natural language query intent
3. Batch Data Processing
- Excel Template Import: Quickly batch add model data
- Data Export & Backup: Export inventory information to Excel
- Batch Status Filtering: View by status (in-stock/pre-order/cancelled/sold)
4. Flexible System Configuration
- Customizable Elasticsearch connection parameters
- Compatible with OpenAI and compatible API services (supports endpoint URL and API key configuration)
- Configurable data storage paths for convenient backup management
5. Two Usage Modes
- Default Mode: Use preset racing model attribute fields
- Custom Mode: Create your own field system based on personal needs

---

## 🛠️ Tech Stack
- Backend
  - Python 3.8+
  - Elasticsearch Python SDK
  - OpenAI Python SDK
- Interactive Interface
  - PyWebIO (for creating web interactive applications)

---

## 🚀 Feature Demonstration
1. Visual Database Initialization - Freely build your database format or use the default format  
<img src="pic/009.png" height="50%" width="50%"/>

2. Batch Data Entry via Excel - Import historical data with one click, painless platform migration  
<img src="pic/010.png" height="50%" width="50%" />

3. One-Click Registration - Register new models quickly and conveniently  
<img src="pic/011.png" height="50%" width="50%" />

4. Multiple Search Modes

- Keyword Search - Efficient (Traditional matching method, precise search)  
<img src="pic/012.png" height="50%" width="50%" />

- Fuzzy Search - Convenient (Fuzzy matching, supports spelling error correction)  
<img src="pic/013.png" height="50%" width="50%" />

- Semantic Search - Intelligent (e.g., searching "world champion" returns world champion models)  
<img src="pic/014.png" height="50%" width="50%" />

5. One-Click Edit - Find the model and click to modify  
<img src="pic/015.png" height="50%" width="50%" />

6. Excel Export - Easily backup your data

---

## 📦 Project Environment Deployment Guide

### Version Compatibility Notes (For Reference Only)

| Component | Tested Version | Compatibility Range |
|------|----------|----------|
| Elasticsearch | 8.15.0 | 8.x series |
| Python | 3.10 | ≥3.10 |
| IK Analyzer | 8.15.0 | Must strictly match ES major version |

> Important Notes  
> 1. IK Analyzer version must match the Elasticsearch major version  
> 2. Production environments should enable xpack security module  
> 3. Windows systems need to use PowerShell for Docker commands

### I. Elasticsearch Environment Deployment

#### ▎Option 1: Official Download (Recommended)

| Component | Download URL |
|------|----------|
| Elasticsearch | https://www.elastic.co/downloads/past-releases/elasticsearch-8-15-0 |
| IK Analyzer | https://release.infinilabs.com/analysis-ik/stable/elasticsearch-analysis-ik-8.15.0.zip |
| Kibana (Optional)| https://www.elastic.co/downloads/past-releases/kibana-8-15-0 |

#### ▎Option 2: Cloud Storage Download

| Platform | Download URL |
|----------|----------|
| Aliyun Drive | https://www.alipan.com/s/DSAeUFYeC11 |
| Quark Drive | https://pan.quark.cn/s/260c70bb004a |

#### ▎Option 3: Docker Containerized Deployment

**Elasticsearch Standalone Deployment**:

```bash
docker run -d --name elasticsearch \
  -p 127.0.0.1:9200:9200 \
  -p 127.0.0.1:9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms2g -Xmx2g" \
  -e "xpack.security.enabled=false" \
  -e "network.host=127.0.0.1" \
  -v ${LOCAL_DATA_PATH}/data:/usr/share/elasticsearch/data \
  -v ${LOCAL_DATA_PATH}/plugins:/usr/share/elasticsearch/plugins \
  -v ${LOCAL_DATA_PATH}/logs:/usr/share/elasticsearch/logs \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.0
```

**Elasticsearch + Kibana Combined Deployment**:

Create a dedicated network

```bash
docker network create es-net
```

Start Elasticsearch

```bash
docker run -d --name elasticsearch \
  --network es-net \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms2g -Xmx2g" \
  -e "xpack.security.enabled=false" \
  -v ${LOCAL_DATA_PATH}/data:/usr/share/elasticsearch/data \
  -v ${LOCAL_DATA_PATH}/plugins:/usr/share/elasticsearch/plugins \
  -v ${LOCAL_DATA_PATH}/logs:/usr/share/elasticsearch/logs \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.0
```

Start Kibana

```bash
docker run -d --name kibana \
  --network es-net \
  -p 5601:5601 \
  -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" \
  docker.elastic.co/kibana/kibana:8.15.0
```

> **Note**: Replace `${LOCAL_DATA_PATH}` with your actual storage path. Kibana default access URL: http://localhost:5601

### II. Python Environment Configuration

#### ▎Option 1: Conda Virtual Environment Deployment (Recommended)

Create a Python 3.10 virtual environment

```bash
conda create -n es python=3.10 -y
conda activate es
```

Install core dependencies

```bash
pip install elasticsearch==8.15.0 openai pandas openpyxl
```

For users in China, use Tsinghua mirror for faster download

```bash
pip install elasticsearch==8.15.0 openai pandas openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### ▎Option 2: Global Python Environment Installation

Ensure Python version ≥3.10
```bash
python --version
```

Install project dependencies
```bash
pip install elasticsearch==8.15.0 openai pandas openpyxl
```

For users in China, use Tsinghua mirror for faster download
```bash
pip install elasticsearch==8.15.0 openai pandas openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### III. ElasticSearch Configuration

For first-time use, you need to install the IK Analyzer plugin and make some settings. Below is an example initialization on MacOS.  
1. Extract elasticsearch and IK Analyzer plugin  
<img src="pic/001.png"  height="100" />
2. Rename the IK Analyzer extracted folder to `ik`  
<img src="pic/002.png"  height="100" />
3. Copy the IK Analyzer plugin to `elasticsearch-8.15.0/plugins` folder  
<img src="pic/003.png"  height="100" />
4. Start ElasticSearch, run the file `elasticsearch-8.15.0/bin/elasticsearch`  
<img src="pic/004.png"  height="100" />
5. On first run, you may see a verification warning. Click `Done`  
<img src="pic/005.png"  height="200" />
6. Go to `Settings` → `Privacy & Security` → `Security`  
<img src="pic/006.png"  height="150" />
7. Click `Open Anyway` → `Open Anyway`  
<img src="pic/007.png"  height="200" />
8. ElasticSearch will start in the terminal. Close it after the first startup
9. Open the configuration file `elasticsearch-8.15.0/config/elasticsearch.yml` and modify it as follows:

```yml
# Enable security features
xpack.security.enabled: false

xpack.security.enrollment.enabled: false

# Enable encryption for HTTP API client connections, such as Kibana, Logstash, and Agents
xpack.security.http.ssl:
  enabled: false
  keystore.path: certs/http.p12

# Enable encryption and mutual authentication between cluster nodes
xpack.security.transport.ssl:
  enabled: false
  verification_mode: certificate
  keystore.path: certs/transport.p12
  truststore.path: certs/transport.p12
```

```yml
# Allow HTTP API connections from anywhere
# Connections are encrypted and require user authentication
http.host: 127.0.0.1
```

10. Restart ElasticSearch, run the file `elasticsearch-8.15.0/bin/elasticsearch`  
<img src="pic/008.png"  height="200" />

---

## 🤝 Support & Contact

| Channel | Link |
|:----:|:-----|
| 📂 **GitHub** | [AlexisZ12/AiModelAdministration](https://github.com/AlexisZ12/AiModelAdministration) |
| 🎁 **Afdian** | [AlexisZ12](https://afdian.com/a/AlexisZ12) |
| 📧 **Email** | 2242809239@qq.com |
| 💬 **WeChat** | `Alexis_12_Z` |

---

<div align="center">

**If you find this project helpful, please give it a ⭐ Star to show your support!**

</div>
