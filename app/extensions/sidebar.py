class MenuElement():
    def render(self):
        return ''

class MenuLabel(MenuElement):
    def __init__(self, label):
        self.label = label

    def render(self):
        return """
            <p class="menu-label">
                {}
            </p>
            """.format(self.label)

class MenuLink(MenuElement):
    def __init__(self, label, href=""):
        self.label = label
        self.href = href

    def render(self):
        return """
        <a href={}>
            {}
        </a>
        """.format(self.href, self.label)

class MenuList(MenuElement):
    def __init__(self, head=None, children=[]):
        self.head = head
        self.children = children

    def render(self):
        lines = [self.head.render()] if self.head is not None else []
        lines.append('<ul class="menu-list">')
        for child in self.children:
            lines.append('<li>')
            lines.append(child.render())
            lines.append('</li>')
        lines.append('</ul>')
        return '\n'.join(lines)

# TODO: technically this could be formatted better, if this was ever to be
# expanded fully into a flask plugin
# This makes use of the bulma-collapsible extension
class MenuCollapsibleList(MenuElement):
    def __init__(self, collapsible_id, label, href, children, mouseover=False):
        self.collapsible_id = collapsible_id
        self.label = label
        self.href = href
        self.children = children
        self.mouseover = mouseover

    def render(self):
        name = f'collapsible-div-{self.collapsible_id}'
        print(name)

        if self.mouseover:
            lines = ['<div onmouseover="mouseover_expand(this)" onmouseout="mouseover_collapse(this)">']
            lines.append(f'<a href="{self.href}">{self.label}</a>')
        else:
            lines = [f'<a href="#{name}" data-action="collapse">{self.label}</a>']
        lines.append(f'<div id="{name}" class="is-collapsible">')
        lines.append('<ul>')
        for child in self.children:
            lines.append('<li>')
            lines.append(child.render())
            lines.append('</li>')
        lines.append('</ul>')
        lines.append('</div>')
        if self.mouseover:
            lines.append('</div>')
        print(lines)
        return '\n'.join(lines)

class Menu(MenuElement):
    def __init__(self, children=[]):
        self.children = children

    def render(self):
        lines = ['<aside class="menu">']
        for child in self.children:
            lines.append(child.render())
        lines.append('</aside>')
        return '\n'.join(lines)
