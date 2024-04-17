import json
import sys
import os
import re

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)
# Now you can import the scraper module
from codescraper import scraper

'''operators_keywords = [
        '==', '!=', '<=', '>=', '->', '\+=', '-=', '\*=', '/=', '//=', '%=', '@=', '&=', '\|=',
        '\^=', '>>=', '<<=', '\*\*', '\+\+', '--', '=', '\+', '-', '\*', '/', '//', '%', '@',
        '<', '>', '\|', '\^', '&', '~', '>>', '<<', '\(', '\)', '\[', '\]', '\{', '\}', ',', ':',
        '\.', ';', ' and ', ' or ', ' not ', ' is ', ' in ', ' if ', ' else ', ' elif ', ' while ',
        ' for ', ' break ', ' continue ', ' return ', ' yield ', ' with ', ' assert ', ' del ',
        ' pass ', ' raise ', ' import ', ' from ', ' as ', ' global ', ' nonlocal ', ' lambda ',
        ' def ', ' class ', ' try ', ' except ', ' finally ', ' async ', ' await '
    ]

def adjust_spaces(code_content):
    # Create a regex pattern to match operators and keywords
    pattern = r'(?<!\s)(' + '|'.join(map(re.escape, operators_keywords)) + r')(?!\s)'

    # Add space before and after each operator/keyword
    code_content = re.sub(pattern, r' \1 ', code_content)

    # Replace multiple spaces with a single space
    code_content = re.sub(r'\s+', ' ', code_content)

    return code_content

def remove_comments(code_content):
    # Use regular expression to remove comments
    code_content = re.sub(r'#.*?\n', '\n', code_content)
    code_content = re.sub(r'\'\'\'.*?\'\'\'', '', code_content, flags=re.DOTALL)
    code_content = re.sub(r'\"\"\".*?\"\"\"', '', code_content, flags=re.DOTALL)
    return code_content


def vectorize(code_content):

    code_content = remove_comments(code_content)
    
    code_content = adjust_spaces(code_content)
    
    words = code_content.split()
    
    return words'''
    
import re

operators = [
    '==', '!=', '<=', '>=', '->', '+=', '-=', '*=', '/=', '//=', '%=', '@=', '&=', '|=',
    '^=', '>>=', '<<=', '**', '++', '--', '=', '+', '-', '*', '/', '//', '%', '@',
    '<', '>', '|', '^', '&', '~', '>>', '<<'
]

parentheses_punctuation = ['(', ')', '[', ']', '{', '}', ',', ':', ';']

keywords = [
    'and', 'or', 'not', 'is', 'in', 'if', 'else', 'elif', 'while',
    'for', 'break', 'continue', 'return', 'yield', 'with', 'assert', 'del',
    'pass', 'raise', 'import', 'from', 'as', 'global', 'nonlocal', 'lambda',
    'def', 'class', 'try', 'except', 'finally', 'async', 'await',
    'True', 'False', 'None'
]

def adjust_spaces(code_content):
    # Combine operators and parentheses into one list for the pattern
    combined_list = operators + parentheses_punctuation

    # Create a regex pattern to match combined items
    pattern = r'(?<!\s)(' + '|'.join(map(re.escape, combined_list)) + r')(?!\s)'

    # Add space before and after each item in the combined list
    code_content = re.sub(pattern, r' \1 ', code_content)

    # Replace multiple spaces with a single space
    code_content = re.sub(r'\s+', ' ', code_content)

    return code_content

def remove_comments(code_content):
    # Use regular expression to remove comments
    code_content = re.sub(r'#.*?\n', '\n', code_content)
    code_content = re.sub(r'\'\'\'.*?\'\'\'', '', code_content, flags=re.DOTALL)
    code_content = re.sub(r'\"\"\".*?\"\"\"', '', code_content, flags=re.DOTALL)
    return code_content

def vectorize(code_content):
    code_content = remove_comments(code_content)
    code_content = adjust_spaces(code_content)
    words = code_content.split()
    filtered_words = [word for word in words if not any(keyword in word for keyword in keywords) and word not in parentheses_punctuation]
    return filtered_words

def add_entry_to_json_file(link, vector, filename="dataset.json"):
    """
    Add a new entry to a JSON file of objects with members 'link' and 'vector'.
    If the file does not exist, it creates the file and adds the object.

    Args:
    link (str): The link to be added.
    vector (str): The vector to be added.
    filename (str): The name of the JSON file.
    """

    if os.path.exists(filename):

        with open(filename, 'r') as file:
            data = json.load(file)
    else:

        data = []


    new_entry = {"link": link, "vector": vector}

  
    data.append(new_entry)


    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
