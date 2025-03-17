import http.client
import json


class ai:
    api_key = "sk-xNoKJZg0BcyKLcWlqYOzE0VM2nhvrqUXnngz63P4Oaf3dapj"
    # gpt api
    api_url = "https://api.chatanywhere.com.cn"
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }
    conn = http.client.HTTPSConnection("api.chatanywhere.tech")

    @classmethod
    async def call_ai_api(self) -> str:
        """
        调用大模型API，获取诊断建议
        """

        prompt = f"""
        我是一名眼科医生，根据以下患者信息，提供诊断建议和治疗流程：
        年龄：50，性别：男，
        确诊疾病：糖尿病,
        疾病阶段：晚期。
    
        请提供：
        1. 治疗建议
        2. 检查计划
        3. 用药建议
        """

        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        self.conn.request("POST", "/v1/chat/completions", payload, self.headers)
        data = json.loads(self.conn.getresponse().read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        content = (content.replace("1.", "###1.")
                   .replace("2.", "###2.")
                   .replace("3.", "###3."))
        return content

    @classmethod
    async def get_ai_answer(self) -> str:
        """
        获取AI模型的诊断建议
        """
        # 测试提问
        question = "我眼睛红肿，酸痛，眼睛浑浊怎么办"

        prompt = f"""
        我是一名眼科医生，请关于我下面的提问进行回答，要求回答具体清晰准确,并按照下面的格式进行回复
        1. answer...
        2. answer...
        ...
        下面我将开始提问
        {question}
        """
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        self.conn.request("POST", "/v1/chat/completions", payload, self.headers)
        data = json.loads(self.conn.getresponse().read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        content = (content.replace("1.", "###1.")
                   .replace("2.", "###2.")
                   .replace("3.", "###3."))
        return content
