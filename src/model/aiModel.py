import ollama
from pydantic import BaseModel

SELECTED_MODEL = 'qwen2.5-coder:0.5b'

class cleanCodeCheckOutputFormat(BaseModel):
    cleanCodeGradeJustification: str
    # cleanCodeGrade: int
    additionalChecksList: str

class cleanCodeCheckNoAdditionalExpectationsOutputFormat(BaseModel):
    cleanCodeGradeJustification: str
    # cleanCodeGrade: int

# Function to get response from the AI model
def get_response(expectations_content,code_content):
    cleanCodeExpectations = \
        '1. Make sure variables are at least three words in their name formatted in camelCase or snake_case, and accurately describe their functionality. Any less than three words is not allowed. Variable names formatted any other way are not allowed.\n' \
        '2. Methods and Functions are at most 5 lines of text, dedicated specifically to doing one task, and no more than that one task.\n' \
        '3. There needs to be at most one comment per method and function describing the functionality of the structure. Any more than one is not allowed.\n' \
        '4. There needs to be at most one blank line between structures. Any more than one is not allowed.\n' \
        '5. The code must be properly indented and formatted. Any code that is not properly indented and formatted is not allowed.\n'
    if expectations_content != '':
        response = ollama.chat(
            model=SELECTED_MODEL,
            format=cleanCodeCheckOutputFormat.model_json_schema(),
            messages=[
                {
                    'role': 'user', 
                    'content': f'Given the following code:\n{code_content}\n\nInspect the code for the following expectations:\n{cleanCodeExpectations}\n\nAdditionally, inspect the code for the following expectations:\n{expectations_content}\n\nDo not provide solutions or recommendations to the feedback, only provide feedback on the code as single sentence responses.\n'
                }
            ]
        )
    else:
        response = ollama.chat(
            model=SELECTED_MODEL,
            format=cleanCodeCheckNoAdditionalExpectationsOutputFormat.model_json_schema(),
            messages=[
                {
                    'role': 'user', 
                    'content': f'Given the following code:\n{code_content}\n\nInspect the code for the following expectations:\n{cleanCodeExpectations}\n\nDo not provide solutions or recommendations to the feedback, only provide feedback on the code as single sentence responses.\n'
                }
            ]
        )

    return response['message']['content']