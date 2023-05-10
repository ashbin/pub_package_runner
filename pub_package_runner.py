import requests
import re
import subprocess
import sys
import os
from collections import deque
from pathlib import Path
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse



def findDirectory(start_dir, folder_name):
    print(f"Searching for {folder_name} in {start_dir}")
    # Use os.walk() to recursively search for the folder
    for dirpath, dirnames, filenames in os.walk(start_dir):
        if folder_name in dirnames:
            # If the folder is found, change the working directory to it
            folder_path = os.path.join(dirpath, folder_name)
            # os.chdir(folder_path)
            print(f"Found {folder_name} at {folder_path}")
            return folder_path
            break
    else:
        # If the folder is not found, print an error message
        print(f"Could not find {folder_name} in {start_dir}")
        return start_dir

def findFilePathBfs(start_dir , file_name):
    # Use a deque to perform a breadth-first search
    queue = deque()
    queue.append(start_dir)

    print(f"Searching for {file_name} in {start_dir}")


    while queue:
        current_dir = queue.popleft()
        for dirpath, dirnames, filenames in os.walk(current_dir):
            print(f"Searching for {file_name} in {dirpath}")
            if file_name in filenames:
                # If the file is found, change the working directory to its parent folder
                file_path = os.path.join(dirpath, file_name)
                parent_dir = os.path.dirname(file_path)
                print(f"Found {file_name} at {file_path}")
                # Exit the loop and the while loop once the file is found
                queue.clear()
                return parent_dir
                break
        else:
            # If the file is not found, add all subdirectories to the queue
            subdirs = [os.path.join(dirpath, dirname) for dirname in dirnames]
            queue.extend(subdirs)



parser = argparse.ArgumentParser(description="Run example project of pub package")
parser.add_argument("package", metavar="Package", help="the pub.dev package name")
parser.add_argument("-d", "--depth", type=int, default=1, help="the depth of the clone (default: 1)")
parser.add_argument("-s", "--studio", type=str, default='/Applications/Android Studio.app', help="the Android Studio application path(default: /Applications/Android Studio.app)")
parser.add_argument("-f", "--flutter", type=str, default='flutter', help="the flutter binary path(default: flutter)")

args = parser.parse_args()

package_name = args.package
# Get the repository URL of the package from pub.dev
url = f"https://pub.dev/packages/{package_name}"
response = requests.get(url)

if response.status_code != 200:
    print(f"Failed to retrieve package information for {package_name}")
    sys.exit(1)

html = response.text
pattern = r'<a class="link" href="(https://github.com/.*?)".*?>Repository \(GitHub\)</a>'
match = re.search(pattern, html)

if not match:
    print(f"No repository found for {package_name}")
    sys.exit(1)

repo_url = match.group(1)

print(f"Found repository {repo_url}")

directory_url = repo_url
git_url = ""
# Loop until a Git clone URL is found or the directory URL becomes invalid
while True:
    # print(f"Searching git clone url in {directory_url}")
    # Send a GET request to the directory URL and get the HTML content
    response = requests.get(directory_url)
    if response.status_code == 404:
        print("Invalid directory URL.")
        break
    html_content = response.content

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the Git clone URL from the HTML using a CSS selector
    git_link = soup.select_one('clipboard-copy[value$=".git"]')

    # Check if a Git link was found
    if git_link is not None:
        git_url = git_link['value']
        # Print the Git clone URL
        print(git_url)
        break
    else:
        # Remove the last path from the directory URL
        parsed_url = urlparse(directory_url)
        directory_url = urljoin(directory_url, parsed_url.path.rsplit('/', 1)[0])


# Clone the repository
print(f"Cloning repository {git_url}")
subprocess.run(["git", "clone", f"--depth={args.depth}", git_url])


# Set the folder name to search for
folder_name = package_name

# Set the starting directory for the search
start_dir = Path.cwd()
package_directory = findDirectory(start_dir, folder_name)
os.chdir(package_directory)

#search for package name again : as in some cases same will be repeated for mobile/web
package_directory = findDirectory(package_directory, folder_name)
os.chdir(package_directory)


example_dir = findDirectory(package_directory, "example")

# os.chdir("./example")

# Set the file name to search for
file_name = "pubspec.yaml"

# Set the starting directory for the search
start_dir = example_dir

file_path = findFilePathBfs(start_dir, file_name)

print(f"Running flutter app from {file_path}")
os.chdir(file_path)
os.system(f"{args.flutter} run")
os.system(f"open -a '{args.studio}' .")
