import os
import subprocess
from pathlib import Path

def find_requirements_files():
    """Find all requirements.txt files"""
    requirements_files = []
    
    # Find requirements.txt in root directory
    root_req = Path(os.path.dirname(os.path.abspath(__file__))) / 'requirements.txt'
    if root_req.exists():
        requirements_files.append(root_req)
    
    # Find requirements.txt files in tools directory
    tools_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'tools'
    if tools_dir.exists():
        for req_file in tools_dir.rglob('requirements.txt'):
            requirements_files.append(req_file)
    return requirements_files

def get_all_requirements():
    """Get all requirements and deduplicate"""
    requirements = set()
    for req_file in find_requirements_files():
        with open(req_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.add(line)
    return requirements

def install_requirements():
    """Install all dependencies directly"""
    requirements = get_all_requirements()
    print("Starting to install dependencies...")
    try:
        subprocess.check_call(['pip', 'install'] + list(requirements))
        print("All dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")

if __name__ == '__main__':
    install_requirements()