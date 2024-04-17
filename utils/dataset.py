import ast
import json
import os
import pandas as pd
from codeparser import parser
from codescraper import scraper
from utils.invertedindex import inverted_index

documents = {}

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


def extract_link_vector_pairs(filename="dataset.json"):
    """
    Extracts link-vector pairs from a JSON file.

    Args:
    filename (str): The name of the JSON file.

    Returns:
    list of tuples: A list of (link, vector) pairs.
    """
    pairs = []
    
    try:
        # Open and read the JSON file
        with open(filename, 'r') as file:
            data = json.load(file)
        
        # Extract link and vector pairs
        for entry in data:
            link = entry.get('link', None)
            vector = entry.get('vector', None)
            if link and vector:
                pairs.append((link, vector))
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except json.JSONDecodeError:
        print(f"There was an error decoding the JSON data in {filename}.")
    
    return pairs


def extract_repo_url_at_line(line_number, file_path="repos.csv"):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if line_number is within the range of the DataFrame
        if line_number < 0 or line_number >= len(df):
            print("Line number out of range.")
            return None

        # Extract and return the URL from the specified line
        # The column containing the URLs is 'repo_url'
        return df.iloc[line_number]['repo_url']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def download_files(github_token, number_of_repos):
    for i in range(0, number_of_repos):
        github_url = extract_repo_url_at_line(i)
        python_files = scraper.get_py_files(github_url, github_token)
        
        for file in python_files:
            file_content = scraper.get_file_content(file)
            parser.add_entry_to_json_file(file, str(parser.vectorize(file_content)))
            
def init():

    link_vector_pairs = extract_link_vector_pairs()

    for pair in link_vector_pairs:
        link, tokens_str = pair
        tokens = ast.literal_eval(tokens_str)  # Convert the string to a list
        inverted_index.update_index(link, tokens)
        documents[link] = tokens
        
    return link_vector_pairs

