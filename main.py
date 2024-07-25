from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
import os
from tools import get_crypto_portfolio_value, get_gold_portfolio_value

load_dotenv()
openai_api_key = os.getenv("OPEN_AI_API_KEY")

llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo"
)

chatTemplate = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You want to inform about the current financial portfolio of the user including the current prices of crypto currencies and gold in US dollars"),
        HumanMessagePromptTemplate.from_template("{prompt_input}"),
        MessagesPlaceholder("agent_scratchpad")
    ]
)

tools = [get_crypto_portfolio_value, get_gold_portfolio_value]
agent = create_tool_calling_agent(llm, tools=tools, prompt= chatTemplate)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

memory = [""]


def get_chatbot_response(prompt):
    memory.append(prompt)
    memory_prompt = ' '.join(memory)
    chatbot_response = agent_executor.invoke({"prompt_input": memory_prompt})["output"]
    memory.append(chatbot_response)
    return chatbot_response


if __name__ == '__main__':
    print("Welcome to the Financial Portfolio Chatbot. Type 'exit' to end the conversation.")
    while True:
        user_input = input("Prompt: ")
        if user_input.lower() == 'exit':
            print("Have a nice day!")
            break
        response = get_chatbot_response(user_input)
        print(f"Chatbot: {response}")