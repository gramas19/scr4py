import argparse
import sys

class CLIArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="A tool for finding endpoints and filenames",
            prog="scr4py.py"
            )
        self._setup_arguments()
        self.args = self.parser.parse_args()

        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            sys.exit(1)

    def _setup_arguments(self):
        # TODO: Add more arguments to the list
        # Verbose mode, output-file, output format, scan all option, ratelimit, headers, random user agent,
        # disable SSL
        self.parser.add_argument("-u", "--url", help="The URL to scan", required=True)
        self.parser.add_argument("-v", "--verbose", help="Enable detailed output", action="store_true")
        self.parser.add_argument("-o", "--output-file", help="Write result to a file", dest="output")
        self.parser.add_argument("-of", "--output-format", help="output format: text, json, html", choices=["text", "json", "html"], default="text")
        self.parser.add_argument("-A", "-all", help="Scan everything", action="store_true")
        self.parser.add_argument("--rate", help="Set rate limit")
        self.parser.add_argument("-H", "--header", help="Set request headers")
        self.parser.add_argument("--random-user-agent", help="Randomize the user-agent each request", action="store_true", dest="rua")
        self.parser.add_argument("--ignore", help="Disable SSL verification", action="store_true")