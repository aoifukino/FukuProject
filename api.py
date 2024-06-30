# FastAPIの読み込み
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

import math
client = Groq(api_key="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")

class TaxIn(BaseModel):
    price: int
    item: str = None
    tax_rate: float

# FastAPIのインスタンスを作成
app = FastAPI()

# getメソッドで、/にアクセスした時の処理を記述
@app.get("/")
# asyncで*非同期処理を行う
# *あるタスクを実行している最中に、実行中のタスクを止めることなく、別のタスクを実行できる
async def hello():
     # Set the system prompt
	system_prompt = {
	"role": "system",
	"content": "あなたは便利なアシスタントです。質問には日本語で簡潔に答えてください。"
	}

	# Set the user prompt
	user_input = "面接のコツを教えてください。"
	user_prompt = {
	"role": "user", "content": user_input
	}
     
	# Initialize the chat history
	chat_history = [system_prompt, user_prompt]
     
	response = client.chat.completions.create(model="llama3-70b-8192",messages=chat_history,max_tokens=100,temperature=1.2)


	return {"text": f"{response.choices[0].message.content}"}

# getメソッドで、/TaxEx/{price}にアクセスした時の処理を記述
@app.post("/TaxEx/{price}")
async def TaxEx(price: int, item: str = None):
    if item:
        return {"text": f"{item}は{price}円"}
    return {"text": f"何かが{price}円"}

# postメソッドで、/にアクセスした時の処理を記述
@app.post("/TaxIn")
async def TaxIn(data: TaxIn):
    in_tax_cost = math.ceil(data.price * (1 + data.tax_rate))
    return {"text": f"{data.item}は{in_tax_cost}円(税込み)"}