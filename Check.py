from openai import APIConnectionError, AuthenticationError, APIStatusError
from pywebio.input import *
from pywebio.output import *

def CheckES(es):
    try:
        if not es.ping():
            toast("❌ Elasticsearch连接失败，请检查地址和服务状态", color='error')
            return False
        toast("✅ Elasticsearch连接成功")
        return True
    except ConnectionError as e:
        toast(f"⛔ 网络连接异常: {str(e)}", color='error')
        return False
    except Exception as e:
        toast(f"🔥 未知连接错误: {str(e)}", color='error')
        return False

def CheckOpenAi(client):
    try:
        response = client.models.list()       
        if not response.data or len(response.data) == 0:
            toast("⚠️ OpenAi服务测试失败", color='warning')
            return False
        toast(f"✅ OpenAi服务连接成功")
        return True
        
    except AuthenticationError:
        toast("⛔ OpenAi API密钥无效", color='error')
        return False
    except APIConnectionError as e:
        toast("🌐 OpenAi网络连接失败", color='error')
        return False
    except APIStatusError as e:
        toast("🚨 OpenAi服务异常", color='error')
        return False
    except Exception as e:
        toast("🔥 OpenAi未知错误", color='error')
        return False