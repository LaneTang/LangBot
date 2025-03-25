import requests

def chat_vloces(content, syetem_content = "你是一个有用的助手!"):
    url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
    headers = {
        'Authorization': "Bearer 5ba3393a-4042-4d28-8bdb-59683296c03a",
        'Content-Type': 'application/json'  # 添加这个header确保服务器知道我们发送的是JSON数据。
    }
    data = {
        "model": "doubao-lite-32k-240828",
        "messages": [
            {
                "role": "system",
                "content": syetem_content
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "stream": False

    }

    response = requests.post(url, headers=headers, json=data)
    ans = response.json()['choices'][0]['message']['content']
    return(ans)

from openai import OpenAI
def chat_deepseek(content, syetem_content = "你是一个有用的助手!"):
    client = OpenAI(api_key="sk-71850043039a4fdab3fed58fe4cd6203", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": syetem_content},
            {"role": "user", "content": content},
        ],
        stream=False  # 启用流式传输
    )

    return(response.choices[0].message.content)