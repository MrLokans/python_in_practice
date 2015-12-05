class Text(object):

    def __init__(self, x, y, text, fontsize):
        self.x = x
        self.y = y
        self.rows = [list(text)]


class Diagram(object):

    #  example skipping of constructor

    def add(self, component):
        for y, row in enumerate(component.rows):
            for x, char in enumerate(row):
                self.diagram[y + component.y][x + component.x] = char

SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" font-family="sans-serif" font-size="{fontsize}">{text}</text>"""
SVG_SCALE = 20


class SvgText(object):

    def __init__(self, x, y, text, fontsize):
        x *= SVG_SCALE
        y *= SVG_SCALE
        fontsize *= SVG_SCALE // 10
        # turns into x=x, y=y, etc
        self.svg = SVG_TEXT.format(**locals())


class DiagramFactory(object):

    def make_diagram(self, w, h):
        return Diagram(w, h)

    def make_rectangle(self, x, y, w, h, fill="white", stroke="black"):
        return Rectangle(x, y, w, h, fill, stroke)

    def make_text(self, x, y, text, fontsize=12):
        return Text(x, y, text, fontsize)


class SvgDiagramFactory(object):

    def make_diagram(self, w, h):
        return SvgDiagram(w, h)

    def make_rectangle(self, x, y, w, h, fill="white", stroke="black"):
        return SvgRectangle(x, y, w, h, fill, stroke)

    def make_text(self, x, y, text, fontsize=12):
        return SvgText(x, y, text, fontsize)


def main():
    txt_diagram = create_diagram(DiagramFactory())
    txt_diagram.save(text_filename)

    svg_diagram = create_diagram(SvgDiagramFactory())
    svg_diagram.save(svg_filename)


def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
    rectangle = factory.make_rectangle(4, 1, 22, 5, "yellow")
    text = factory.make_text(7, 3, "Abstract Factory")
    diagram.add(rectangle)
    diagram.add(text)
    return diagram

if __name__ == '__main__':
    main()
