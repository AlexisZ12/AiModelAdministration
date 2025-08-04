from pywebio.input import *
from pywebio.output import *
import os
import json

config_path = 'config/config.json'

def GetConfig():
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if not set(['ESURL', 'INDEX', 'KEY', 'BASE', 'PATH']).issubset(config.keys()):
                    toast("⚠️ 配置文件损坏，重新初始化配置", color='error')
                    config = ChangeConfig(config)
        else:
            toast("⚠️ 配置文件丢失，重新初始化配置", color='error')
            config = ChangeConfig(config)
    except json.JSONDecodeError:
        toast("⚠️ 配置文件损坏，使重新初始化配置", color='error')
        config = ChangeConfig(config)
    
    return config

def FormateConfig():
    os.makedirs('config', exist_ok=True)
    default_config = {
        'ESURL': 'http://localhost:9200',
        'INDEX': 'model',
        'KEY': 'your-api-key',
        'BASE': 'https://api.openai.com/v1',
        'PATH': './log'
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if not set(['ESURL', 'INDEX', 'KEY', 'BASE', 'PATH']).issubset(config.keys()):
                    toast("⚠️ 配置文件损坏，使用默认设置", color='error')
                    config = default_config
        else:
            toast("⚠️ 配置文件丢失，使用默认设置", color='error')
            config = default_config
    except json.JSONDecodeError:
        toast("⚠️ 配置文件损坏，使用默认设置", color='error')
        config = default_config
    
    return config

def ChangeConfig(config):
    config = input_group(
        "系统初始化设置",
        [
            input("ElasticSearch 地址", name="ESURL", value=config['ESURL']),
            input("索引名称", name="INDEX", value=config['INDEX']),
            input("API Key", name="KEY", type=PASSWORD, value=config['KEY']),
            input("Base URL", name="BASE", value=config['BASE']),
            input("导出文件路径", name="PATH", value=config['PATH']),
            checkbox(name="SAVE", options=[{"label": "保存这些设置", "value": "save", "selected": True}])
        ]
    )
    toast("✅ 配置文件修改成功！")
    if "save" in config['SAVE']:
        config.pop('SAVE')
        config['FIRST'] = False
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        toast("✅ 配置文件保存成功！")
    
    return config
def SetConfig():
    config = FormateConfig()
    return ChangeConfig(config)

def CheckFirst():
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('FIRST') is False
    
    return True