from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore
from ErrorHandler import ErrorHandler
from UserAgentHandler import UserAgentHandler
import requests, urllib3
import re
import time
import warnings
import sys

class EndpointFinder:
    links_to_visit = set()
    visisted_links = set()
    found_endpoints = set()

    err_handler = ErrorHandler()
    user_headers = {
        "User-Agent" : UserAgentHandler.get_default()
    }

    # Initialize every url with https://
    def __init__(self, url, file_handler, verify=True):
        self.base_url = url if url.startswith("http") else "https://" + url
        self.file_handler = file_handler
        self.verify = verify
        self.warning_count = 0
        self.url_error_count = 0 # URL connection tries

    def run(self):
        self._extract_links(self.base_url)

    def _parse_js(self, js_url):
        if js_url in self.visisted_links:
            return
        self.visisted_links.add(js_url)
        # TODO: This will be used with verbose output
        print(js_url)

        try:
            response = requests.get(js_url, verify=self.verify, header=self.user_headers)
            js_text = response.text
            self._find_endpoints(js_text, js_url)
        except Exception:
            pass

    def _find_endpoints(self, text, source_url):
        if not self.is_url_in_whitelist(source_url):
            return 

        candidates = re.findall(r'["\'](/[\w\-/]+)["\']', text)
        for endpoint in candidates:
            clean_endpoint = str(endpoint).strip("/")
            if clean_endpoint not in self.found_endpoints:
                # Skip short endpoint names in case of garbage
                if len(clean_endpoint) > 2:
                    self.found_endpoints.add(clean_endpoint)

    def _extract_words_from_endpoint(self, endpoint):
        # TODO: Extract words from endpoint where endpoint does not contain the word api
        pass

    def _check_for_garbage(self, link):
        # Look for garbage urls in site. Extend list to skip more
        garbage_keywords = ["cloudflare", "google", "youtube"]
        domain = urlparse(link).netloc.lower()
        for word in garbage_keywords:
            if word in domain:
                    return True
            return False
            
    def _visit_link(self, full_url, path, extension):
        if extension == "" or path.endswith(extension):
                endpoint = path.split("/")[-1].replace(extension, "")
                if endpoint and endpoint not in self.found_endpoints:
                    self.found_endpoints.add(endpoint)
                self._extract_links(full_url)

    # Try to handle error and retry connection on misspelled URLs
    def _retry_connection(self, url):
        self.url_error_count = self.url_error_count + 1
        if self.url_error_count == 3:
            sys.exit(Fore.RED + "Could not fix broken URL. Check your spelling" + Fore.WHITE)
        if url in self.visisted_links:
                self.visisted_links.remove(url)
                self.base_url = self.err_handler.fix_url(url)
                self._extract_links(self.base_url)

    def is_url_in_whitelist(self, url):
        whitelist_keywords = ["jquery"]
        whitelist = urlparse(self.base_url).netloc
        # Count amount of dots in url to get the domain name and TLD
        dot_count = str(whitelist).count(".")
        split_url = whitelist.split(".")
        domain = split_url[dot_count - 1]
        tld = split_url[dot_count]

        # match all subdomains for given url
        pattern = rf"^(https?:)?\/\/([a-z0-9-]+\.)*{domain}\.{tld}"
        match = re.match(pattern, url)
        if match or any(kw in url for kw in whitelist_keywords):
            return True

    def _extract_links(self, url):
        if url in self.visisted_links:
            return
        else:
            self.visisted_links.add(url)
            # TODO: This will be used with verbose output
            print(url)
        #time.sleep(1)
        try:
            response = requests.get(url, verify=self.verify, headers=self.user_headers)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            for tag in soup.find_all(["a", "script", "link", "frame", "iframe"]):
                attribute = "href" if tag.name in ["a", "link"] else "src"
                link = tag.get(attribute)
                # if link != None and not str(link).startswith("mailto"):
                #     print(link)

                if not link:
                    continue

                if "http" in link or "//" in link and link != None:
                    if not self.is_url_in_whitelist(link):
                        # Skip if link starts with http or // and is not in whitelist
                        continue

                if self._check_for_garbage(link):
                    continue
                
                full_url = urljoin(self.base_url, link)
                path = urlparse(full_url).path
                # TODO: this is a user option
                # if "." not in path.split("/")[-1]:
                #     # if no extension, visit the link, eg. /start, /register
                #     self._visit_link(full_url, path, "")

                self._visit_link(full_url, path, ".php")
                self._visit_link(full_url, path, ".asp")
                self._visit_link(full_url, path, ".jsp")


                if path.endswith(".js"):
                    self._parse_js(full_url)
                if path.endswith(".html") or path.endswith("/"):
                    self._extract_links(full_url)

            self._find_endpoints(html, url)
            
        except requests.exceptions.ConnectionError:
            # Warn user about the error, then try to disable verify used in requests.get
            try:
                if self.warning_count == 3:
                    sys.exit(Fore.RED + "Failed to verify, please check the url. Exiting..." + Fore.WHITE)
                self.warning_count = self.warning_count + 1
                print(Fore.YELLOW + "Could not verify SSL certificate, trying to disable..." + Fore.WHITE)
                warnings.filterwarnings("ignore", message="Unverified HTTPS request") # Ignore InsecureRequestWarning
                self.verify = False
                if self.base_url in self.visisted_links:
                    self.visisted_links.remove(self.base_url)
                    self._extract_links(url)
            except KeyboardInterrupt:
                sys.exit(Fore.RED + "User exited" + Fore.WHITE)
        except urllib3.exceptions.LocationParseError:
            print(Fore.RED + "Error: URL is misspelled, please check your settings." + Fore.WHITE)
            print(Fore.YELLOW + "Trying to fix broken URL..." + Fore.WHITE)
            self._retry_connection(url)
        except requests.exceptions.InvalidURL:
            print(Fore.RED + "Error: URL is misspelled, please check your settings." + Fore.WHITE)
            print(Fore.YELLOW + "Trying to fix broken URL..." + Fore.WHITE)
            self._retry_connection(url)
        except requests.exceptions.MissingSchema:
            sys.exit(Fore.RED + "Protocol mismatch, check your spelling" + Fore.WHITE)
        except KeyboardInterrupt:
            sys.exit(Fore.RED + "User exited" + Fore.WHITE)

        print("Found endpoints:", self.found_endpoints)
        self._extract_words_from_endpoint(self.found_endpoints)
        self.file_handler.save_api_endpoints(self.found_endpoints)


        print("Visited links: ", self.visisted_links)