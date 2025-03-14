"""Check that we 1) have a file matching the end of the URL in the given annual directory
and 2) that that file is an actual zip archive. Usage:

    python urlcheck.py urls.txt [urlsfile]

if the second argument is "urlsfile" then the script prints in a format that can be fed
into filedl.fish, e.g. a year and list of missing or non-zip URLs for that year. This
can be used to fill in the missing files."""

from pathlib import Path
import re
import sys
from urllib.parse import urlparse

import filetype


urlprefix = "https://nces.ed.gov/ipeds/datacenter/data/"
urlsfile = sys.argv[1]
if len(sys.argv) > 2:
    # urlsfile
    outputstyle = sys.argv[2]
else:
    outputstyle = None


def output(year, filename=None, msg=None):
    if year and not filename:
        if outputstyle == "urlsfile":
            return print(year)
        else:
            return print(f"Checking URLs for {year}")
    if year and filename:
        if outputstyle == "urlsfile":
            return print(f"{urlprefix}{filename}")
        else:
            return print(f"ERROR: {filename} from {year} is {msg}")


with open(urlsfile, "r") as fh:
    for line in fh.readlines():
        if re.match("^[0-9]{4}$", line):
            year = line.rstrip()
            output(year)
        else:
            url = urlparse(line)
            filename = url.path.split("/")[-1]
            path = Path("IPEDS") / year / filename
            if path.exists():
                guess = filetype.guess_mime(path)
                if not guess:
                    output(year, filename, "of indeterminate mime type")
                elif guess != "application/zip":
                    output(year, filename, "not a zip archive")
            else:
                output(year, filename, "missing")
