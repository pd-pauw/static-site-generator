import os
from markdownfunctions import markdown_to_html_node
from helper_functions import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r", encoding="utf-8") as f:
            markdown = f.read()

        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except OSError as e:
        print(f"Error reading files: {e}")
        return

    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    html_content = html_node.to_html()

    html = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(source_path):
            # Recurse into subdirectory
            generate_pages_recursive(
                source_path,
                template_path,
                os.path.join(dest_dir_path, entry)
            )
        elif os.path.isfile(source_path) and entry.endswith(".md"):
            # Change .md extension to .html
            filename = os.path.splitext(entry)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, filename)

            generate_page(source_path, template_path, dest_path)