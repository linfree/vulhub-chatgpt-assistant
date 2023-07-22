import os

# openai api key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = "gpt-3.5-turbo-0613"

# 是否开启代理
IS_PORXY = True
HTTP_PROXY = 'http://127.0.0.1:1080'
HTTPS_PROXY = 'http://127.0.0.1:1080'

# docker server url
DOCKER_SERVER_URL = "tcp://localhost:2375"

# vulhub path