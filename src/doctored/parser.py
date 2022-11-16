from docutils import frontend, utils
from docutils.parsers.rst import Parser


def rest_parser(file):
    settings = frontend.get_default_settings(Parser)
    with open(file) as f:
        content = f.read()
        document = utils.new_document(f.name, settings)
        Parser().parse(content, document)

        return document
