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
        self.children = children if children else []
        self.props = props if props else {}

    def to_html(self) -> str:
        html_text = f"<{self.tag}{self.props_to_html()}>" if self.tag else ""

        if self.children:
            for child in self.children:
                if not isinstance(child, HTMLNode):
                    raise TypeError("ParentNode's children must be HTMLNode instances")
                html_text += child.to_html()

        html_text += f"</{self.tag}>" if self.tag else ""
        if self.tag != "pre":
            # Replace \n with <br> for all tags except code
            html_text = html_text.replace(r"\n", "<br>")
        return html_text

    def props_to_html(self) -> str:
        html_text = ""
        for key, value in self.props.items():
            html_text += f' {key}="{value}"'
        return html_text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str = "",
        value: str = "",
        props: dict | None = None,
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.tag != "img" and not self.value:
            raise ValueError("LeafNode's value cannot be None")
        html_text = f"<{self.tag}{self.props_to_html()}>" if self.tag else ""
        html_text += f"{self.value}"
        html_text += f"</{self.tag}>" if self.tag else ""
        if self.tag != "code":
            html_text.replace(r"\n", "<br>")
        return html_text


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict | None = None,
    ):
        if not tag:
            raise ValueError("ParentNode's tag cannot be None")
        if not children:
            raise ValueError("ParentNode's children cannot be None")
        super().__init__(
            tag=tag,
            value=None,
            children=children,
            props=props,
        )
