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

### Prerequisites
- Python 3.9 or higher
- An OpenAI API key (get one at [OpenAI](https://platform.openai.com/))
- An AgentQL API key (sign up at [AgentQL](https://agentql.com/))
- A LangChain API key (optional, for tracing; get one at [LangChain](https://smith.langchain.com/))

### 1. Clone the Repository
```bash
git clone https://github.com/mohammed97ashraf/ApplyWizard.git
cd ApplyWizard
```

### 2. Create a Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file with API keys
```bash
AGENTQL_API_KEY=your_agentql_api_key
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key  # optional
LANGCHAIN_TRACING_V2="true"  # optional
LANGCHAIN_PROJECT=ApplyWizard  # optional
```

### 5. Run the example
Create a `run.py` file with the following content:

```python
import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_utils.create_embeddings import create_new_embedding  # Note: fixed typo
from langchain_utils.langgraph_react_agent import get_react_agent
from langchain import hub
from agental_utils.get_application import get_form_files
from agental_utils.fill_form import fill_the_form, flatten_and_filter_questions
from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import AgentExecutor

load_dotenv()

# Example usage (pseudo-code – adapt to your actual workflow)
def main():
    try:
        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        
        # Load job application form (replace with actual URL or file path)
        form_url = "https://example.com/job-application"
        
        # Fetch form fields
        form_data = get_form_files(form_url)
        
        # Flatten questions
        questions = flatten_and_filter_questions(form_data)
        
        # Create agent
        agent = get_react_agent(llm, tools=...)
        executor = AgentExecutor(agent=agent, tools=..., verbose=True)
        
        # Execute form filling
        result = fill_the_form(questions, user_data_path="resume.pdf")
        print("Application completed:", result)
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
```

### Troubleshooting
- **API Key errors**: Ensure you have set all required keys in `.env`.
- **Import errors**: If you see `ModuleNotFoundError: No module named 'langchain_utils.cretae_embaddings'`, rename the directory to `langchain_utils` and fix the import to `create_embeddings`.
- **Form not detected**: Verify the URL is accessible and contains a valid form.

---

## 📚 Documentation

For full API reference and architecture, see the [docs](./docs/) folder (coming soon).

## 🤝 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.