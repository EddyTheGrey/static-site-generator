class HTMLNode:
    def __init__(self, tag:str = None, value:str = None, children:list = None, props:dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")
    
    def props_to_html(self):
        if self.props:
            return ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        return ''

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag:str, value:str, props:dict = None):
        super().__init__(tag=tag, value=value, children=[], props=props)
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return str(self.value) 
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list, props:dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"