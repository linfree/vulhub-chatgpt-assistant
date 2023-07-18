import json
import os
import sys
import time
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel


class VulInfo(BaseModel):
    """
    漏洞信息模型

    - app_name: 应用名称
    - cve_id: 漏洞编号或具体漏洞名称
    """
    app_name: str = None
    cve_id: str = None
    

# 开发一个chatgpt的插件，用于docker启动vulhub的容器。返回启动的容器的ip和端口信息
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/start_container")
async def start_container(vul_info: VulInfo):
    """
    通过应用名称或cve编号启动容器,返回容器的url和id信息
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - container_info: 容器的url(http://+ip+端口)和id信息
    """
    # 获取要启动的容器的docker-compose.yml文件
    # 通过应用名称或cve编号获取docker-compose.yml文件
    # 通过docker-compose.yml文件启动容器
    # 返回容器的ip和端口信息和容器id
    app_name = vul_info.app_name
    cve_id = vul_info.cve_id
    if not app_name and not cve_id:
        return {"code": 1, "message": "app_name or cve_id is required"}
    if cve_id:
        # 通过cve_id获取docker-compose.yml文件
        container_info = {"url": "http://<ip>:<port>", "id": "container_id"}
        pass
    if app_name:
        # 通过app_name获取docker-compose.yml文件
        container_info = {"url": "http://<ip>:<port>", "id": "container_id"}
        pass
    return {"code": 0, "message": "success", "container_info": container_info}


@app.get("/stop_container")
async def stop_container(container_id: str):
    """
    通过容器id停止容器
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
    """

    # 通过容器id停止容器
    stop_cmd = f"docker stop {container_id}"
    os.system(stop_cmd)
    return {"code": 0, "message": "success"}
    
    

@app.get("/get_vul_doc")
async def get_vul_doc(vul_info: VulInfo):
    """
    通过应用名称或cve编号获取漏洞文档
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - vul_doc: 漏洞验证文档url
    """
    # 通过应用名称或cve编号获取漏洞文档
    app_name = vul_info.app_name
    cve_id = vul_info.cve_id
    if not app_name and not cve_id:
        return {"code": 1, "message": "app_name or cve_id is required"}
    if cve_id:
        # 通过cve_id获取漏洞文档
        pass
    if app_name:
        # 通过app_name获取漏洞文档
        pass
    return {"code": 0, "message": "success", "vul_doc": "http://file.vulhub.org/xxx.pdf"}


