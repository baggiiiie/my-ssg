class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        # NOTE: when this is called, it should go recursively to the children
        if not self.children:
            return ""
        html_text = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            # if not isinstance(child, HTMLNode):
            #     print(type(child))
            #     print(child)
            #     raise TypeError("Children must be HTMLNode instances")
            html_text += child.to_html()
        return html_text + f"</{self.tag}>"

    def props_to_html(self) -> str:
        html_text = ""
        for key, value in self.props.items():
            html_text += f' {key}="{value}"'
        return html_text

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict | None = None,
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.tag = tag
        self.value = value
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode's value cannot be None")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict | None = None,
    ):
        super().__init__(tag=tag, value=None, children=children, props=props)
        if not tag:
            raise ValueError("ParentNode's tag cannot be None")
        if not children:
            raise ValueError("ParentNode's children cannot be None")
        self.tag = tag
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self) -> str:
        html_text = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            # if not isinstance(child, HTMLNode):
            #     raise TypeError("ParentNode's children must be HTMLNode instances")
            # NOTE: CONTEXT SWITCH - how to call `.to_html()` on child? when the child has children, `list.to_html()` is called and it raises errors
            html_text += child.to_html()

        html_text += f"</{self.tag}>"
        return html_text
