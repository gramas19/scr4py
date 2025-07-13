from colorama import Fore
import os

class FileHandler:
    def __init__(self, cli):
        self.cli = cli
        self.api_endpoint_file = "api-endpoints.txt"
        self.endpoints = self._load_existing_endpoints(self.api_endpoint_file)
        if self.cli.args.output:
            self.words = self._load_existing_endpoints(self.cli.args.output)
        else:
            self.words = set()

    # Filetype: text, html, json, xml
    # TODO: add extension check
    def save(self, words, filetype="text"):
        if self.cli.args.output:
            new_words = set(words) - self.words  # endast nya ord
            if not new_words:
                return
            try:
                with open(self.cli.args.output, "a") as f:
                    for word in new_words:
                        f.write(word + "\n")
                        self.words.add(word)  # uppdatera interna listan också
            except Exception as e:
                print(Fore.RED + f"Error writing to file: {e}" + Fore.WHITE)

    def save_api_endpoints(self, candidates):
        api_common_names = [
            "api/", 
            "v0/", 
            "v1/", 
            "v2/", 
            "v3/",
            "graphql/",
            "admin/",
            "rest/",
            "json/",
            "user/",
            "account/",
            "auth/"
        ]
        for endpoint in candidates:
            if any(name in endpoint for name in api_common_names) and endpoint not in self.endpoints:
                self._write_to_file(self.api_endpoint_file, endpoint)
        
    def _write_to_file(self, filename, endpoint):
        try:
            with open(filename, "a") as f:
                f.write(endpoint + "\n")
            self.endpoints.add(endpoint)
            if self.cli.args.verbose:
                print(Fore.GREEN + f"Saved: {endpoint}" + Fore.WHITE)
        except FileNotFoundError:
            print(Fore.YELLOW + "File not found. Creating api-endpoints.text" + Fore.WHITE)
        except PermissionError:
            print(Fore.RED + "No permission to create file - CHECK PERMISSIONS" + Fore.WHITE)
        except OSError:
            print(Fore.RED + "File could not be created" + Fore.WHITE)

    def _load_existing_endpoints(self, filename):
        try:
            with open(filename, "r") as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            return set()