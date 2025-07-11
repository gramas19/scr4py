#from ErrorHandler import ErrorHandler
from EndpointFinder import EndpointFinder
from CLIArguments import CLIArguments
from FileHandler import FileHandler
import subprocess
import sys
import importlib

def install_from_requirements(requirements_file="requirements.txt"):
    try:
        with open(requirements_file, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Extract package name without version
                package_name = line.split("==")[0].lower()

                if importlib.util.find_spec(package_name) is None:
                    print(f"Package '{package_name}' missing. Installing...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", line])
                else:
                    pass
                    #print(f"Package '{package_name}' is already installed.")
    except FileNotFoundError:
        print("requirements.txt could not be found.")
    except Exception as e:
        print("Error installing package:", e)

if __name__ == "__main__":

    install_from_requirements()
    # TODO: Add argument handling for different purposes
    cli = CLIArguments()
    
    file_handler = FileHandler()

    scraper = EndpointFinder(cli.args.url, file_handler)
    scraper.run()