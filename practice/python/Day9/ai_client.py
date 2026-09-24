# Day 9: AI 测试 —— 调用本地 DeepSeek
# =====================================================
# 前提：Ollama 已安装，DeepSeek 已下载
# 运行：python ai_client.py

import requests
import time


def ask_deepseek(question: str, model: str = "deepseek-r1:1.5b") -> dict:
    """
    调用本地 DeepSeek，返回回答 + 耗时

    返回：{
        "question": str,
        "answer": str,
        "time_cost": float（秒）,
        "success": bool,
        "error": str or None
    }
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": question,
        "stream": False,      # False = 一次性返回完整回答
    }

    try:
        start = time.time()   # 记录开始时间
        resp = requests.post(url, json=payload, timeout=60)
        end = time.time()     # 记录结束时间

        data = resp.json()
        answer = data.get("response", "")

        # 去掉 DeepSeek 的 <think>...</think> 标签（思考过程）
        if "<think>" in answer:
            answer = answer.split("</think>")[-1].strip()

        return {
            "question": question,
            "answer": answer,
            "time_cost": round(end - start, 2),
            "success": True,
            "error": None,
        }

    except Exception as e:
        return {
            "question": question,
            "answer": "",
            "time_cost": 0,
            "success": False,
            "error": str(e),
        }


# =====================================================
# 测试：调用一次看看
# =====================================================
if __name__ == "__main__":
    print("正在调用本地 DeepSeek，请稍等...\n")

    result = ask_deepseek("用一句话解释什么是软件测试")

    if result["success"]:
        print(f"问题: {result['question']}")
        print(f"回答: {result['answer']}")
        print(f"耗时: {result['time_cost']} 秒")
    else:
        print(f"调用失败: {result['error']}")
