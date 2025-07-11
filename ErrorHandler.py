import re
from colorama import Fore

class ErrorHandler:
    def fix_url(self, url):
        url = url.strip() # remove leading and trailing whitespace from url

        protocol = "https"
        if url.startswith("http://"):
            protocol = "http"
        elif url.startswith("https://"):
            protocol = "https"

        # Look for extra colons and slashes. Remove extras
        url = re.sub(r'^(http|https)[:/]+', '', url)
        
        # Look for extra dots in the URL and replace all occurences
        url = re.sub(r'\.{2,}', '.', url)

        cleaned_url = f"{protocol}://{url}"

        print(Fore.GREEN + "New URL set: " + cleaned_url + Fore.WHITE)
        return cleaned_url