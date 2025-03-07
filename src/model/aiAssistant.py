import re

TEST_FILE_PATH = 'src/model/badPythonCodeTest.txt'

# Function to read the file to a string FOR TESTING PURPOSES
def read_file_to_string(TEST_FILE_PATH: str) -> str:
    with open(TEST_FILE_PATH, 'r') as file:
        return file.read()

# Check for variable and function names, method/function length, comments per method, blank lines between structures, and indentation/formatting
def check_code_quality(code: str) -> dict:
    issues = {
        "possibly_bad_variable_function_names": [],
        "method_function_length": [],
        "comments_per_method": [],
        "missing_blank_lines_between_structures": [],
        "missing_indentation_formatting": []
    }

    # Initialize variables
    lines = code.split('\n')
    method_function_lines = []
    comment_count = 0
    blank_line_count = 0
    inside_method_function = False

    # For each line in the provided file
    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Check for variable and function names
        check_variable_function_names(stripped_line, i, issues)

        # Check for method/function length and comments
        check_method_function_length_and_comments(stripped_line, i, issues, method_function_lines, comment_count, inside_method_function)

        # Check for blank lines between structures
        check_blank_lines_between_structures(stripped_line, i, issues, blank_line_count, lines)

        # Check for proper indentation and formatting
        check_indentation_formatting(line, i, issues)

    # Return the issues found
    return issues

# Check for unclean variable and function names. 
# Specifically check for single letter names, if the name is not in camelCase or snake_case, and if the name is made of less than three words
def check_variable_function_names(stripped_line, i, issues):
    # Skip comment lines
    if stripped_line.startswith('//') or stripped_line.startswith('#') or '/*' in stripped_line and '*/' in stripped_line:
        return
    
    # Skip words in strings and string literals
    stripped_line = re.sub(r'(["\']).*?\1', '', stripped_line)
    
    # Skip library functions for C, C++, Java, and Python
    library_functions = {'print', 'def', 'return', 'if', 'else', 'for', 'while', 'switch', 'case', 'break', 'continue', 
        'class', 'import', 'from', 'try', 'except', 'finally', 'with', 'as', 'lambda', 'yield', 'raise', 'assert', 'pass', 
        'global', 'nonlocal', 'del', 'True', 'False', 'None', 'and', 'or', 'not', 'is', 'in', 'async', 'await', 'self', 
        'super', 'public', 'private', 'protected', 'static', 'final', 'void', 'int', 'float', 'double', 'char', 'boolean', 
        'byte', 'short', 'long', 'new', 'this', 'instanceof', 'enum', 'interface', 'extends', 'implements', 'throws', 'throw', 
        'synchronized', 'volatile', 'transient', 'native', 'goto', 'const', 'sizeof', 'typedef', 'struct', 'union', 'extern', 
        'register', 'auto', 'signed', 'unsigned', 'inline', 'restrict', 'complex', 'imaginary', 'bool', 'true', 'false', 'null', 
        'nullptr', 'constexpr', 'decltype', 'noexcept', 'static_assert', 'thread_local', 'alignas', 'alignof', 'char16_t', 
        'char32_t', 'wchar_t', 'override', 'final', 'friend', 'virtual', 'explicit', 'mutable', 'namespace', 'using', 'template', 
        'typename', 'operator', 'dynamic_cast', 'static_cast', 'reinterpret_cast', 'const_cast', 'typeid', 'decltype', 'concept', 
        'requires', 'co_await', 'co_yield', 'co_return'}
    stripped_line = re.sub(r'\b(' + '|'.join(re.escape(word) for word in library_functions) + r')\b(?=\s*[\(\)])', '', stripped_line)
    stripped_line = ' '.join(word for word in stripped_line.split() if word not in library_functions)

    # Check for variable and function names
    variable_function_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')
    matches = variable_function_pattern.findall(stripped_line)
    
    # Add the variable and function names to the issues list
    issues["possibly_bad_variable_function_names"].extend(
    (i + 1, match) for match in matches
    if (len(match) == 1 and match.isalpha()) or 
       (not re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', match) and not re.match(r'^[a-z]+(?:_[a-z]+)*$', match)) or
       (re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', match) and len(re.findall(r'[A-Z][a-z]+', match)) < 2) or
       (re.match(r'^[a-z]+(?:_[a-z]+)*$', match) and len(match.split('_')) < 3)
)

# Check for method/function length and comments
def check_method_function_length_and_comments(stripped_line, i, issues, method_function_lines, comment_count, inside_method_function):
    if stripped_line.startswith(('def ', 'class ')):
        if inside_method_function:
            issues["method_function_length"].append((i + 1, len(method_function_lines)))
            issues["comments_per_method"].append((i + 1, comment_count))
            method_function_lines.clear()
            comment_count = 0
        inside_method_function = True

    if inside_method_function:
        method_function_lines.append(stripped_line)
        if stripped_line.startswith('#'):
            comment_count += 1

    if inside_method_function and stripped_line == '':
        inside_method_function = False
        issues["method_function_length"].append((i + 1, len(method_function_lines)))
        issues["comments_per_method"].append((i + 1, comment_count))
        method_function_lines.clear()
        comment_count = 0


# Check for blank lines between structures
def check_blank_lines_between_structures(stripped_line, i, issues, blank_line_count, lines):
    if stripped_line == '':
        blank_line_count += 1
    else:
        if stripped_line.startswith(('def ', 'class ')):
            if i == 0 or (lines[i - 1].strip() != '' and not lines[i - 1].strip().startswith('#')):
                issues["missing_blank_lines_between_structures"].append(i + 1)
        blank_line_count = 0

# Check for proper indentation and formatting
def check_indentation_formatting(line, i, issues):
    stripped_line = line.lstrip()
    indent_level = len(line) - len(stripped_line)
    
    # Check if the line is inside a function or class definition
    if stripped_line.startswith(('def ', 'class ')):
        expected_indent = 0
    elif stripped_line.startswith(('elif ', 'else:', 'except ', 'finally:')):
        expected_indent = indent_level - 4
    elif stripped_line.startswith(('return', 'pass', 'break', 'continue', 'raise')):
        expected_indent = indent_level - 4
    else:
        expected_indent = indent_level

    # Check if the indentation is a multiple of 4 spaces
    if indent_level % 4 != 0:
        issues["missing_indentation_formatting"].append((i + 1, "Indentation is not a multiple of 4 spaces"))

    # Check if the indentation level is appropriate
    if indent_level != expected_indent:
        issues["missing_indentation_formatting"].append((i + 1, f"Expected indent level: {expected_indent}, found: {indent_level}"))

def main():
    # Read the file to a string
    code = read_file_to_string(TEST_FILE_PATH)

    # Check the code quality
    issues = check_code_quality(code)

    # Print the issues found
    print("Code Quality Issues:")
    for issue_type, issue_list in issues.items():
        print(f"{issue_type}: {issue_list}")

if __name__ == "__main__":
    main()