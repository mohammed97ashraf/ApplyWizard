import agentql
from playwright.sync_api import sync_playwright
from playwright_dompath.dompath_sync import xpath_path
import os
import json
from dotenv import load_dotenv

load_dotenv()

os.environ["AGENTQL_API_KEY"] = os.getenv("AGENTQL_API_KEY")
# URL = "https://form.jotform.com/242476590759471"

# QUERY = """
# {
#     details[]
#     {
#         job_role
#         descption
#         all_qustions[]
#         {
#             question
#             input_filed_type
#             options
#         }
#     }
# }
# """


def get_form_files(url : str, query : str) ->dict:
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        page.goto(url)

        # Use query_data() method to fetch the data from the page
        response = page.query_data(query)

        # close page
        page.close()

        return response["details"]
