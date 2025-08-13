from elasticsearch import Elasticsearch
from openai import OpenAI
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import start_server
import json
import UI
import Config
import Check
import Initialize
import Search
import Transform

def main():
    UI.MainUI()
    
    if not Config.CheckFirst():
        toast("⚡ 开始初始化配置文件...")
        config = Config.SetConfig()
    else:
        config = Config.GetConfig()
        
    es = Elasticsearch(config['ESURL'])
    index_name = config['INDEX']
    client = OpenAI(api_key=config['KEY'], base_url=config['BASE'])
    path = config['PATH']
    
    while True:
        if Check.CheckES(es) and Check.CheckOpenAi(client):
            break
        act = actions("", [{'label': '重新配置', 'color': 'warning','value':1}, {'label': '重试', 'value':0}])
        match act:
            case 0:
                continue
            case 1:
                config = Config.SetConfig()
                es = Elasticsearch(config['ESURL'])
                index_name = config['INDEX']
                client = OpenAI(api_key=config['KEY'], base_url=config['BASE'])
                path = config['PATH']
    
    if not es.indices.exists(index=index_name):
        Initialize.Initialize(es, index_name)
    
    with open('config/index.json', 'r', encoding='utf-8') as f:
        index_config = json.load(f)
    
    if index_config[-1]['style'] == 'default':
        head = ["ID", "品牌", "比例", "赛季", "车队", "型号", "车手", "车号", "分站", "名次", "状态", "入库时间", "购入价格", "卖出价格", "备注"]
        keyword = ["品牌", "比例", "赛季", "车队", "型号", "车手", "车号", "分站", "名次", "状态", "备注"]
        text = ["备注", "描述"]
        number = ["入库时间", "购入价格", "卖出价格"]
        style = 'default'
    else:
        head = ["ID",]
        keyword = []
        text = []
        number = []
        for field in index_config[1:-1]:
            head.append(field['name'])
            if field['type'] == 'text':
                keyword.append(field['name'])
                text.append(field['name'])
            elif field['type'] == 'keyword':
                keyword.append(field['name'])
            elif field['type'] == 'integer':
                number.append(field['name'])
        style = 'custom'
                
    head.append('操作')
    
    while True:
        UI.MainUI()
        menu = actions(buttons=[{'label': '📋 批量查找', 'value': 1}, {'label': '🔍 关键词检索', 'value': 2}, {'label': '✨ 模糊检索', 'value': 3},
                                {'label': '🤖 语义检索', 'value': 4}, {'label': '➕ 新增条目', 'value': 5}, {'label': '📥 导入数据', 'value': 6},
                                {'label': '📤 导出数据', 'value': 7}, {'label': '⚙️ 设置参数', 'value': 8},
                                {'label': '🚪 退出系统', 'value': 0, 'color': 'warning'}])
        
        match menu:
            case 0:
                clear()
                return
            
            case 1:
                clear()
                Search.BatchSearch(es, index_name, head, text, number, client, style)
            
            case 2:
                clear()
                Search.KeywordSearch(es, index_name, head, text, number, client, style, keyword)
            
            case 3:
                clear()
                Search.FuzzySearch(es, index_name, head, text, number, client, style)
                
            case 4:
                clear()
                Search.SemanticSearch(es, index_name, head, text, number, client, style)
            
            case 5:
                clear()
                Transform.InputOne(es, index_name, head, text, number, client, style)
            
            case 6:
                clear()
                Transform.InputData(es, index_name, head, text, client, style)
            
            case 7:
                clear()
                Transform.OutputData(es, index_name, head, style, path)
            
            case 8:
                clear()
                config = Config.SetConfig()
                es = Elasticsearch(config['ESURL'])
                index_name = config['INDEX']
                client = OpenAI(api_key=config['KEY'], base_url=config['BASE'])
                path = config['PATH']
                while True:
                    if Check.CheckES(es) and Check.CheckOpenAi(client):
                        break
                    act = actions("", [{'label': '重新配置', 'color': 'warning','value':1}, {'label': '重试', 'value':0}])
                    match act:
                        case 0:
                            continue
                        case 1:
                            config = Config.SetConfig()
                            es = Elasticsearch(config['ESURL'])
                            index_name = config['INDEX']
                            client = OpenAI(api_key=config['KEY'], base_url=config['BASE'])
                            path = config['PATH']
                
        
if __name__ == '__main__':
    main()