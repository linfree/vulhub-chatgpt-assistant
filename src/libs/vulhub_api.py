import os
import json


# vulhub项目的路径
VULHUB_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "vulhub", "vulhub")
# 基础容器的目录名称
BASE_CONTAINER_DIR = "base"


class VulhubApi(object):
    """
    vulhub项目的api
    vuls: 漏洞列表，格式为：{"app_name+cve_id": {app_name: "", vul_id: "", build_file: "", markdown: ""}} 方便查询
    base_apps: 基础容器列表，格式为：{"app_name+version": {app_name: "", version: "", dockerfile: ""}} 方便查询
    """

    vuls = {}
    base_apps = {}

    def __init__(self):
        self.vuls = self.__init_vuls()
        self.base_apps = self.__init_base_apps()

    def __init_vuls(self):
        """
        初始化vuls
        """
        vuls = {}
        for app_name in os.listdir(VULHUB_PATH):
            # 过滤掉隐藏文件和基础容器的目录
            if app_name.startswith(".") or app_name == BASE_CONTAINER_DIR:
                continue
            if not os.path.isdir(os.path.join(VULHUB_PATH, app_name)):
                continue
            for vul_id in os.listdir(os.path.join(VULHUB_PATH, app_name)):
                vul_path = os.path.join(VULHUB_PATH, app_name, vul_id)
                if vul_id.startswith(".") or not os.path.isdir(vul_path):
                    continue
                # 校验漏洞id的目录中是否有docker-compose.yml文件
                if not os.path.exists(os.path.join(vul_path, "docker-compose.yml")):
                    # print(f"漏洞id: {app_name}--{vul_id}的目录中没有docker-compose.yml文件")
                    continue
                # 判断漏洞id的目录中是否有README-zh.md文件，没有再判断是否有README.md文件，都没有markdown文件则为none
                markdown_path = os.path.join(vul_path, "README.zh-cn.md")
                if not os.path.exists(markdown_path):
                    markdown_path = os.path.join(vul_path, "README.md")
                if not os.path.exists(markdown_path):
                    markdown_path = None
            
                vuls[f"{app_name}{vul_id}"] = {
                    "app_name": app_name,
                    "vul_id": vul_id,
                    "build_file": os.path.join(VULHUB_PATH, app_name, vul_id, "docker-compose.yml"),
                    "markdown_file": markdown_path
                }
        return vuls

    def __init_base_apps(self):
        """
        初始化base_apps
        """
        base_apps = {}
        base_path = os.path.join(VULHUB_PATH, BASE_CONTAINER_DIR)
        for app_name in os.listdir(base_path):

            app_path = os.path.join(base_path, app_name)
            if app_name.startswith(".") or not os.path.isdir(app_path):
                continue
            for version in os.listdir(app_path):
                
                app_version_path = os.path.join(app_path, version)
                if version.startswith(".") or not os.path.isdir(app_version_path):
                    continue
                # 如果有Dockerfile文件则为基础容器
                if not os.path.exists(os.path.join(app_version_path, "Dockerfile")):
                    continue

                base_apps[f"{app_name}{version}"] = {
                    "app_name": app_name,
                    "version": version,
                    "dockerfile": os.path.join(app_version_path, "Dockerfile")
                }
        return base_apps
    
    def search_vul(self, app_name=None, cve_id=None):
        """
        根据应用名称或者cve_id查询漏洞
        """
        if not app_name and not cve_id:
            return None
        if cve_id:
            for vul_id in self.vuls.keys():
                if cve_id.lower() in vul_id.lower():
                    return self.vuls[vul_id]
        if app_name:
            for vul_id in self.vuls.keys():
                if app_name.lower() in vul_id.lower():
                    return self.vuls[vul_id]
        return None
    
    def search_base_app(self, app_name, version=None):
        """
        根据应用名称和版本号查询基础容器
        """
        if not app_name and not version:
            return None
        if version:
            candidate_app = [app for app in self.base_apps.keys() if app_name.lower() in app.lower()]
            for app in candidate_app:
                app_info = self.base_apps[app]
                if app_info["version"].lower().replace(app_info["app_name"].lower(), "").startswith(version.lower()):
                    return app_info
                    
        else:
            for app in self.base_apps.keys():
                if app_name.lower() in app.lower():
                    return self.base_apps[app]

        return None



if __name__ == "__main__":

    # test
    vulhub_api = VulhubApi()
    print(vulhub_api.search_vul(app_name="struts2", cve_id="S2-045"))
    print(vulhub_api.search_base_app(app_name="tomcat", version="6"))