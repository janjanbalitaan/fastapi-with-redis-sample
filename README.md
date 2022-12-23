# FastAPI with Redis Implementation

FastAPI with Redis Implementation Sample using Python 3

## TODOs
* Automated Test Cases

## Requirements
* [Python 3.8.1](https://www.python.org/downloads/release/python-381)
* [Package Manager](https://pip.pypa.io/en/stable/)
* [Redis](https://redis.io/download/)

## Installation
* Create a virtual environment
```bash
python3 -m venv venv
```
* Enable the virtualenvironment
```bash
source venv/bin/activate
```
* Install libraries
```bash
pip install -r requirements.txt
```
* Create a environment variable file (rename/copy sample.env file to .env and update the values)
```bash
cp sample.env .env
```

## Usage
* Running the application
```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```
## API Documentation
* [Docs](http://localhost:8000/docs) - Swagger Documentation