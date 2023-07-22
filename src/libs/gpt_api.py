# 对openai的接口的封装
import os
import openai
import json
import copy
from config import (
    OPENAI_API_KEY,
    IS_PORXY,
    HTTP_PROXY,
    HTTPS_PROXY,
    DEFAULT_MODEL,
)


from libs.plugin_functions import (
    start_base_app_container,
    stop_vul_container,
    start_vul_container,
    FUNCTIONS,
)


# 从环境变量中获取openai的api key
openai.api_key = OPENAI_API_KEY
VUL_FUNCTIONS = FUNCTIONS
COMMON_MESSAGES = [
    {"role": "system", "content": "你是一个安全助手，你可以通过调用函数帮我启动和关闭漏洞容器和基础容器，你可以通过调用函数帮我获取漏洞验证文档"},
]
# http代理
if IS_PORXY:
    os.environ['HTTP_PROXY'] = HTTP_PROXY
    os.environ['HTTPS_PROXY'] = HTTPS_PROXY


# 将上面的示例代码改造成可以传入消息参数和function参数的类
class GPTAPI:

    def __init__(self, api_key: str, functions: list, model: str = "gpt-3.5-turbo-0613"):
        self.api_key = api_key
        self.functions = functions
        self.model = model
        openai.api_key = api_key

    def run_conversation(self, message):
        """对话函数，根据用户消息调用openai的api返回回复消息，
        如果需要调用函数则调用函数返回函数的返回值，
        再次调用openai的api返回回复消息

        Args:
            messages (_type_): _description_

        Returns:
            second_response (_type_): _description_
        """
        messages = copy.deepcopy(COMMON_MESSAGES)
        messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=self.functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            available_functions = {
                "start_base_app_container": start_base_app_container,
                "stop_vul_container": stop_vul_container,
                "start_vul_container": start_vul_container
            }

            function_name = response_message["function_call"]["name"]
            fuction_to_call = available_functions[function_name]
            function_args = response_message["function_call"]["arguments"]
            function_args = json.loads(function_args)
            # print(function_args)
            function_response = fuction_to_call(**function_args)
            function_response = json.dumps(function_response)

            messages.append(response_message)
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )
            return second_response        
        return response


if __name__ == "__main__":
    gpt = GPTAPI(OPENAI_API_KEY, VUL_FUNCTIONS, DEFAULT_MODEL)
    print(gpt.run_conversation("帮我关闭struts2漏洞容器"))
