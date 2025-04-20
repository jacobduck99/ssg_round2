VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr",
    "input", "link", "meta", "param",
    "source", "track", "wbr"
}  # "img" removed from void elements to allow </img>

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        attributes = [f'{prop}="{value}"' for prop, value in self.props.items()]
        return " " + " ".join(attributes)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
            
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
            
        if self.tag is None:
            return self.value.strip().replace("\n", "")  # Ensure whitespace and newlines are removed
        
        if self.tag in VOID_ELEMENTS:
            return f"<{self.tag}{self.props_to_html()} />"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value.strip()}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
    
        children_html = "".join(child.to_html().strip() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
