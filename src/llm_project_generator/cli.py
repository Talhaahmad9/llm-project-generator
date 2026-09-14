import argparse
import sys
from pathlib import Path
from collections.abc import Sequence

from llm_project_generator.errors import GeneratorError
from llm_project_generator.generator import generate_project
from llm_project_generator.providers import resolve_provider


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-project-generator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init = subparsers.add_parser("init", help="create a new project")
    init.add_argument("destination", type=Path)
    init.add_argument("--provider", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        provider = resolve_provider(args.provider)
        destination = generate_project(args.destination, provider)
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Created {destination} using provider {provider.name}.")
    return 0
