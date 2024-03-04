# 北商 Python 入門助教


## 本地執行

> 安裝需求
- Python >= 3.12.1
- poetry >= 1.6.1

### 下載專案

```bash
$ git clone https://github.com/JiaWeiXie/ntub-python-assistant.git
$ cd ntub-python-assistant
```

### 設定執行環境

```bash
$ poetry install
$ poetry shell
```

### 執行

```bash
$ streamlit run main.py
```

## 安裝及部署

> 安裝需求
- Docker
- Docker Compose

### 下載專案

```bash
$ git clone https://github.com/JiaWeiXie/ntub-python-assistant.git
$ cd ntub-python-assistant
```

### 設定環境變數

1. 新增一個名為`.env`的檔案在`ntub-python-assistant`底下
2. 編輯`.env`檔案

```
OPENAI_API_KEY=<你的 OpenAI API Key>
OPENAI_ASSISTANT_ID=<你的 OpenAI Assistant ID>
```

### 建置

```bash
$ docker compose build
```

### 啟動

```bash
$ docker compose up -d
```