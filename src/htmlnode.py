class HTMLNode():
    def __init__(self, tag: str = None, value: str= None, children: list = None, props: dict[str,str]= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        result = ""
        if not self.props:
            return result
        for key_value in self.props.items():
            result += f' {key_value[0]}="{key_value[1]}"'
        return result
    
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"