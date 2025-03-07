import ollama
from pydantic import BaseModel
from model.aiAssistant import ai_assistant


SELECTED_MODEL = 'qwen2.5-coder:0.5b'
# SELECTED_MODEL = 'qwen2.5-coder:1.5b'
# SELECTED_MODEL = 'qwen2.5-coder:3b'

class cleanCodeCheckOutputFormat(BaseModel):
    cleanCodeGradeJustification: str
    # cleanCodeGrade: int
    additionalExpectationsMet: str

class cleanCodeCheckNoAdditionalExpectationsOutputFormat(BaseModel):
    cleanCodeGradeJustification: str
    # cleanCodeGrade: int

# Function to get response from the AI model
def get_response(expectations_content,code_content):
    cleanCodeExpectations = \
        '1. Make sure variable and function names have at least three words in their name, are formatted correctly in camelCase or snake_case, and named to accurately describe their functionality.\n' \
        '2. Methods and Functions are at most 5 lines of text, dedicated specifically to doing one task, and no more than that one task.\n' \
        '3. There needs to be at most one comment per method and function describing the functionality of the structure. Any more than one is not allowed.\n' \
        '4. There needs to be at most one blank line between structures. Any more than one is not allowed.\n' \
        '5. The code must be properly indented and formatted. Any code that is not properly indented and formatted is not allowed.\n'
    detectedErrors = ai_assistant(code_content)
    if expectations_content != '':
        response = ollama.chat(
            model=SELECTED_MODEL,
            format=cleanCodeCheckOutputFormat.model_json_schema(),
            messages=[
                {
                    'role': 'user', 
                    'content': (
                        f'Given the following code:\n{code_content}\n\n'
                        f'Inspect the code for the following expectations:\n{cleanCodeExpectations}\n\n'
                        f'Additionally, list the following additional expectations and if each one is met:\n{expectations_content}\n\n'
                        f'If there are syntax errors, they will be included here, alongside the line number for each error. Please heavily factor this into your conclusion: :\n{detectedErrors}\n\n'
                        'Do not provide solutions or recommendations to the feedback, nor a list of each of the expectations with an explanation for each. Instead only provide feedback on the code as a single sentence response for each expectation.\n'
                        )
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
                        'content': (
                        f'Given the following code:\n{code_content}\n\n'
                        f'Inspect the code for the following expectations:\n{cleanCodeExpectations}\n\n'
                        f'If there are syntax errors, they will be included here, alongside the line number for each error. Please heavily factor this into your conclusion: \n{detectedErrors}\n\n'
                        'Do not provide solutions or recommendations to the feedback, nor a list of each of the expectations with an explanation for each. Instead only provide feedback on the code as single sentence responses.\n'
                        )
                }
            ]
        )

    return response['message']['content']