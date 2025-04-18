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
        raise NotImplementedError("Currently not implemented")

    def props_to_html(self) -> str:
        html_text = ""
        for key, value in self.props.items():
            html_text += f' {key}="{value}"'
        return html_text

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, value: str | None = None):
        super().__init__(tag, value)
        self.tag = tag
        self.value = value
        self.children = []
        self.props = {}

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Value cannot be None")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
