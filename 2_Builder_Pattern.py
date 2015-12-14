import abc
# Top level form building

htmlForm = create_login_form(HtmlFormBuilder())
with open(HtmlFilename, "w", encoding="utf-8") as f:
    f.write(htmlForm)

tkForm = create_login_form(TkFormBuilder())
with open(TkFilename, "w", encoding="utf-8") as f:
    f.write(tkForm)


def create_login_form(builder):
    builder.add_title("login")
    builder.add_label("username", 0, 0, target="username")
    builder.add_entry("password", 1, 0, target="password")
    builder.add_entry("password", 1, 1, kind="password")
    builder.add_button("Login", 2, 0)
    builder.add_button("Cancel", 2, 1)
    return builder.form()


# Abstract class our builders will inherit from
# this class can not be instantiated
class AbstractFormBuilder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_title(self, title):
        self.title = title

    @abc.abstractmethod
    def form(self):
        pass

    @abc.abstractmethod
    def add_label(self, text, row, column, **kwargs):
        pass


class HtmlFormBuilder(AbstractFormBuilder):

    def __init__(self):
        self.title = "HtmlFormBuilder"
        self.items = {}

    def add_title(self, title):
        super().add_title(escape(title))

    def add_label(self, text, row, column, **kwargs):
        self.items[(row, column)] = ('<td><label for="{}"> {}: </label></td>'
            .format(kwargs.get("target", ""), escape(text)))

    def add_entry(self, var, row, column, **kwargs):
        html = """<td><input name="{}" type="{}" /></td>""".format(
            var, kwargs.get("kind", "text"))
        self.items[(row, column)] = html

    def form(self):
        html = ["<!doctype html>\n<html><head><title>{}</title></head>"
                "<body>".format(self.title), '<form><table border="0">']
        thisRow = None

        for key, value in sorted(self.items.items()):
            row, column = key
            if not thisRow:
                html.append(" <tr>")
            elif thisRow != row:
                html.append(" </tr>\n <tr>")
            thisRow = row
            html.append("   " + value)
        html.append(" </tr>\n</table></form></body></html>")
        return "\n".join(html)
