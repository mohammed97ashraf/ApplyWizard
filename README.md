# ApplyWizard 

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
cd ApplyWizard
```

### 2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file with API keys:
```
AGENTQL_API_KEY=
LANGCHAIN_API_KEY=
OPENAI_API_KEY=
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT=
```

### 5. Run the example (see below) to verify setup.

---

## 💻 How to Use ApplyWizard

Create a new Python file (e.g., `run_wizard.py`) with the following complete example:

```python
import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_utils.create_embeddings import create_new_embedding
from langchain_utils.langgraph_react_agent import get_react_agent
from langchain import hub
from agentql_utils.get_application import get_form_files
from agentql_utils.fill_form import fill_the_form, flatten_and_filter_questions
from langchain_core.output_parsers import JsonOutputParser

def main():
    load_dotenv()
    
    # Initialize the language model
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    # Get the agent (assuming get_react_agent returns an AgentExecutor)
    agent = get_react_agent(llm)
    
    # Example: URL of a job application form
    form_url = "https://example.com/apply"
    
    # Fetch form fields
    form_data = get_form_files(form_url)
    if not form_data:
        print("Could not retrieve form fields.")
        return
    
    # Flatten and filter questions
    questions = flatten_and_filter_questions(form_data)
    
    # Fill the form using the agent
    result = agent.invoke({"input": f"Fill out the job application form with these questions: {questions}"})
    print("Agent output:", result)
    
    # Optionally submit the form
    # fill_the_form(form_url, result)

if __name__ == "__main__":
    main()
```

*Note: The above code assumes the exact module paths exist. Adjust imports if your local structure differs.*

---

## 🏗 Architecture

ApplyWizard uses a ReAct (Reasoning + Acting) agent powered by LangChain. The agent:
1. Receives a job application URL.
2. Uses AgentQL to scrape form fields and questions.
3. Leverages embeddings to match user profile data to questions.
4. Generates responses using OpenAI GPT-4.
5. Optionally submits the form autonomously.

Below is a simplified flow:
```
User URL → AgentQL → LangChain Agent → LLM Response → Fill Form
```

---

## 🛠 Troubleshooting

- **Import errors**: Ensure all dependencies in `requirements.txt` are installed and package names match the actual modules.
- **API key errors**: Verify your `.env` file has correct keys and is loaded using `load_dotenv()`.
- **AgentQL not working**: Check the form URL is accessible and AgentQL supports it.
- **Missing modules**: If you see `ModuleNotFoundError` for `langchain_utils` or `agentql_utils`, ensure the source code is in the correct location (they should be inside the repo).

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details. (A license file should be added.)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.