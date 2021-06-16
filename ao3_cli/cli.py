import click
import sys
from loguru import logger
from datetime import datetime
from colorama import init, Fore

from .utils.processing import get_format_type, show_urls_from_page
from .utils.fetch_data import FetchData

init(autoreset=True)  # colorama init
time = datetime.now().strftime("%H_%M_%S")


# @logger.catch  # for internal debugging
@click.command(no_args_is_help=True)
@click.option('-u', '--url', help='The url of the fanfiction enclosed within quotes ')
@click.option('-i', '--infile', help='Give a filename to read URLs from')
@click.option('-l', '--list-url', 'list_url',  help='Enter a comma separated list of urls to download, enclosed within quotes')
@click.option('-o', '--out-dir', 'out_dir', default="", help='Absolute path to the Output directory for files (default: Current Directory)')
@click.option('-f', '--format', '_format', default="epub", help='Download Format: EPUB (default), AZW3, MOBI, PDF or HTML')
@click.option('--force', default=False, help=' Force overwrite of an existing file', is_flag=True)
@click.option('--get-urls', 'get_urls', default=None, help='Get all story urls found from a page')
@click.option('-d', '--debug', default=False, help='Show the log in the console for debugging', is_flag=True)
@click.option('--log', default=False, help='Save the logfile for debugging', is_flag=True)
@click.option('-v', '--version', default=False, help='Display version & quit.', is_flag=True)
def run_cli(infile: str, url: str, list_url: str, _format: str, get_urls: str,
            out_dir: str, debug: bool, version: bool, log: bool, force: bool):
    """
    A CLI to download from archiveofourown.org using their built-in download option

    To report issues for the CLI, open an issue at https://github.com/arzkar/ao3-cli/issues
    """

    if log:
        debug = True
        click.echo(
            Fore.GREEN + f"Creating ao3_cli_{time}.log in the current directory")
        logger.add(f"ao3_cli_{time}.log")

    format_type = get_format_type(_format)
    if infile:
        fic = FetchData(format_type, out_dir, force,
                        debug)
        fic.get_fic_with_infile(infile)

    elif list_url:
        fic = FetchData(format_type, out_dir, force,
                        debug)
        fic.get_fic_with_list(list_url)

    elif url:
        fic = FetchData(format_type, out_dir, force,
                        debug)
        fic.get_fic_with_url(url)

    elif get_urls:
        fic = FetchData(debug)
        fic.get_urls_from_page(get_urls)
        fic.exit_status = show_urls_from_page(fic)

    if version:
        click.echo("Version: 0.1.2")
        sys.exit(0)

    sys.exit(fic.exit_status)
