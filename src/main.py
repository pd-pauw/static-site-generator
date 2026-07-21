from textnode import TextNode, TextType
from helper_functions import copy_directory, extract_title
from generate_page import generate_pages_recursive, generate_page

def main():
    print("hello")
    copy_directory("static/", "public/")
    ##generate_page("content/index.md","template.html", "public/index.html")
    generate_pages_recursive("content/","template.html", "public/")


main()