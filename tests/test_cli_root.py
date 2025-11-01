import pathlib
import sys
import unittest
from io import StringIO
from typing import Iterator
from unittest.mock import patch

from rich.console import Console

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from apt_toolkit import __version__
from apt_toolkit import cli_root
import apt_toolkit.cli  # ensure analyzer module is importable during tests


class AptRootCliTests(unittest.TestCase):
    def _make_console(self) -> Console:
        return Console(
            file=StringIO(),
            force_terminal=False,
            color_system=None,
            width=120,
        )

    def test_version_flag_outputs_package_version(self):
        console = self._make_console()

        with patch("apt_toolkit.cli_root.Console", return_value=console):
            exit_code = cli_root.main(["--version"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(console.file.getvalue().strip(), __version__)

    def test_analyzer_delegates_to_cli_main_preserving_arguments(self):
        console = self._make_console()
        call_count = {"value": 0}

        def fake_main():
            call_count["value"] += 1
            self.assertEqual(
                sys.argv,
                ["apt-analyzer", "initial-access", "--json"],
            )
            return 0

        with patch("apt_toolkit.cli_root.Console", return_value=console):
            with patch("apt_toolkit.cli.main", side_effect=fake_main):
                exit_code = cli_root.main(
                    ["analyzer", "initial-access", "--json"],
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(call_count["value"], 1)

    def test_interactive_shell_displays_catalog_and_exits(self):
        console = self._make_console()
        inputs: Iterator[str] = iter(["exit"])

        exit_code = cli_root.launch_interactive_shell(
            console=console,
            input_provider=lambda _: next(inputs),
        )

        output = console.file.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("APT Toolkit Interactive Console", output)
        self.assertIn("initial-access", output)
        self.assertIn("Campaign Simulations", output)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
