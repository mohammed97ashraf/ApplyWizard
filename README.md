# ApplyWizard 🚀
Automate your job application process with AI-powered form filling using **LangChain**, **ReAct Agent**, and **AgentQL**. Save time, boost productivity, and simplify your job search journey.

![High Level Design](https://github.com/mohammed97ashraf/ApplyWizard/blob/main/AgentQL.png)

---

✨ **Why ApplyWizard?**
- **Automate**: Let AI fill out your job applications.
- **Save Time**: Focus on important tasks, while ApplyWizard does the repetitive work.
- **Customize**: Tailor the tool to match your specific job search needs.
  
For a detailed explanation, read this article: [Automate Job Applications with LangChain and ReAct Agent](https://medium.com/@mohammed97ashraf/transforming-web-form-filling-automate-job-applications-with-langchain-react-agent-and-agentql-83530acc51f3)

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/mohammed97ashraf/ApplyWizard.git
```
### 2. Create a Python virtual environment:
    ```bash
    python -m venv venv
    ```
### 3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
### 4. Create a `.env` file with API keys:
    ```bash
    AGENTQL_API_KEY=
    LANGCHAIN_API_KEY=
    OPENAI_API_KEY=
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_PROJECT=
    ```


### 💻 How to Use ApplyWizard
!. Create a New Python File: Start by creating a new .py file to run ApplyWizard.

```python
# Import necessary libraries and modules
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

# Load environment variables from .env file
load_dotenv()

# Set environment variables for OpenAI API key, LangChain tracing, project, and API key
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_PROJECT"] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

# Create a new embedding for the resume
new_enadding = create_new_embadding(
    file_path=<path_to_your_resume>,  # Path to your resume
    embadding_collection_name=<collection_name>,  # Name of the embedding collection
    retriever_tool_name=<retriever_tool_name>,  # Name of the retriever tool
    retriever_tool_description=<tool_description>  # Description of the retriever tool
)

# Create a new retriever tool using the embedding
retriever_tool = new_enadding.create_retriever_tools()

# Define a list of tools
tools = [retriever_tool]

# Define a custom prompt for the ReAct agent
prompt = """<custom prompt based on your use case>"""

# Create a new ReAct agent with the tools and prompt
graph_agent = get_react_agent(tools=tools, prompt=prompt)

# Define a query in AgentQL format
QUERY = """
<query in AgentQL format>
"""

# Define the target URL
url = <Target_url>

# Get the input forms from the URL using the query
input_forms = get_form_files(url=url, query=QUERY)

# Flatten and filter the questions in the input forms
filtered_data = flatten_and_filter_questions(input_forms)

# Define the input for the ReAct agent
inputs = {"messages": [("user", str(filtered_data))]}

# Invoke the ReAct agent with the input
result = graph_agent.invoke(inputs)

# Parse the output of the ReAct agent as JSON
parser = JsonOutputParser()
json_data = parser.parse(result["messages"][-1].content)

# Fill the form using the parsed JSON data and the resume location path
fill_the_form(url=url, form_data=json_data, resume_location_path=<local_path_to_your_resume>)
```
#### 🔍 Need Help?
Refer to the examples and more detailed instructions in the repository to see how to customize and extend ApplyWizard to fit your needs.


