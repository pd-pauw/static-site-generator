from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown:str)-> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
           continue
        block = block.strip()
        new_blocks.append(block)
    return new_blocks

def block_to_block_type(block:str) -> BlockType:
    first_char = block[0]
    if first_char == "#": 
        count_char = block.count("#")
        if block[count_char] == " ":
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH
    if first_char == "`":
        if block[:4] == "```\n" and block[-3:] == "```":
            return BlockType.CODE
        else:
            return BlockType.PARAGRAPH
    lines = block.split("\n")
    count = 0
    for line in lines:
        if line.startswith(first_char):
            count += 1
        else:
            count = 0
            break
    if count == len(lines):
        return BlockType.QUOTE if first_char == ">" else BlockType.UNORDERED_LIST
    for i in range(len(lines)):
        if lines[i].startswith(f"{i+1}."):
            count += 1
        else:
            count = 0
            break
    if count == len(lines):
        return BlockType.ORDERED_LIST
   
    return BlockType.PARAGRAPH
