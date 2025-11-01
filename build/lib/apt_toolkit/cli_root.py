"""
Unified command-line entry point for the APT Toolkit.

Running ``apt`` without arguments now launches an interactive, colourful shell
that highlights the toolkit's tradecraft modules and campaign simulations.
Sub-commands are delegated to the existing CLI implementations.
"""

from __future__ import annotations

import argparse
import shlex
import sys
from importlib import import_module
from typing import Callable, Dict, Optional, Sequence, Tuple

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .catalog import get_campaign_catalog, get_tool_catalog

try:
    from .cli import CHINESE_APT_SUPPORT
except Exception:  # pragma: no cover - defensive fallback
    CHINESE_APT_SUPPORT = False

# Mapping of sub-command name -> (module, attribute, help text)
_DELEGATE_TABLE: Dict[str, Tuple[str, str, str]] = {
    "analyzer": (
        "apt_toolkit.cli",
        "main",
        "Run the classic analyzer CLI (advanced modules, reports, tooling).",
    ),
}

# Lazily populated cache so repeated invocations do not keep re-importing.
_DELEGATE_CACHE: Dict[str, Callable[[], int]] = {}


def _load_delegate(command: str) -> Callable[[], int]:
    """
    Lazily import and fetch the callable that backs a delegated command.

    A dedicated helper keeps import semantics isolated and simplifies testing,
    where we can patch the imported attribute.
    """

    if command in _DELEGATE_CACHE:
        return _DELEGATE_CACHE[command]

    module_name, attribute, _ = _DELEGATE_TABLE[command]
    module = import_module(module_name)
    try:
        delegate = getattr(module, attribute)
    except AttributeError as exc:  # pragma: no cover - defensive guard
        raise RuntimeError(
            f"Delegate '{command}' is misconfigured: "
            f"{module_name}.{attribute} is missing."
        ) from exc

    _DELEGATE_CACHE[command] = delegate
    return delegate


def _invoke_delegate(command: str, delegate: Callable[[], int], args: Sequence[str]) -> int:
    """
    Execute the delegated entry point while preserving intuitive sys.argv state.

    We temporarily replace ``sys.argv`` so that the downstream argparse logic
    sees exactly the arguments the user provided after the ``apt`` prefix.
    """

    argv_snapshot = sys.argv
    sys.argv = [f"apt-{command}", *args]
    try:
        result = delegate()
    finally:
        sys.argv = argv_snapshot

    return int(result) if isinstance(result, int) else 0


def _build_delegate_table() -> Table:
    """Return a rich table detailing delegated commands."""

    table = Table(
        title="[bold cyan]Delegated Commands[/]",
        box=box.ROUNDED,
        highlight=True,
    )
    table.add_column("Command", style="bold cyan")
    table.add_column("Description", style="white")

    for command, (_, _, description) in sorted(_DELEGATE_TABLE.items()):
        table.add_row(command, description)

    return table


def _build_tool_table(chinese_support: bool) -> Table:
    """Return a table summarising the available analyzer modules."""

    table = Table(
        title="[bold green]Tradecraft Modules[/]",
        box=box.ROUNDED,
        highlight=True,
    )
    table.add_column("Category", style="magenta")
    table.add_column("Module", style="bold cyan")
    table.add_column("Description", style="white")
    table.add_column("Try It", style="green")

    for entry in get_tool_catalog(chinese_support):
        table.add_row(
            entry["category"],
            entry["module"],
            entry["description"],
            entry["command_hint"],
        )

    return table


def _build_campaign_table(chinese_support: bool) -> Table:
    """Return a table highlighting available campaign orchestrations."""

    table = Table(
        title="[bold yellow]Campaign Simulations[/]",
        box=box.ROUNDED,
        highlight=True,
    )
    table.add_column("Category", style="magenta")
    table.add_column("Scenario", style="bold cyan")
    table.add_column("Description", style="white")
    table.add_column("Launch", style="green")

    campaigns = get_campaign_catalog(chinese_support)
    if campaigns:
        for entry in campaigns:
            table.add_row(
                entry["category"],
                entry["name"],
                entry["description"],
                entry["command_hint"],
            )
    else:
        table.add_row(
            "Campaigns",
            "Optional data pack missing",
            "Install the Chinese APT campaign bundle to unlock comparative simulations.",
            "Visit repository documentation",
        )

    return table


def _render_shell_intro(console: Console, chinese_support: bool) -> None:
    """Render the welcome panel and tables when the shell starts."""

    console.print(
        Panel.fit(
            "[bold magenta]APT Toolkit Interactive Console[/]\n"
            "[cyan]Advanced Persistent Threat simulation suite for authorised operators[/]\n"
            f"[white]Version {__version__}[/]",
            border_style="magenta",
        )
    )
    console.print(_build_tool_table(chinese_support))
    console.print(_build_campaign_table(chinese_support))
    console.print(_build_delegate_table())
    console.print(
        Panel(
            "[bold]Type[/] [green]help[/] for shell shortcuts or "
            "[green]exit[/] to quit.",
            border_style="cyan",
        )
    )


