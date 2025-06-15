from langchain_community.tools import ShellTool,tool
from langchain_google_genai import ChatGoogleGenerativeAI
from  langchain.agents import create_react_agent,AgentExecutor
from langchain import hub
from langchain_core.prompts import PromptTemplate
from typing import Literal,Optional
from pydantic import BaseModel,Field
from dotenv import load_dotenv
load_dotenv()
import re


model=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

prompt=hub.pull("hwchase17/react")

shell_tool=ShellTool()





@tool
def ShellCommands(task:str)->str:
    "this tool will genearete shell commands for windows"
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    template = PromptTemplate(
        template="For the following task: {task}, give ONLY the Windows shell command. Do not add any explanation, output only the command.",
        input_variables=["task"]
    )

    chain = template | model

    result = chain.invoke({"task": task})
    response = result.content.strip()

    # Parsing logic: extract command from backticks if present
    match = re.search(r'`(.+?)`', response)
    if match:
        command = match.group(1)
    else:
        command = response

    return command.strip()

        
    

agent=create_react_agent(
    llm=model,
    tools=[shell_tool,ShellCommands],
    prompt=prompt

)


agent_ex=AgentExecutor(
    agent=agent,
    tools=[shell_tool,ShellCommands],
    verbose=True


)

log = agent_ex.invoke({
    "input": r"Create a text file  and file name is mahesh  and add a text in that Mahesh you will clear Hashdin internship"
})

print(log)