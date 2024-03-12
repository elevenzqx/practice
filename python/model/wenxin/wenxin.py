from langchain_wenxin import Wenxin

WENXIN_APP_Key = ""
WENXIN_APP_SECRET = ""

llm = Wenxin(
    temperature=0.9,
    model="ernie-bot-turbo",
    baidu_api_key = WENXIN_APP_Key,
    baidu_secret_key = WENXIN_APP_SECRET,
    verbose=True,
)

response = llm("你是谁？")
print(response)