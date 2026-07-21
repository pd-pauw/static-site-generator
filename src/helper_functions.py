import os
import shutil

def copy_directory(source_dir, destination_dir):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)
    copy_recursive(source_dir, destination_dir)

def copy_recursive(source_dir, destination_dir):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)
    
        if os.path.isdir(source_path):
            os.mkdir(destination_path)
            copy_recursive(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)
            print(f"Copied: {source_path} -> {destination_path}")

def extract_title(markdown:str) -> str:
    lines =  markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[1:]
            return title.strip()
    return "No title"

