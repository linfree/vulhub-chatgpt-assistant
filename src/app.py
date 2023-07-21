import json
import os
import sys
import time
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


from libs.vulhub_api import (
    VULHUB_PATH,
    BASE_CONTAINER_DIR,
    VulhubApi,
)



class VulInfo(BaseModel):
    """
    漏洞信息模型

    - app_name: 应用名称
    - cve_id: 漏洞编号或具体漏洞名称
    """
    app_name: str = None
    cve_id: str = None


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # 渲染首页
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content
    

@app.get("/chat")
async def chat(request: Request):
    """
    前端post提问，后端通过调用openapi的接口获取答案后返回，如果需要调用function，可以在这里调用
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - answer: 答案
    """
    question = request.query_params.get("question")
    if not question:
        return {"code": 1, "message": "question is required"}
    

@app.get("/start_container")
async def start_vul_container(vul_info: VulInfo):
    """
    通过应用名称或cve编号启动有漏洞容器,返回容器的url和id信息
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - container_info: 容器启动的ip和端口信息和容器id
    """

    app_name = vul_info.app_name
    cve_id = vul_info.cve_id

    if not app_name and not cve_id:
        return {"code": 1, "message": "app_name or cve_id is required"}

    container_info = VulhubApi().search_vul(app_name=app_name, cve_id=cve_id)
    if not container_info:
        return {"code": 1, "message": "app_name or cve_id is not exist"}
    # TODO: 通过容器信息启动容器
    # docker_compose_file = os.path.join(BASE_CONTAINER_DIR, app_name, cve_id, "docker-compose.yml")
    # start_cmd = f"docker-compose -f {docker_compose_file} up -d"
    # os.system(start_cmd)

    return {"code": 0, "message": "success", "container_info": container_info}


@app.get("/start_base_app_container")
async def start_base_app_container(app_name: str, version: str = None):
    """
    通过应用名称和版本号获取基础容器的docker-compose.yml文件
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - container_info: 容器启动的ip和端口信息和容器id
    """
    # 通过应用名称和版本号获取基础容器的Dockerfile文件
    # 通过Dockerfile文件构建基础容器
    # 通过基础容器启动容器
    # 返回容器的ip和端口信息和容器id
    if not app_name and not version:
        return {"code": 1, "message": "app_name or version is required"}
    app_info = VulhubApi().search_base_app(app_name=app_name, version=version)
    if not app_info:
        return {"code": 1, "message": "app_name or version is not exist"}

    # TODO: 通过容器信息build容器,启动容器
    # docker_file = app_info.get("docker_file")
    # build_cmd = f"docker build -f {docker_file} -t {app_name}:{version} ."
    # os.system(build_cmd)
    return {"code": 0, "message": "success", "container_info": app_info}


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
    vul_doc = VulhubApi().search_vul(app_name=app_name, cve_id=cve_id)
    if not vul_doc:
        return {"code": 1, "message": "app_name or cve_id is not exist"}

    return {"code": 0, "message": "success", "vul_doc": vul_doc}

@app.get("/show_vul_md_file")
async def show_vul_md_file(vul_name: str):
    """
    通过应用名称或cve编号获取漏洞文档
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - vul_doc: 漏洞验证文档url
    """
    # 通过应用名称或cve编号获取漏洞文档
    vuls_dict = VulhubApi().vuls
    vul_info = vuls_dict.get(vul_name.lower(), None)
    if not vul_info:
        return {"code": 1, "message": "vul_name is not exist"}


    