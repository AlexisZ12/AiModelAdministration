from pywebio.input import *
from pywebio.output import *
import json
import math
import UI

def AssenblyData(EsResponse, size, head, style):
    data = []
    if style == 'default':
        for i in range(0, size):
            source = EsResponse['hits']['hits'][i]['_source']
            row = [source['ID'], source['品牌'], source['比例'], source['赛季'], source['车队'], source['型号'], source['车手'], source['车号'], source['分站'], source['名次'], source['状态'], source['入库时间'], source['购入价格'], source['卖出价格'], source['备注'], None]
            data.append(row)
        for i in range(0, 10):
            data.append(["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
    else:
        for i in range(0, size):
            source = EsResponse['hits']['hits'][i]['_source']
            row = []
            for each in head[:-1]:
                row.append(source[each])
            row.append(None)
            data.append(row)
        for i in range(0, 10):
            data.append(["" for i in range(len(head))])
    
    return data

def QuerryAll(es, index_name, head, style):
    search = {
        "query": {
            "match_all": {}
        },
        "sort": [{"ID": {"order": "asc"}}],
        "from": 0,
        "size": 10000,
    }
    response = es.search(index = index_name, body = search)
    size = response['hits']['total']['value']
    data = AssenblyData(response, size, head, style)
    
    return data, size

def QuerryAllRequired(es, index_name, head, style, requirement):
    search = {
        "query": {
            "term": {
                "状态": requirement
            }
        },
        "sort": [{"ID": {"order": "asc"}}],
        "from": 0,
        "size": 10000,
    }
    response = es.search(index = index_name, body = search)
    size = response['hits']['total']['value']
    data = AssenblyData(response, size, head, style)
    
    return data, size

def PageDeviceAll(es, index_name, head, text, number, client, style):
    data, size = QuerryAll(es, index_name, head, style)
    page = 0
    pagemax = math.ceil(size/10)
    
    while True:
        UI.ShowTable(es, index_name, head, text, number, client, style, page, data)
        action = actions("", [{'label': '⬅️ 上一页', 'value': 1}, {'label': '➡️ 下一页', 'value': 2}, {'label': '↩️ 返回批量查找菜单', 'value': 0, 'color': 'warning'}])
        
        match action:
            case 0:
                clear()
                break
            case 1:
                page = page - 1
                if page < 0:
                    page = 0
                clear()
            case 2:
                page = page + 1
                if page >= pagemax:
                    page = pagemax - 1
                clear()

def PageDeviceAllRequired(es, index_name, head, text, number, client, style, requirement):
    data, size = QuerryAllRequired(es, index_name, head, style, requirement)
    page = 0
    pagemax = math.ceil(size/10)
    
    while True:
        UI.ShowTable(es, index_name, head, text, number, client, style, page, data)
        action = actions("", [{'label': '⬅️ 上一页', 'value': 1}, {'label': '➡️ 下一页', 'value': 2}, {'label': '↩️ 返回批量查找菜单', 'value': 0, 'color': 'warning'}])
        
        match action:
            case 0:
                clear()
                break
            case 1:
                page = page - 1
                if page < 0:
                    page = 0
                clear()
            case 2:
                page = page + 1
                if page >= pagemax:
                    page = pagemax - 1
                clear()

def BatchSearch(es, index_name, head, text, number, client, style):
    if style == "default":    
        while True:
            UI.MainUI()
            BatchSearch = actions("", [{'label': '📋 查看全部', 'value':1}, {'label': '📦 查看入库', 'value':2}, {'label': '📅 查看预售', 'value':3}, {'label': '❌ 查看退订', 'value':4}, {'label': '💰 查看已售', 'value':5}, {'label': '↩️ 返回主菜单', 'value': 0, 'color': 'warning'}])

            match BatchSearch:
                case 0:
                    clear()
                    break
                
                case 1:
                    clear()
                    PageDeviceAll(es, index_name, head, text, number, client, style)
                    
                case 2:
                    clear()
                    PageDeviceAllRequired(es, index_name, head, text, number, client, style, "入库")
            
                case 3:
                    clear()
                    PageDeviceAllRequired(es, index_name, head, text, number, client, style, "预购")
            
                case 4:
                    clear()
                    PageDeviceAllRequired(es, index_name, head, text, number, client, style, "退订")
            
                case 5:
                    clear()
                    PageDeviceAllRequired(es, index_name, head, text, number, client, style, "已售")
    else:
        PageDeviceAll(es, index_name, head, text, number, client, style)

def QuerryKeyword(es, index_name, head, text, style, field, condition):
    if field in text:
        search = {
            "query": {
                "match_phrase": {
                    field: condition
                }
            },
            "sort": [{"ID": {"order": "asc"}}],
            "from": 0,
            "size": 10000,
        }
    else:
        search = {
            "query": {
                "term": {
                    field: condition
                }
            },
            "sort": [{"ID": {"order": "asc"}}],
            "from": 0,
            "size": 10000,
        }
    response = es.search(index = index_name, body = search)
    size = response['hits']['total']['value']
    data = AssenblyData(response, size, head, style)
    
    return data, size

def PageDeviceKeyword(es, index_name, head, text, number, client, style, field, condition):
    data, size = QuerryKeyword(es, index_name, head, text, style, field, condition)
    page = 0
    pagemax = math.ceil(size/10)
    
    while True:
        UI.ShowTable(es, index_name, head, text, number, client, style, page, data)
        action = actions("", [{'label': '⬅️ 上一页', 'value': 1}, {'label': '➡️ 下一页', 'value': 2}, {'label': '↩️ 返回批量查找菜单', 'value': 0, 'color': 'warning'}])
        
        match action:
            case 0:
                clear()
                break
            case 1:
                page = page - 1
                if page < 0:
                    page = 0
                clear()
            case 2:
                page = page + 1
                if page >= pagemax:
                    page = pagemax - 1
                clear()     

def KeywordSearch(es, index_name, head, text, number, client, style, keyword):
    if text == []:
        toast("没有可以搜索的字段，要求keyword或text类型", color='error')
        clear()
        return
    
    while True:
        search = input_group(
            "选择检索条件",
            [
                radio("搜索条目", options=keyword, name="field"),
                input("搜索字段", name="condition"),
                actions("", [{'label': '✅ 确认', 'value': 1}, {'label': '↩️ 返回主菜单', 'value': 0, 'color': 'warning'}], name="action")
            ],
            validate=lambda d: (
                ("field", "请选择搜索条目") if d['action'] == 1 and not d.get('field') else
                ("condition", "搜索字段不能为空") if d['action'] == 1 and not d.get('condition', '').strip() else
                None
            )
        )
        
        match search['action']:
            case 0:
                clear()
                break
            
            case 1:
                PageDeviceKeyword(es, index_name, head, text, number, client, style, search['field'], search['condition'])

def QuerryFuzzy(es, index_name, head, style, field, condition):
    search = {
        "query": {
            "match": {
                field: {
                    "query": condition,
                    "fuzziness": "AUTO"
                }
            }
        },
        "sort": [{"ID": {"order": "asc"}}],
        "from": 0,
        "size": 10000,
    }
    response = es.search(index = index_name, body = search)
    size = response['hits']['total']['value']
    data = AssenblyData(response, size, head, style)
    
    return data, size

def PageDeviceFuzzy(es, index_name, head, text, number, client, style, field, condition):
    data, size = QuerryFuzzy(es, index_name, head, style, field, condition)
    page = 0
    pagemax = math.ceil(size/10)
    
    while True:
        UI.ShowTable(es, index_name, head, text, number, client, style, page, data)
        action = actions("", [{'label': '⬅️ 上一页', 'value': 1}, {'label': '➡️ 下一页', 'value': 2}, {'label': '↩️ 返回批量查找菜单', 'value': 0, 'color': 'warning'}])
        
        match action:
            case 0:
                clear()
                break
            case 1:
                page = page - 1
                if page < 0:
                    page = 0
                clear()
            case 2:
                page = page + 1
                if page >= pagemax:
                    page = pagemax - 1
                clear()     

def FuzzySearch(es, index_name, head, text, number, client, style):
    if text == []:
        toast("没有可以搜索的字段，要求text类型", color='error')
        clear()
        return
    
    while True:
        search = input_group(
            "选择检索条件",
            [
                radio("搜索条目", options = text, name = "field"),
                input("搜索字段", name="condition"),
                actions("", [{'label': '✅ 确认', 'value': 1}, {'label': '↩️ 返回主菜单', 'value': 0, 'color': 'warning'}], name = "action")
            ],
            validate=lambda d: (
                ("field", "请选择搜索条目") if d['action'] == 1 and not d.get('field') else
                ("condition", "搜索字段不能为空") if d['action'] == 1 and not d.get('condition', '').strip() else
                None
            )
        )
        
        match search['action']:
            case 0:
                clear()
                break
            
            case 1:
                PageDeviceFuzzy(es, index_name, head, text, number, client, style, search['field'], search['condition'])

def QuerrySemantic(es, index_name, head, client, style, field, condition):
    vector = client.embeddings.create(input=condition, model="text-embedding-3-small")
    search = {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, params.field_name) + 1.0",
                    "params": {
                        "query_vector": vector.data[0].embedding,
                        "field_name": field + 'Vector'
                    }
                }
            }
        },
        "from": 0,
        "size": 10000,
    }
    response = es.search(index = index_name, body = search)
    size = response['hits']['total']['value']
    data = AssenblyData(response, size, head, style)
    
    return data, size

