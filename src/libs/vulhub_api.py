import os
import json

# vulhub项目的路径
VULHUB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","vulhub", "vulhub")
# 基础容器的目录名称
BASE_CONTAINER_DIR = "base"


def get_vul_app_list():
    """
    获取vulhub项目的列表
    """
    vulhub_list = []
    for app_name in os.listdir(VULHUB_PATH):
        if app_name.startswith(".") or app_name == BASE_CONTAINER_DIR:
            continue

        if os.path.isdir(os.path.join(VULHUB_PATH, app_name)):
            vulhub_list.append(app_name)
    return vulhub_list


def get_all_vul_id_list():
    """
    获取全部应用项目的漏洞id列表
    """
    vul_id_list = []
    for app_name in get_vul_app_list():
        app_path = os.path.join(VULHUB_PATH, app_name)
        for vul_id in os.listdir(app_path):
            if vul_id.startswith("."):
                continue
            if os.path.isdir(os.path.join(app_path, vul_id)):
                # 校验漏洞id的目录中是否有docker-compose.yml文件
                if not os.path.exists(os.path.join(app_path, vul_id, "docker-compose.yml")):
                    # print(f"漏洞id: {app_name}--{vul_id}的目录中没有docker-compose.yml文件")
                    continue
                vul_id_list.append(f"{app_name}/{vul_id}")
    return vul_id_list


def get_base_app_list():
    """
    获取基础容器的列表
    """
    base_app_list = []
    base_app_path = os.path.join(VULHUB_PATH, BASE_CONTAINER_DIR)
    for app_name in os.listdir(base_app_path):
        if app_name.startswith("."):
            continue
        for version in os.listdir(os.path.join(base_app_path, app_name)):
            if version.startswith("."):
                continue
            if os.path.isdir(os.path.join(base_app_path, app_name, version)):
                base_app_list.append(f"{app_name}{version}")
    return base_app_list




# 获取全部应用项目的漏洞id列表
ALL_VUL_ID_LIST = get_all_vul_id_list()
# 获取基础容器的列表
BASE_APP_LIST = get_base_app_list()


def get_vul_id_by_app_name_or_cve_id(app_name=None, cve_id=None):
    """
    根据应用名称或漏洞id找到对应的漏洞id的方法
    """
    if not app_name and not cve_id:
        return None

    if cve_id:
        for vul_id in ALL_VUL_ID_LIST:
            if cve_id.lower() in vul_id.lower():
                return vul_id
    if app_name:
        for vul_id in ALL_VUL_ID_LIST:
            if app_name.lower() in vul_id.lower():
                return vul_id
    return None


def get_vul_id_by_app_name(app_name):
    """
    根据应用名称找到对应的漏洞id的方法
    """
    if not app_name:
        return None
    for vul_id in ALL_VUL_ID_LIST:
        if app_name.lower() in vul_id.lower():
            return vul_id
    return None


def get_base_app_dockerfile(app_name, version=None):
    """
    根据应用名称和版本号获取基础容器的dockerfile
    """
    if not app_name and not version:
        return None
    for base_app in BASE_APP_LIST:
        if app_name.lower() in base_app.lower():
            if version:
                if version.lower() in base_app.lower():
                    return base_app
            else:
                return base_app
    return None

    # dockerfile_path = os.path.join(VULHUB_PATH, BASE_CONTAINER_DIR, app_name, version, "Dockerfile")

if __name__ == "__main__":

    # test
    print(get_vul_id_by_app_name_or_cve_id(cve_id="S2-045"))
    print(get_vul_id_by_app_name(app_name="struts2"))

    # test
    # print(get_vul_app_list())
    # print(get_all_vul_id_list())
    # print(get_base_app_list())