from pprint import pprint

class MenuElement():
    def __init__(self, elem_id=None):
        self.elem_id = elem_id

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

class MenuNumericRange(MenuElement):
    def __init__(self, pre_label, mid_label, post_label):
        self.pre_label = pre_label
        self.mid_label = mid_label
        self.post_label = post_label

    def render(self):
        return """
        <a>
            <div class="has-text-dark">
                <span style="">{}</span>
                <input style="width: 40px" class="input" type="text">{}
                <input style="width: 40px" class="input" type="text">
                <button class="button is-success">
                    <span class="icon is-small">
                        <i class="fas fa-chevron-right"></i>
                    </span>
                    {}
                </button>
            </div>
        </a>
        """.format(self.pre_label, self.mid_label, self.post_label)

class MenuCheckbox(MenuElement):
    def __init__(self, prelabel, label, *args, **kwargs):
        self.prelabel = prelabel
        self.label = label
        super().__init__(*args, **kwargs)

    def render(self):
        return """
            <label for="{}">
                <a>
                    {}
                    <label class="checkbox">
                        <input type="checkbox" id={}>
                            {}
                        </input>
                    </label>
                </a>
            </label>
        """.format(self.elem_id, self.prelabel, self.elem_id, self.label)


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
# Replace the 'label' with a head element that gets rendered
# Include kwargs
class MenuCollapsibleList(MenuElement):
    def __init__(self, collapsible_id, head, href, children, mouseover=False):
        self.collapsible_id = collapsible_id
        self.is_label = isinstance(head, str)
        if isinstance(head, str):
            self.label = head
        else:
            self.label = head.render()
        self.href = href
        self.children = children
        self.mouseover = mouseover

    def render(self):
        name = f'collapsible-div-{self.collapsible_id}'

        if self.mouseover:
            lines = ['<div onmouseover="mouseover_expand(this)" onmouseout="mouseover_collapse(this)">']
            if self.is_label:
                lines.append(f'<a href="{self.href}">{self.label}</a>')
            else:
                lines.append(self.label)
        else:
            if self.is_label:
                lines = [f'<a href="#{name}" data-action="collapse">{self.label}</a>']
            else:
                raise NotImplementedError('Can\'t use non-label header to open menu')

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
        pprint(lines)
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
