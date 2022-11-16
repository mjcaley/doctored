import typer

from .parser import rest_parser


def command(file: str):
    document = rest_parser(file)
    typer.echo(document)


def main():
    typer.run(command)
