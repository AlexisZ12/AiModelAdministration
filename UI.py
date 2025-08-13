from pywebio.output import *
import Modify

def MainUI():
    put_markdown("""
# 🏎 欢迎使用赛车模型库存管理系统
**赛车模型管理系统** 是一个专为赛车模型爱好者设计的开源免费的库存管理工具，帮助你高效管理和追踪心爱的模型收藏品。
我们非常重视用户的反馈，如果你有任何建议或发现问题，请通过以下方式联系我：
- 📂 **项目仓库**: [github.com/AlexisZ12/AiModelAdministration](https://github.com/AlexisZ12/AiModelAdministration)
- ⭐ **欢迎Star**: 如果喜欢这个项目，请在GitHub上点个Star支持我们
- ✉️ **联系邮箱**: 2242809239@qq.com
🚀 **当前版本**: v1.0.0 | 🔄 **最后更新**: 2025-08-04
---
### 🌈 特色功能
- 完整的模型收藏管理
- 支持多维度分类系统
- 数据导入/导出功能
- 可视化统计报表（待更新）
    """)

def ShowTable(es, index_name, head, text, number, client, style, page, data):
    showlist = []
    showlist.append(head)
    for i in range(page*10, page*10+10):
        modify_button = put_button("修改", onclick=lambda id=data[i][0]: Modify.ModifyDocumentDefault(es, index_name, head, text, number, client, style, page, data, id)) if data[i][0] != "" else ""
        data[i][-1] = modify_button
        showlist.append(data[i])
    
    put_table(showlist)