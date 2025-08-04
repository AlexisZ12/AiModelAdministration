from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import pandas as pd
import io
import os
from datetime import datetime
import Search

def TemplateForm(head):
    df = pd.DataFrame(columns=head)
    with io.BytesIO() as buffer:
        df.to_excel(buffer, index=False)
        excel_bytes = buffer.getvalue()
    
    return excel_bytes

def InputOne(es, index_name, head, text, number, client, style):
    id = es.count(index=index_name)['count'] + 1
    if style == 'default':
        data_new = input_group(
            "ID: {0}".format(id),
            [
                input("品牌", name = "brand"),
                input("比例", name = "scale"),
                input("赛季", name = "season"),
                input("车队", name = "team"),
                input("型号", name = "type"),
                input("车手", name = "driver"),
                input("车号", name = "number"),
                input("分站", name = "stage"),
                input("名次", name = "rank"),
                select("状态", options=['入库', '预购', '退订', '已售'], name="state"),
                input("入库时间", type=NUMBER, name = "date"),
                input("购入价格", type=NUMBER, name = "price_in"),
                input("卖出价格", type=NUMBER, name = "price_out"),
                input("备注", name = "remark"),
                actions(name="action", buttons=[{'label': '✅ 确认', 'value': 1}, {'label': '❌ 取消', 'value': 0, 'color': 'warning'}])
            ])
        
        match data_new['action']:
            case 0:
                clear()
            
            case 1:          
                ModelDescribe = "这是一台品牌为{0}的{1}比例的赛车模型，这台模型的原型车为{2}赛季{3}车队{4}号车手{5}驾驶的{6}。".format(data_new['brand'], data_new['scale'], data_new['season'], data_new['team'], data_new['number'], data_new['driver'], data_new['type'])

                if data_new['rank'] == "DNF":
                    RaceDescribe = "{0}在{1}的正赛中未完赛。".format(data_new['driver'], data_new['stage'])
                elif data_new['rank'] == "Pole":
                    RaceDescribe = "{0}在{1}的排位赛中取得杆位。".format(data_new['driver'], data_new['stage'])
                elif data_new['rank'] == "测试":
                    RaceDescribe = "{0}在{1}参与了测试".format(data_new['driver'], data_new['stage'])
                else:
                    RaceDescribe = "{0}在{1}的正赛中取得了第{2}名。".format(data_new['driver'], data_new['stage'], data_new['rank'])
                
                if data_new['state'] == "退订":
                    StateDescribe = "这台模型已经退订"
                elif data_new['state'] == "预购":
                    if(data_new['price_in'] == 0):
                        StateDescribe = "这台模型已经预订，预定价格未知"
                    else:
                        StateDescribe = "这台模型已经预订，预定价格为{0}".format(data_new['price_in'])
                elif data_new['state'] == "入库":
                    StateDescribe = "这台模型已经入库，购入价格为{0}，入库时间为{1}".format(data_new['price_in'], data_new['date'])
                elif data_new['state'] == "已售":
                    StateDescribe = "这台模型已经出售，购入价格为{0}，卖出价格为{1}，入库时间为{2}".format(data_new['price_in'], data_new['price_out'], data_new['date'])

                TextDescribe = ModelDescribe + RaceDescribe + StateDescribe + "这台模型还有如下特点：" + data_new['remark']
                vector2 = client.embeddings.create(
                    input = TextDescribe,
                    model = "text-embedding-3-small"
                )
                
                vector1 = client.embeddings.create(
                    input = data_new['remark'],
                    model = "text-embedding-3-small"
                )

                doc = {
                    "ID": id,
                    "品牌": data_new['brand'],
                    "比例": data_new['scale'],
                    "赛季": data_new['season'],
                    "车队": data_new['team'],
                    "型号": data_new['type'],
                    "车手": data_new['driver'],
                    "车号": data_new['number'],
                    "分站": data_new['stage'],
                    "名次": data_new['rank'],
                    "状态": data_new['state'],
                    "入库时间": data_new['date'],
                    "购入价格": data_new['price_in'],
                    "卖出价格": data_new['price_out'],
                    "备注": data_new['remark'],
                    "备注Vector": vector1.data[0].embedding,
                    "描述": TextDescribe,
                    "描述Vector": vector2.data[0].embedding
                }
                
                es.index(index = index_name, id = id, document = doc)
                toast('新增成功')
                
    else:
        data_new = input_group(
            "ID: {0}".format(id),
            [
                input(field, name=str(idx), type=NUMBER) if field in number 
                else input(field, name=str(idx))
                for idx, field in enumerate(head[1:-1])
            ] +
            [
                actions(name="action", buttons=[
                    {'label': '✅ 确认', 'value': 1},
                    {'label': '❌ 取消', 'value': 0, 'color': 'warning'}
                ])
            ]
        )
        
        match data_new['action']:
            case 0:
                clear()
            
            case 1:
                doc = {'ID': id,}
                for i in range(len(head)-2):
                    doc[head[i+1]] = data_new[str(i)]
                    if head[i+1] in text:
                        vector = client.embeddings.create(
                            input = data_new[str(i)],
                            model = "text-embedding-3-small"
                        )
                        doc[head[i+1]+'Vector'] = vector.data[0].embedding
                
                es.index(index = index_name, id = id, document = doc)
                toast('新增成功')
    
