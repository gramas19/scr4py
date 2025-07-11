# scr4py

Scr4py is a python reconaissance tool that identifies endpoints and generates wordlists based on websites naming conventions

## Installation

to download the script:

`git clone https://github.com/gramas19/scr4py.git`

Install required packages by running the script

_or_

by running `pip install requirements.txt`

# Example usage

This example shows how the script could be used

## Getting API endpoints from a website

`python scr4py.py -u https://example.com`

This will scrape the website example.com for .php, .asp, jsp and .js files to find endpoints.

If any endpoints are found, they will be stored in a file called _api-endpoints.txt_

## Save output of words/links

This option has not been implemented yet

# Usage

In order to run scr4py a URL needs to be defined as in the example above. The most basic use case for this script is to fetch endpoints from different websites.

```
usage: scr4py.py [-h] [-u URL] [-v VERBOSE] [-o OUTPUT_FILE] [-of OUTPUT_FORMAT] [-A A] [--rate RATE] [-H HEADER] [--random-user-agent RANDOM_USER_AGENT] [--ignore IGNORE]

A tool for finding endpoints and filenames

options:
    -h, --help show this help message and exit
    -u, --url                   URL The URL to scan
    -v, --verbose               Enable detailed output
    -o, --output-file           Write result to a file
    -of, --output-format        OUTPUT_FORMAT
                                output format: text, json, html
    -A, -all                    Scan everything
    --rate                      RATE Set rate limit
    -H, --header                Set request headers
    --random-user-agent         Randomize the user-agent each request
    --ignore                    Disable SSL verification
```

# When to use this script?

This script is perfect for gathering endpoints from different websites when you want to build your own lists of endpoints and files/directories to use when doing bug bounty hunting

# Note

This script is still in beta and will be updated
