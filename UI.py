from pywebio.output import *
from pywebio.input import *
import Modify

def MainUI():
    put_markdown("""
# 🏎 AiModelAdministration

## 🌟 项目简介
**AiModelAdministration** 专为模型收藏爱好者打造，通过AI语义理解与高效检索技术，让您的每一件赛车模型都得到精准管理。无论是记录收藏细节、追踪状态变化，还是快速查找心仪藏品，都能轻松实现。
- 📂 **GitHub项目仓库**: [AlexisZ12/AiModelAdministration](https://github.com/AlexisZ12/AiModelAdministration)
- ⭐ **欢迎Star**: 如果喜欢这个项目，请在GitHub上点个Star支持我们
- ✉️ **联系邮箱**: 2242809239@qq.com
- 💬 **微信**: `Alexis_12_Z`
- 💖 **爱发电**: [AlexisZ12](https://afdian.com/a/AlexisZ12)

## ✨ 核心功能
- 🚗 全维度模型信息管理（品牌/比例/赛季/状态等）
- 🔍 三重检索系统（关键词/模糊/语义理解）
- 📥 批量数据导入导出（支持Excel格式）
- 🛠️ 自定义字段配置，适配个性化收藏需求
- 📊 收藏状态可视化统计

## 🔑 开始使用
1. 配置 **Elasticsearch** 连接信息
2. 填写 **OpenAI API** 密钥（用于语义检索）
3. 选择使用模式（默认/自定义字段）
4. 启动系统，开始管理您的收藏！
    """)

def ShowTable(es, index_name, head, text, number, client, style, page, data):
    showlist = []
    showlist.append(head)
    for i in range(page*10, page*10+10):
        modify_button = put_button("修改", onclick=lambda id=data[i][0]: Modify.ModifyDocumentDefault(es, index_name, head, text, number, client, style, page, data, id)) if data[i][0] != "" else ""
        data[i][-1] = modify_button
        showlist.append(data[i])
    
    put_table(showlist)