from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import json

# 定义只刷新字段列表区域的函数
def refresh_field_list(fields):
    clear()
    if fields:
        table_data = [['字段名', '类型', '操作']]
        for i, f in enumerate(fields):
            # 第一个字段id不允许删除
            delete_button = put_button("删除", onclick=lambda i=i: delete_field(fields, i)) if i > 0 else None
            table_data.append([f['name'], f['type'], delete_button])
        put_table(table_data)

# 字段删除函数 - 只删除非id字段
def delete_field(fields, index):
    if index > 0:  # 确保不删除第一个id字段
        deleted_field = fields.pop(index)
        toast(f"已删除字段: {deleted_field['name']}")
        refresh_field_list(fields)  # 只刷新字段列表区域

def Initialize(es, index_name):
    """Elasticsearch 索引创建工具 - 核心功能版"""
    toast("⚡ 开始初始化索引...")
    # 界面标题和说明
    put_markdown("## 🛠️ 索引创建工")
    # 初始化字段列表 - 强制第一个字段为id (integer类型)
    fields = fields = [{"name": "ID", "type": "integer"}]
    # 初始显示字段列表
    refresh_field_list(fields)
    
    while True:
        # 操作按钮组 - 放在循环内部持续响应
        action = actions("字段管理", buttons=[
            {'label': '➕ 添加字段', 'value': 'add'},
            {'label': '✅ 完成创建', 'value': 'done'},
            {'label': '❌ 取消', 'value': 'cancel'},
            {'label': '⚙️ 默认', 'value': 'default'}
        ])

        match action:
            case 'cancel':
                # 初始化字段列表 - 强制第一个字段为id (integer类型)
                fields = [{"name": "ID", "type": "integer"}]
                # 初始显示字段列表
                refresh_field_list(fields)
                continue
        
            case 'done':
                # 至少需要id之外的另一个字段
                if len(fields) < 2:
                    toast("请添加至少一个字段", color='error')
                    continue
                
                fields.append({"style": "custom"})
                with open("config/index.json", "w", encoding="utf-8") as f:
                    json.dump(fields, f, indent=4, ensure_ascii=False) 
                properties = {}
                for each in fields[:-1]:
                    match each['type']:
                        case 'integer':
                            properties[each['name']] = {"type": "integer"}
                        case 'keyword':
                            properties[each['name']] = {"type": "keyword"}
                        case 'text':
                            properties[each['name']] = {"type": "text", "analyzer": "ik_smart", "search_analyzer": "ik_smart"}
                            properties[each['name']+'Vector'] = {"type": "dense_vector", "dims": 1536, "index": True, "similarity": "cosine"}
                break
            
            case 'default':
                fields = [{"style": "default"}]
                with open("config/index.json", "w", encoding="utf-8") as f:
                    json.dump(fields, f, indent=4, ensure_ascii=False)
                
                properties = {"ID": {"type": "integer"}, "品牌": {"type": "keyword"}, "比例": {"type": "keyword"}, "赛季": {"type": "keyword"},
                              "车队": {"type": "keyword"}, "型号": {"type": "keyword"}, "车手": {"type": "keyword"}, "车号": {"type": "keyword"},
                              "分站": {"type": "keyword"}, "名次": {"type": "keyword"}, "状态": {"type": "keyword"},
                              "入库时间": {"type": "integer"}, "购入价格": {"type": "integer"}, "卖出价格": {"type": "integer"}, 
                              "备注": {"type": "text", "analyzer": "ik_smart", "search_analyzer": "ik_smart"},
                              "备注Vector": {"type": "dense_vector", "dims": 1536, "index": True, "similarity": "cosine"},
                              "描述": {"type": "text", "analyzer": "ik_smart", "search_analyzer": "ik_smart"},
                              "描述Vector": {"type": "dense_vector", "dims": 1536, "index": True, "similarity": "cosine"}}
                
                break

        # 添加新字段表单
        field = input_group("添加新字段", [
            input("字段名称", name="name", required=True, 
                  validate=lambda v: "字段名已存在" if v in [f['name'] for f in fields] else None),
            select("数据类型", options=[
                ('关键字 (keyword)', 'keyword'),
                ('文本 (text)', 'text'),
                ('整数 (integer)', 'integer'),
            ], name="type", value='keyword'),
        ])
        fields.append(field)
        toast(f"字段 '{field['name']}' 已添加")
        refresh_field_list(fields)  # 更新字段列表
           
    index_mapping = {"mappings": {"properties":properties}, "settings":{"number_of_shards":1, "number_of_replicas":1}}
    es.indices.create(index=index_name, body=index_mapping)
    toast("✅ 索引初始化完成！")
    clear()