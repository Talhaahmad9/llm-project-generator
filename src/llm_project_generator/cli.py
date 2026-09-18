import argparse
import sys
from pathlib import Path
from collections.abc import Sequence

from llm_project_generator.errors import GeneratorError
from llm_project_generator.generator import generate_project
from llm_project_generator.providers import PROVIDERS, ProviderSpec, resolve_provider


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-project-generator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init = subparsers.add_parser("init", help="create a new project")
    init.add_argument("destination", type=Path)
    init.add_argument(
        "--provider",
        help="select a provider directly; omit in a terminal for interactive selection",
    )
    return parser


def _select_provider() -> ProviderSpec | None:
    if not sys.stdin.isatty():
        print(
            "error: --provider is required for non-interactive use",
            file=sys.stderr,
        )
        return None

    print("Select a provider:")
    for number, provider in enumerate(PROVIDERS, start=1):
        print(f"  {number}. {provider.display_name}")

    while True:
        try:
            selection = input("Provider number: ")
        except (EOFError, KeyboardInterrupt):
            print("error: provider selection cancelled", file=sys.stderr)
            return None

        if not selection.strip().isdigit():
            print("Invalid provider number; try again.", file=sys.stderr)
            continue

        number = int(selection)
        if not 1 <= number <= len(PROVIDERS):
            print("Invalid provider number; try again.", file=sys.stderr)
            continue

        return PROVIDERS[number - 1]


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.provider is None:
            provider = _select_provider()
            if provider is None:
                return 2
        else:
            provider = resolve_provider(args.provider)
        destination = generate_project(args.destination, provider)
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Created {destination} using provider {provider.name}.")
    return 0