def _print_shell_help(console: Console) -> None:
    """Display interactive shell shortcuts."""

    console.print(
        Panel(
            "\n".join(
                [
                    "[bold cyan]Interactive Shortcuts[/]",
                    "[green]modules[/]     Reprint the tradecraft module catalog.",
                    "[green]campaigns[/]   Reprint the campaign simulation catalog.",
                    "[green]commands[/]    Show delegated console commands.",
                    "[green]run <args>[/]  Execute an analyzer module (e.g. run initial-access --json).",
                    "[green]analyzer <...>[/] Directly forward arguments to the classic analyzer CLI.",
                    "[green]clear[/]       Clear the screen and re-render the welcome banner.",
                    "[green]help[/]        Display this help message.",
                    "[green]exit[/]/[green]quit[/]  Leave the interactive shell.",
                ]
            ),
            border_style="cyan",
        )
    )


def launch_interactive_shell(
    *,
    console: Optional[Console] = None,
    input_provider: Optional[Callable[[Console], str]] = None,
) -> int:
    """
    Launch the interactive shell experience.

    Parameters
    ----------
    console:
        Optional rich Console. When omitted a standard Console is created.
    input_provider:
        Optional callable returning the next line of user input. Primarily used
        by unit tests to script interactions.
    """

    console = console or Console()
    chinese_support = bool(CHINESE_APT_SUPPORT)

    def _read() -> str:
        if input_provider is not None:
            return input_provider(console)
        return console.input("[bold cyan]apt[/] > ")

    _render_shell_intro(console, chinese_support)

    while True:
        try:
            raw = _read()
        except StopIteration:
            console.print("\n[yellow]End of scripted input. Terminating session.[/]")
            break
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Session closed by user.[/]")
            break

        if raw is None:
            console.print("[red]No input received; exiting shell.[/]")
            break

        command = raw.strip()
        if not command:
            continue

        lowered = command.lower()

        if lowered in {"exit", "quit"}:
            console.print("[bold green]Goodbye.[/]")
            return 0

        if lowered in {"help", "?"}:
            _print_shell_help(console)
            continue

        if lowered in {"modules", "tools"}:
            console.print(_build_tool_table(chinese_support))
            continue

        if lowered == "campaigns":
            console.print(_build_campaign_table(chinese_support))
            continue

        if lowered == "commands":
            console.print(_build_delegate_table())
            continue

        if lowered == "clear":
            console.clear()
            _render_shell_intro(console, chinese_support)
            continue

        delegate_args: Optional[Sequence[str]] = None

        if lowered.startswith("analyzer"):
            delegate_args = shlex.split(command)[1:]
        elif lowered.startswith("apt-analyzer"):
            delegate_args = shlex.split(command)[1:]
        elif lowered.startswith("run "):
            delegate_args = shlex.split(command[4:])
            if not delegate_args:
                console.print("[red]Usage: run <module> [options][/]")
                continue
        else:
            console.print(
                f"[red]Unknown command '{command}'. "
                "Type 'help' to see available shortcuts.[/]"
            )
            continue

        if delegate_args is None:
            console.print("[red]No analyzer arguments supplied.[/]")
            continue

        try:
            delegate = _load_delegate("analyzer")
        except (ImportError, RuntimeError) as exc:
            console.print(f"[red]Error loading analyzer: {exc}[/]")
            continue

        console.print(
            f"[cyan]→ Running analyzer with arguments:[/] "
            f"[white]{' '.join(delegate_args) or '(none)'}[/]"
        )
        exit_code = _invoke_delegate("analyzer", delegate, delegate_args)
        if exit_code != 0:
            console.print(f"[red]Analyzer exited with status {exit_code}[/]")

    console.print("[bold green]Goodbye.[/]")
    return 0


def _print_command_list(console: Console) -> None:
    """Print the delegated command list using the provided console."""

    console.print(_build_delegate_table())


def main(
    argv: Optional[Sequence[str]] = None,
    *,
    console: Optional[Console] = None,
    input_provider: Optional[Callable[[Console], str]] = None,
) -> int:
    """
    Entry point for the ``apt`` console script.

    Parameters
    ----------
    argv:
        Optional iterable of arguments to parse instead of ``sys.argv``.
    console:
        Optional rich Console for output redirection/testing.
    input_provider:
        Optional callable used to feed interactive input during tests.
    """

    console = console or Console()
    args_to_parse = list(argv) if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="apt",
        description="APT Toolkit consolidated command-line interface.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the installed apt-toolkit version and exit.",
    )
    parser.add_argument(
        "--list",
        dest="list_commands",
        action="store_true",
        help="List all available delegated commands.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=sorted(_DELEGATE_TABLE),
        help="Delegated command to execute.",
    )

    parsed_args, remainder = parser.parse_known_args(args_to_parse)

    if parsed_args.version:
        console.print(__version__)
        return 0

    if parsed_args.list_commands:
        _print_command_list(console)
        return 0

    if not parsed_args.command:
        return launch_interactive_shell(console=console, input_provider=input_provider)

    try:
        delegate = _load_delegate(parsed_args.command)
    except (ImportError, RuntimeError) as exc:
        console.print(f"[red]Error: {exc}[/]")
        return 1

    return _invoke_delegate(parsed_args.command, delegate, remainder)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
