

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    
    def to_html(self):
        if self.tag is None:
            return self.value or ""
    
        props = self.props_to_html()
    
        if self.children is None:
            children_html = self.value or ""
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
        
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"

    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            result = ""
            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return result
    
    def __repr__(self):
        return f'HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})'
    

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.props = props
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value
        elif self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            result = ""
            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return f'<{self.tag}{result}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,children=None,props=props)
        self.children = children

    def to_html(self):
        
        if self.tag is None:
            raise ValueError
        elif self.children is None:
            print(f"Debug children: {self.children}") 
            raise ValueError("Missing Children")
        else:
            result = f'<{self.tag}>'
            for child in self.children:
                result += child.to_html()
            result += f'</{self.tag}>'
            return result