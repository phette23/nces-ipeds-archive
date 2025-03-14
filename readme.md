# Downloading NCES IPEDS Data

DOI for dataset: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15028111.svg)](https://doi.org/10.5281/zenodo.15028111)

Tools to download and double-check the [IPEDS](https://nces.ed.gov/ipeds) survey data from the U.S. [NCES](https://nces.ed.gov/).

Note that [another copy of this data](https://www.datalumos.org/datalumos/project/218981/version/V1/view) is already preserved in ICPSR's DataLumos repository. If you view the [IPEDS scraping](https://www.datalumos.org/datalumos/project/218981/version/V1/view?path=/datalumos/218981/fcr:versions/V1/Supplementary-Information/IPEDS-Scraping.html&type=file) HTML file it contains instructions on downloading all the IPEDS data using R.

## How To

Go to the IPEDS Data Center and select "all years" in the dropdown menu to load a table with all existing data onto the page. Paste [the browser copy script](./browser-copy-urls.js) into your browser's JavaScript console which copies a list of all the dataset URLs from the table to your clipboard. Paste them into a plain text file.

This is a full list of everything we want to download. I added year separator lines between each annual set of URLs manually, but it would be better to edit the browser JS to do this. The other scripts expect the years to know how to put them into annual subfolders.

```txt
2023
https://nces.ed.gov/ipeds/datacenter/data/ADM2023.zip
https://nces.ed.gov/ipeds/datacenter/data/ADM2023_Data_Stata.zip
...
2022
https://nces.ed.gov/ipeds/datacenter/data/ADM2022.zip
...
```

Download the data like: `./filedl.fish years-urls.txt | tee -a download.log`. Downloads into a folder structure like:

- IPEDS
  - 2023
    - ADM2023.zip
    - ADM2023_Data_Stata.zip
    - all the other 2023 files...
  - 2022
    - ADM2022.zip
    - etc...

It took about 20 minutes per year with two-second pauses in between request. There was no sign that NCES was rate limiting so this could've been much quicker with no `sleep` statements and parallel requests.

It comes to about 2.4GB of data and 6912 files, all of which are zip archives. The [urlcheck script](./urlcheck.py) can then double-check that every URL in the text file has a corresponding zip file in our folders.

## Complete Steps in Shell Commands

These steps were done on a macbook. There are other ways to install `uv` and `fish` shell for other systems; consult those tools' installation guides.

Setup:

```sh
# install homebrew if you don't have it https://brew.sh/
brew install fish uv
uv install
```

Run:

```sh
./filedl.fish years-urls.txt | tee -a download.log # download the data
find IPEDS -name .DS_Store -delete # clean up macos junk
uv run python urlcheck.py years-urls.txt # check that files exist & are zips
tar cf IPEDS-1980-2023.tar --directory=IPEDS . # one tar for everything
```

I didn't think it was worth it to compress the tarball because all the individual data files are already zipped.

## LICENSE

[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/deed.en)
