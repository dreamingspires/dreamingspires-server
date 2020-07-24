class Timeline():
    def __init__(self, children):
        self.children = children

    def render(self):
        lines = ['<div class="timeline">']
        for child in self.children:
            lines.append(child.render())
        lines.append('</div>')
        return '\n'.join(lines)

class TimelineHeader():
    def __init__(self, text, classes):
        self.text = text
        self.classes = classes

    def render(self):
        return """
            <header class="timeline-header">
                <span class="tag {}">{}</span>
            </header>
        """.format(self.classes, self.text)

class TimelineItem():
    def __init__(self, marker_text, marker_classes, heading_text, body_text, \
            content_classes, line_classes):
        self.marker_text = marker_text
        self.heading_text = heading_text
        self.body_text = body_text
        self.content_classes = content_classes
        self.marker_classes = marker_classes
        self.line_classes = line_classes

    def render(self):
        return """
            <div class="timeline-item {}">
                <div class="timeline-marker {}">{}</div>
                <div class="timeline-content {}">
                    <p class="heading">{}</p>
                    <p>{}</p>
                </div>
            </div>
        """.format(self.line_classes, self.marker_classes, self.marker_text,
                self.content_classes, self.heading_text, self.body_text)
