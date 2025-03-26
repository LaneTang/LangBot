import requests
from openai import OpenAI

def chat_vloces(content, syetem_content = "你是来自电影银翼杀手2049的女主角乔伊!"):
    url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
    headers = {
        'Authorization': "Bearer 53d6f2b9-3347-48cc-bf88-698b486b243b",
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

def chat_deepseek(content, syetem_content = "你是来自电影银翼杀手2049的女主角乔伊!"):
    client = OpenAI(api_key="sk-0dad667193c24aa7ad5a2af8d5aba764", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": syetem_content},
            {"role": "user", "content": content},
        ],
        stream=False  # 启用流式传输
    )

    return(response.choices[0].message.content)