def InputData(es, index_name, head, text, client, style):
    put_markdown('# 导入模板')
    put_markdown('请按照以下格式导入数据')
    put_table([head[1:-1]])
    put_file("template.xlsx", TemplateForm(head[1:-1]), "📄 下载模板")
    action = input_group("导入数据",
        [
            file_upload(name="file", accept=".xlsx"),
            actions(name="act", buttons=[{'label': '📥 导入数据', 'value': 1}, {'label': '↩️ 返回主菜单', 'value': 0, 'color': 'warning'}])
        ],
        validate=lambda d: ("必须选择文件" if d.get("act") == 1 and not d.get("file") else None)
    )
    
    match action['act']:
        case 0:
            clear()
        
        case 1:
            id = es.count(index=index_name)['count'] + 1
            strat = id
            
            file_content = action['file']['content']
            df = pd.read_excel(io.BytesIO(file_content), dtype=str, keep_default_na=False)
            
            if style == 'default':
                for index, row in df.iterrows():
                    if row['入库时间'] == '0': row['入库时间'] = None
                    if row['购入价格'] == '0': row['购入价格'] = None
                    if row['卖出价格'] == '0': row['卖出价格'] = None
                    
                    ModelDescribe = "这是一台品牌为{0}的{1}比例的赛车模型，这台模型的原型车为{2}赛季{3}车队{4}号车手{5}驾驶的{6}。".format(row['品牌'], row['比例'], row['赛季'], row['车队'], row['车号'], row['车手'], row['型号'])

                    if row['名次'] == "DNF":
                        RaceDescribe = "{0}在{1}的正赛中未完赛。".format(row['车手'], row['分站'])
                    elif row['名次'] == "Pole":
                        RaceDescribe = "{0}在{1}的排位赛中取得杆位。".format(row['车手'], row['分站'])
                    elif row['名次'] == "测试":
                        RaceDescribe = "{0}在{1}参与了测试".format(row['车手'], row['分站'])
                    else:
                        RaceDescribe = "{0}在{1}的正赛中取得了第{2}名。".format(row['车手'], row['分站'], row['名次'])
                    
                    if row['状态'] == "退订":
                        StateDescribe = "这台模型已经退订"
                    elif row['状态'] == "预购":
                        if(row['购入价格'] == None):
                            StateDescribe = "这台模型已经预订，预定价格未知"
                        else:
                            StateDescribe = "这台模型已经预订，预定价格为{0}".format(row['购入价格'])
                    elif row['状态'] == "入库":
                        StateDescribe = "这台模型已经入库，购入价格为{0}，入库时间为{1}".format(row['购入价格'], row['入库时间'])
                    elif row['状态'] == "已售":
                        StateDescribe = "这台模型已经出售，购入价格为{0}，卖出价格为{1}，入库时间为{2}".format(row['购入价格'], row['卖出价格'], row['入库时间'])

                    TextDescribe = ModelDescribe + RaceDescribe + StateDescribe + "这台模型还有如下特点：" + row['备注']
                    vector2 = client.embeddings.create(
                        input = TextDescribe,
                        model = "text-embedding-3-small"
                    )
                    
                    vector1 = client.embeddings.create(
                        input = row['备注'],
                        model = "text-embedding-3-small"
                    )
                    
                    doc = {
                        "ID": id,
                        "品牌": row['品牌'],
                        "比例": row['比例'],
                        "赛季": row['赛季'],
                        "车队": row['车队'],
                        "型号": row['型号'],
                        "车手": row['车手'],
                        "车号": row['车号'],
                        "分站": row['分站'],
                        "名次": row['名次'],
                        "状态": row['状态'],
                        "入库时间": row['入库时间'],
                        "购入价格": row['购入价格'],
                        "卖出价格": row['卖出价格'],
                        "备注": row['备注'],
                        "备注Vector": vector1.data[0].embedding,
                        "描述": TextDescribe,
                        "描述Vector": vector2.data[0].embedding
                    }
                    
                    es.index(index = index_name, id = id, document = doc)
                    id += 1
            else:
                for index, row in df.iterrows():
                    doc = {'ID': id,}
                    for each in head[1:-1]:
                        doc[each] = row[each]
                        if each in text:
                            vector = client.embeddings.create(
                                input = row[each],
                                model = "text-embedding-3-small"
                            )
                            doc[each+'Vector'] = vector.data[0].embedding
                    
                    es.index(index = index_name, id = id, document = doc)
                    id += 1
            
            toast('导入完成，导入{0}条数据'.format(id-strat))
            clear()
    
def OutputData(es, index_name, head, style, path):
    data, size = Search.QuerryAll(es, index_name, head, style)
    processed_data = []
    for i in range(size):
        processed_data.append(data[i][1:-1])
    df = pd.DataFrame(processed_data, columns=head[1:-1])
    
    os.makedirs(path, exist_ok=True)
    filename = datetime.now().strftime('%Y%m%d_%H%M')
    df.to_excel(f'{path}/{filename}.xlsx', index=False, engine='openpyxl')
    
    toast('导出完成，导出{0}条数据'.format(size))