def PageDeviceSemantic(es, index_name, head, text, number, client, style, field, condition):
    data, size = QuerrySemantic(es, index_name, head, client, style, field, condition)
    page = 0
    pagemax = math.ceil(size/10)
    
    while True:
        UI.ShowTable(es, index_name, head, text, number, client, style, page, data)
        action = actions("", [{'label': '⬅️ 上一页', 'value': 1}, {'label': '➡️ 下一页', 'value': 2}, {'label': '↩️ 返回批量查找菜单', 'value': 0, 'color': 'warning'}])
        
        match action:
            case 0:
                clear()
                break
            case 1:
                page = page - 1
                if page < 0:
                    page = 0
                clear()
            case 2:
                page = page + 1
                if page >= pagemax:
                    page = pagemax - 1
                clear()     

def SemanticSearch(es, index_name, head, text, number, client, style):
    if text == []:
        toast("没有可以搜索的字段，要求text类型", color='error')
        clear()
        return
    
    while True:
        search = input_group(
            "选择检索条件",
            [
                radio("搜索条目", options = text, name = "field"),
                input("搜索字段", name="condition"),
                actions("", [{'label': '✅ 确认', 'value': 1}, {'label': '↩️ 返回主菜单', 'value': 0, 'color': 'warning'}], name = "action")
            ],
            validate=lambda d: (
                ("field", "请选择搜索条目") if d['action'] == 1 and not d.get('field') else
                ("condition", "搜索字段不能为空") if d['action'] == 1 and not d.get('condition', '').strip() else
                None
            )
        )
        
        match search['action']:
            case 0:
                clear()
                break
            
            case 1:
                PageDeviceSemantic(es, index_name, head, text, number, client, style, search['field'], search['condition'])
