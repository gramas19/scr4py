from colorama import Fore
import os

class FileHandler:
    def __init__(self):
        self.api_endpoint_file = "api-endpoints.txt"
        self.endpoints = self._load_existing_endpoints(self.api_endpoint_file)

    # Filetype: text, html, json, xml
    def save(self, filename, filetype="text"):
        # TODO: Save result to a custom file
        pass

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
                print(endpoint)
        
    def _write_to_file(self, filename, endpoint):
        try:
            with open(filename, "a") as f:
                f.write(endpoint + "\n")
            self.endpoints.add(endpoint)
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