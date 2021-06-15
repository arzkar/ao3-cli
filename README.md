<h1 align="center">ao3-cli</h1>

A CLI to download from archiveofourown.org using their built-in download option.<br/><br/>
To report issues for the CLI, open an issue at https://github.com/arzkar/ao3-cli/issues<br/>

### Features:

- Download works & series from archiveofourown.org
- It also supports downloading all works or series from any archiveofourown.org page.<br/><br/>

# Installation

## Using pip (Recommended)

```
pip install -U ao3-cli
```

## From Source (Might have bugs, for development use)

```
pip install git+https://github.com/arzkar/ao3-cli@main
```

# Usage

```
> ao3_cli
Usage: ao3_cli [OPTIONS]

  A CLI to download from archiveofourown.org

  To report issues for the CLI, open an issue at
  https://github.com/arzkar/ao3-cli/issues

Options:
  -u, --url TEXT       The url of the fanfiction enclosed within quotes
  -i, --infile TEXT    Give a filename to read URLs from
  -l, --list-url TEXT  Enter a comma separated list of urls to download,enclosed within quotes
  -o, --out-dir TEXT   Absolute path to the Output directory for files(default: Current Directory)
  -f, --format TEXT    Download Format: EPUB (default), AZW3, MOBI, PDF or HTML
  --force              Force overwrite of an existing file
  --get-urls TEXT      Get all story urls found from a page
  -d, --debug          Show the log in the console for debugging
  --log                Save the logfile for debugging
  -v, --version        Display version & quit.
  --help               Show this message and exit.
```

## Example

- To download using a URL

```
ao3_cli -u https://archiveofourown.org/works/10916730/chapters/24276864
```

- To download using a file containing URLs

```
ao3_cli -i urls.txt
```

- To download using a comma separated list of URLs

```
ao3_cli -l "https://archiveofourown.org/works/31923052/chapters/79053661,https://archiveofourown.org/works/31950595"
```

### Default Configuration

- The fanfiction will be downloaded in epub format. To change it, use `-f` followed by the format.
- The fanfiction will be downloaded in the current directory. To change it, use `-o` followed by the path to the directory.

Check `ao3_cli --help` for more info.
