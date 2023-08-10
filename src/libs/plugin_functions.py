"""
插件函数,提供给`gpt function calling`和app的api接口调用
提供启动容器和停止容器的功能，后续考虑提供容器的状态查询功能


"""
import os
import yaml
import docker


from libs.vulhub_api import (
    VULHUB_PATH,
    BASE_CONTAINER_DIR,
    VulhubApi
)

from config import (
    DOCKER_SERVER_URL,
    DOCKER_SERVER_REMOTE_IP
)
DOCKER_SERVER_IP = DOCKER_SERVER_REMOTE_IP

client = docker.DockerClient(base_url=DOCKER_SERVER_URL)


def start_vul_container(app_name: str = None, cve_id: str = None):
    """
    通过应用名称或cve编号启动有漏洞容器,返回容器的url和id信息
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - container_info: 容器启动的ip和端口信息和容器id
    """
    if not app_name and not cve_id:
        return {"code": 1, "message": "app_name or cve_id is required"}

    container_info = VulhubApi().search_vul(app_name=app_name, cve_id=cve_id)

    if not container_info:
        return {"code": 1, "message": "app_name or cve_id is not exist"}
    
    # 获取容器的docker-compose.yml文件，获取到port映射的信息
    docker_compose_file = container_info.get("docker_compose_file")
    print(docker_compose_file)
    docker_compose_info = yaml.load(open(docker_compose_file, "r", encoding="utf-8"), Loader=yaml.FullLoader)
    ports = []
    for service, info in docker_compose_info["services"].items():
        if "ports" in info:
            ports.extend(info["ports"])
    container_info["ports"] = ports
    container_info["url"] = [f"http://{DOCKER_SERVER_IP}:{port.split(':')[0]}" for port in ports]

    # TODO: 通过容器信息启动容器
    cmd = f"docker-compose -f {docker_compose_file} up -d"
    os.system(cmd)

    return {"code": 0, "message": "success", "container_info": container_info}


def stop_vul_container(app_name: str = None, cve_id: str = None):
    """
    通过应用名称或cve编号停止有漏洞容器
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
    """
    if not app_name and not cve_id:
        return {"code": 1, "message": "app_name or cve_id is required"}

    container_info = VulhubApi().search_vul(app_name=app_name, cve_id=cve_id)

    if not container_info:
        return {"code": 1, "message": "app_name or cve_id is not exist"}
    
    # 获取容器的docker-compose.yml文件，
    docker_compose_file = container_info.get("docker_compose_file")
    # 停止容器
    cmd = f"docker-compose -f {docker_compose_file} down"
    os.system(cmd)

    return {"code": 0, "message": "success"}

def start_base_app_container(app_name: str,version: str = None):
    """
    通过应用名称启动基础应用容器
    return:
        - code: 0表示成功，1表示失败
        - message: 返回的信息
        - container_info: 容器启动的ip和端口信息和容器id
    """
    if not app_name:
        return {"code": 1, "message": "app_name is required"}

    container_info = VulhubApi().search_base_app(app_name=app_name)

    if not container_info:
        return {"code": 1, "message": "app_name is not exist"}

    # 获取容器的Dockerfile文件，获取到port映射的信息
    dockerfile_path = container_info.get("dockerfile_path")
    print(dockerfile_path)
    # TODO: 通过容器信息启动容器
    tag = f"{app_name}:{container_info.get('version')}"
    image , logs = client.images.build(path=dockerfile_path,tag=tag)
    # print(image)
    # print(logs)
    container = client.containers.run(image=tag,detach=True)
    print(container)
    return {"code": 0, "message": "success", "container_info": container_info}


FUNCTIONS = [
    {
        "name": "start_vul_container",
        "description": "Starts a vulnerable container using either an application name or CVE ID. Returns the URL, ID, and other info of the container.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application",
                },
                "cve_id": {
                    "type": "string",
                    "description": "The ID of the CVE",
                }
            }
        }
    },
    {
        "name": "stop_vul_container",
        "description": "Stops a vulnerable container using either an application name or CVE ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application",
                },
                "cve_id": {
                    "type": "string",
                    "description": "The ID of the CVE",
                }
            }
        }
    },
    {
        "name": "start_base_app_container",
        "description": "Starts a base application container using the application name. Returns the URL, ID, and other info of the container.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application",
                },
                "version": {
                    "type": "string",
                    "description": "The version of the application",
                }
            },
            "required": ["app_name"]
        }
    }
]



if __name__ == "__main__":
    # print(start_vul_container(cve_id="CVE-2020-11981"))
    # print(stop_vul_container(cve_id="CVE-2020-11981"))
    print(start_base_app_container(app_name="tomcat",version="8.5.51"))

    
