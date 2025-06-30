from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv
# .env 파일을 만들면 따로 api키를 설정하지 않아도 됨


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


# client = OpenAI(api_key=api_key)
# 랭체인에서 제공하는 ChatOpenAI 클래스를 사용하여 OpenAI API와 연결
llm = ChatOpenAI(model="gpt-4o")

# def get_ai_response(messages):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         temperature=0.9,
#         messages=messages,
#     )
#     return response.choices[0].message.content
    

messages=[
    # {"role": "system",  "content":"너는 상담사를 도와주는 상담사야"}
    # 랭체인에서는 SystemMessage 클래스를 사용하여 시스템 메시지를 생성
    SystemMessage(content="너는 사용자를 도와주는 상담사야")
] # 초기 시스템 메시지 설정

while True:
    user_input = input("사용자: ") # 사용자 입력받기
    
    if user_input =="exit":
        break
    # messages.append({"role": "user", "content": user_input})
    # 랭체인에서는 HumanMessage 클래스를 사용하여 사용자 메시지를 생성
    messages.append(HumanMessage(user_input))
        
    #ai_response = get_ai_response(messages) # 대화 기록 기반으로 ai 응답 가져오기
    ai_response = llm.invoke(messages) # 랭체인에서는 invoke 메서드를 사용하여 메시지를 전달하고 응답을 생성
    messages.append(ai_response)
    print("AI:" + ai_response.content)
   
