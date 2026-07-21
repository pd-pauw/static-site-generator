from textnode import TextNode, TextType
from helper_functions import copy_directory, extract_title
from generate_page import generate_pages_recursive, generate_page
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print("hello")
    copy_directory("static/", "docs/")
    ##generate_page("content/index.md","template.html", "public/index.html")
    generate_pages_recursive("content/","template.html", "docs/", basepath)


main()