import requests
import os

def get_file_content(raw_url):
    """
    Retrieves the content of a file from a given raw URL.

    Args:
    raw_url (str): The raw URL of the file to be downloaded.

    Returns:
    str: The content of the file as text if the request is successful; otherwise, None.
    """
    response = requests.get(raw_url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve content: {response.status_code}")
        return None
    
def get_raw_url(url):
    """
    Converts a GitHub file URL to its corresponding raw file URL.

    Args:
    url (str): The GitHub URL of the file.

    Returns:
    str: The raw URL of the file.
    """
    url = url.replace("github.com", "raw.githubusercontent.com")
    url = url.replace("/blob/", "/")
    return url

#da cancellare
def download_and_save_file(file_url, save_path):
    """
    Downloads a file from a given URL and saves it to a specified path.

    Args:
    file_url (str): The URL of the file to download.
    save_path (str): The path where the file should be saved.
    """
    content = get_file_content(file_url)
    if content:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w') as file:
            file.write(content)
            
def get_py_files(github_url, github_token, branch='master'):
    """
    Retrieves a list of download URLs for all Python files in a given GitHub repository.

    Args:
    github_url (str): The URL of the GitHub repository.
    github_token (str): GitHub token for API authentication.
    branch (str): The branch of the repository to search. Defaults to 'master'.

    Returns:
    list: A list of URLs for downloading Python files in the repository.
    """
    def extract_user_repo(github_url):
        parts = github_url.split('/')
        user, repo = parts[-2], parts[-1]
        return user, repo

    user, repo = extract_user_repo(github_url)
    base_url = f"https://api.github.com/repos/{user}/{repo}/contents/"
    files = []

    def walk_directory(path=''):
        nonlocal files
        url = base_url + path
        headers = {'Authorization': f'token {github_token}'}
        params = {'ref': branch}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            contents = response.json()
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.py'):
                    files.append(item['download_url'])
                elif item['type'] == 'dir':
                    walk_directory(item['path'])
        else:
            print("failed retriving file")
            return

    walk_directory()

    return files
