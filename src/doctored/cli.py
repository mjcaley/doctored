from pathlib import Path
import typer

from .pipeline import pipeline
# from .parser import rest_parser


def command(path: Path):
    # document = rest_parser(path)
    # typer.echo(document)
    pipeline(path)


def main():
    typer.run(command)
