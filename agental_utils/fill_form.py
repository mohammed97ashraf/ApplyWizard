import time
import agentql
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from playwright_dompath.dompath_sync import xpath_path

load_dotenv()

os.environ["AGENTQL_API_KEY"] = os.getenv("AGENTQL_API_KEY")

import time
from playwright.sync_api import sync_playwright

def flatten_and_filter_questions(input_data):
    for item in input_data:
        flattened_questions = []
        
        # Flatten the sub_questions into the main list
        for question in item['qustions_asksed']:
            if question.get('sub_questions'):
                # Add each sub_question to the flattened list
                flattened_questions.extend(question['sub_questions'])
            else:
                # Add the main question if no sub_questions exist
                flattened_questions.append(question)
        
        # Apply the filter: Remove 'upload your resume' and file input fields
        filtered_questions = [
            q for q in flattened_questions 
            if 'upload your resume' not in q['question']  or "Resume" not in q['question'] and q.get('input_filed_type') != 'file' 
        ]
        
        # Update the 'qustions_asksed' with the filtered and flattened questions
        item['qustions_asksed'] = filtered_questions
    
    return input_data
    

def fill_the_form(url: str, form_data: dict, resume_location_path: str) -> None:
    
    key_names = []
    
    # Build the key names based on form data
    for key, values in form_data.items():
        key_name = key.replace(' ', '_').replace('?', '').replace('-', '_').replace('(', '').replace(')', '').replace('/', '')
        
        if values in ["Yes", "No"]:
            key_name += f"_radio_options_{values}"
        
        key_names.append({key_name: values})
    
    # Format the questions by extracting keys from dictionaries
    formatted_questions = '\n'.join(list(d.keys())[0] for d in key_names) + '\nupload_resume\nsummit'
    
    # Add surrounding triple quotes for display
    formatted_string = '{' + '\n' + formatted_questions + '\n' + '}'
    print(type(formatted_string))
    print(formatted_string)
    
    # Playwright interaction
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
       
        page.goto(url)
        page.wait_for_load_state('load')

        response = page.query_elements(formatted_string)

        # Fill the form fields
        for key_dict in key_names:
            key_name = list(key_dict.keys())[0]  # Extract the key name
            value = key_dict[key_name]
            field = getattr(response, key_name, None)  # Dynamically access the response attribute
            
            if field:
                field.scroll_into_view_if_needed()
                time.sleep(2)
                
                if value in ["Yes", "No"]:  # Handle radio button selection
                    field.click()
                else:  # Handle typing text in the form field
                    field.type(value)
        
        # Upload the resume if applicable
        if response.upload_resume:
            response.upload_resume.scroll_into_view_if_needed()
            time.sleep(2)
            response.upload_resume.locator('input[type="file"]').set_input_files(resume_location_path)
        
        # Submit the form
        if response.summit:
            response.summit.scroll_into_view_if_needed()
            time.sleep(2)
            response.summit.click()

        time.sleep(2)
        page.close()
