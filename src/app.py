import json
import os
import sys
import time
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

from libs.vulhub_api import (
    get_vul_id_by_app_name,
    get_vul_id_by_app_name_or_cve_id,
    get_all_vul_id_list,
    get_base_app_list,
    get_base_app_dockerfile,
    BASE_APP_LIST,
    ALL_VUL_ID_LIST,
    VULHUB_PATH,
    BASE_CONTAINER_DIR,
)

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
async def start_vul_container(vul_info: VulInfo):
    """
    通过应用名称或cve编号启动有漏洞容器,返回容器的url和id信息
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - container_info: 容器启动的ip和端口信息和容器id
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
        vul_path = get_vul_id_by_app_name_or_cve_id(cve_id=cve_id)
        if not vul_path:
            return {"code": 1, "message": "cve_id is not exist"}

        # 通过cve_id获取docker-compose.yml文件
        container_info = {"ip": "<ip>", "id": "container_id",
                          f"{VULHUB_PATH}/{vul_path}/docker-compose.yml": ["<port1>", "<port2>"]}
        pass
    else:
        # 通过app_name获取docker-compose.yml文件
        vul_path = get_vul_id_by_app_name(app_name=app_name)
        container_info = {"ip": "<ip>", "id": "container_id",
                          f"{VULHUB_PATH}/{vul_path}/docker-compose.yml": ["<port1>", "<port2>"]}
        pass
    return {"code": 0, "message": "success", "container_info": container_info}

@app.get("/start_base_app_container")
async def start_base_app_container(app_name: str, version: str=None):
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
    # 通过应用名称和版本号获取基础容器的Dockerfile文件
    dockerfile_path = get_base_app_dockerfile(app_name=app_name, version=version)
    if not dockerfile_path:
        return {"code": 1, "message": "app_name or version is not exist"}
    # 通过Dockerfile文件构建基础容器
    # build_cmd = f"docker build -t {app_name}:{version} -f {dockerfile_path} ."
    # os.system(build_cmd)
    # 通过基础容器启动容器
    # run_cmd = f"docker run -d -p 80:80 {app_name}:{version}"
    # os.system(run_cmd)
    # 返回容器的ip和端口信息和容器id
    container_info = {"ip": "<ip>", "id": "container_id","path": dockerfile_path}
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
