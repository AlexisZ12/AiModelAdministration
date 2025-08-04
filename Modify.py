from pywebio.input import *
from pywebio.output import *
import json
import UI

def ModifyDocumentDefault(es, index_name, head, text, number, client, style, page, data, id):
    clear()
    if style == 'default':
        response = es.get(index = index_name, id = id)
        data_new = input_group(
            "ID: {0}".format(response['_source']['ID']),
            [
                input("品牌", value = response['_source']['品牌'], name = "brand"),
                input("比例", value = response['_source']['比例'], name = "scale"),
                input("赛季", value = response['_source']['赛季'], name = "season"),
                input("车队", value = response['_source']['车队'], name = "team"),
                input("型号", value = response['_source']['型号'], name = "type"),
                input("车手", value = response['_source']['车手'], name = "driver"),
                input("车号", value = response['_source']['车号'], name = "number"),
                input("分站", value = response['_source']['分站'], name = "stage"),
                input("名次", value = response['_source']['名次'], name = "rank"),
                select("状态", options=['入库', '预购', '退订', '已售'], value=response['_source']['状态'], name="state"),
                input("入库时间", value = response['_source']['入库时间'], type=NUMBER, name = "date"),
                input("购入价格", value = response['_source']['购入价格'], type=NUMBER, name = "price_in"),
                input("卖出价格", value = response['_source']['卖出价格'], type=NUMBER, name = "price_out"),
                input("备注", value = response['_source']['备注'], name = "remark"),
                actions(name="action", buttons=[{'label': '确认', 'value': 1}, {'label': '取消', 'value': 0, 'color': 'warning'}])
            ])
        
        match data_new['action']:
            case 0:
                clear()
                UI.ShowTable(es, index_name, head, text, number, client, style, page, data)

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

                document = {
                    "doc": {
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
                }
                response = es.update(index = index_name, id = id, body = document)
                toast('修改成功')
                
                for each in data:
                    if each[0] == id:
                        each[1] = data_new['brand']
                        each[2] = data_new['scale']
                        each[3] = data_new['season']
                        each[4] = data_new['team']
                        each[5] = data_new['type']
                        each[6] = data_new['driver']
                        each[7] = data_new['number']
                        each[8] = data_new['stage']
                        each[9] = data_new['rank']
                        each[10] = data_new['state']
                        each[11] = data_new['date']
                        each[12] = data_new['price_in']
                        each[13] = data_new['price_out']
                        each[14] = data_new['remark']
                        
                clear()
                UI.ShowTable(es, index_name, head, text, number, client, style, page, data)
    else:
        response = es.get(index = index_name, id = id)
        data_new = input_group(
            "ID: {0}".format(response['_source']['ID']),
            [
                input(field, value=response['_source'].get(field, ""), name=str(idx), type=NUMBER) if field in number
                else input(field, value=response['_source'].get(field, ""), name=str(idx)) 
                for idx, field in enumerate(head[1:-1])
            ] +
            [
                actions(name="action", buttons=[
                    {'label': '确认', 'value': 1},
                    {'label': '取消', 'value': 0, 'color': 'warning'}
                ])
            ]
        )
        match data_new['action']:
            case 0:
                clear()
                UI.ShowTable(es, index_name, head, text, number, client, style, page, data)
            case 1:
                doc = {}
                for i in range(len(head)-2):
                    doc[head[i+1]] = data_new[str(i)]
                    if head[i+1] in text:
                        vector = client.embeddings.create(
                            input = data_new[str(i)],
                            model = "text-embedding-3-small"
                        )
                        doc[head[i+1]+'Vector'] = vector.data[0].embedding
                document = {"doc": doc}
                
                response = es.update(index = index_name, id = id, body = document)
                toast('修改成功')

                for each in data:
                    if each[0] == id:
                        for j in range(len(head)-2):
                            each[j+1] = data_new[str(j)]
                
                clear()
                UI.ShowTable(es, index_name, head, text, number, client, style, page, data)