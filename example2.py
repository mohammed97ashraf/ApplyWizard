import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_utils.cretae_embaddings import create_new_embadding
from langchain_utils.langgraph_react_agent import get_react_agent
from langchain import hub
from agental_utils.get_application import get_form_files
from agental_utils.fill_form import fill_the_form, flatten_and_filter_questions
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_PROJECT"] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

new_enadding = create_new_embadding(file_path="./Mohammed_Ashraf_v5.pdf",
                                    embadding_collection_name="my-resume",
                                   retriever_tool_name="my_resume",
                                   retriever_tool_description="my resume have the the information me as a machine learning engineer.")

retriever_tool =new_enadding.create_retriever_tools()

@tool
def get_anwers_about_me(query: str):
    """Useful for when you need to answer questions about me.use my resume to anwers the qustion"""

    llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=False)
    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt.messages[0].prompt.template = "you are help asssistent for Mohammed Ashraf.\
    you need to anwers the questions asked in the job application form using the tools you have.\
    incuding my contact details if needed."

    agent = create_openai_tools_agent(llm, [retriever_tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[retriever_tool])
    response = agent_executor.invoke({"input":query})
    return response

@tool
def write_a_cover_letter(job_role:str,job_desc:str):
    """Useful for when you need to write a cover letter.use my resume to write a highly costomize cover letter"""

    llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=False)
    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt.messages[0].prompt.template = "you are help asssistent for Mohammed Ashraf.\
    you need to anwers the questions asked in the job application form using the tools you have.\
    i want you to write cover latter for based on the job role and the job descption.make it as custumize as posible."
    agent = create_openai_tools_agent(llm, [retriever_tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[retriever_tool])
    response = agent_executor.invoke({"input":f'{{"job_role":"{job_role}",\
                                  "job_desc":"{job_desc}"}}'})
    return response


tools = [get_anwers_about_me,write_a_cover_letter]

prompt="you are help asssistent for Mohammed Ashraf.\
you need to anwers the questions asked in the job application form using the tools you have.\
the questions will be in form stype with `qustion` and `expected anwers type`. \
find the anwers to questions and the respose.\
return JSON a object with the aswer"

grapgh_agent = get_react_agent(tools=tools,prompt=prompt)

QUERY = """
{
    details[]
    {
        job_role
        descption
        qustions_asksed[]
        {
            question
            sub_questions[]
            {
                question
                type
                options
            }
            type(like select, radio, checkbox, text, textarea)
            options
        }
    }
}
"""

input_forms = get_form_files(url="https://form.jotform.com/242476590759471", query = QUERY)

print(input_forms)
filtered_data = flatten_and_filter_questions(input_forms)

print(filtered_data)
inputs = {"messages": [("user", str(filtered_data))]}
result = grapgh_agent.invoke(inputs)
parser = JsonOutputParser()
json_data = parser.parse(result["messages"][-1].content)
print(json_data)

fill_the_form(url="https://form.jotform.com/242476590759471",form_data=json_data, resume_location_path="E:\\new_projects\\web_automation\\agent_ql\\app\\Mohammed_Ashraf_v5.pdf")
