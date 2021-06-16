import re
import requests
from tqdm import tqdm
from colorama import Fore, Style
from loguru import logger
from bs4 import BeautifulSoup
from rich.console import Console

from .ao3 import ArchiveOfOurOwn
from .logging import init_log, download_processing_log
from .processing import check_url, save_data

bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}, {rate_fmt}{postfix}, ETA: {remaining}"
console = Console()


class FetchData:
    def __init__(self, format_type="epub", out_dir="", force=False,
                 debug=False):
        self.format_type = format_type
        self.out_dir = out_dir
        self.force = force
        self.debug = debug
        self.exit_status = 0

    def get_fic_with_infile(self, infile: str):

        try:
            with open(infile, "r") as f:
                urls = f.read().splitlines()

        except FileNotFoundError:
            tqdm.write(
                Fore.RED +
                f"{infile} file could not be found. Please enter a valid file path.")
            exit(1)

        init_log(self.debug, self.force)
        if self.debug:
            logger.debug("Calling get_fic_with_infile()")

        url_list = []
        for url in urls:
            if not re.search(r"\barchiveofourown.org/works/\b", url):
                self.get_urls_from_page(url)
                if self.ao3_works_list:
                    url_list += self.ao3_works_list

            else:
                url_list.append(url)

        if not url_list:
            exit(1)

        with tqdm(total=len(url_list), ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            for url in url_list:

                supported_url, self.exit_status = check_url(
                    pbar, url, self.debug, self.exit_status)
                if supported_url:
                    try:
                        download_processing_log(self.debug, url)
                        fic = ArchiveOfOurOwn(url, self.debug,
                                              self.exit_status)
                        fic.get_fic_metadata(self.format_type)

                        # update the exit status
                        self.exit_status = fic.exit_status

                        if fic.ao3_works_name is None:
                            tqdm.write(
                                Fore.RED +
                                "Fanfiction not found")
                            self.exit_status = 1
                            continue

                        if fic.file_name is None:
                            self.exit_status = 1

                        else:
                            self.exit_status = save_data(
                                fic, self.out_dir,
                                fic.file_name,
                                fic.download_url, self.debug, self.force,
                                self.exit_status)

                        pbar.update(1)

                    # Error: 'ArchiveOfOurOwn' object has no attribute 'file_name'
                    # Reason: Unsupported URL
                    except AttributeError:
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    continue

    def get_fic_with_list(self, list_url: str):

        urls = list_url.split(",")

        init_log(self.debug, self.force)
        if self.debug:
            logger.debug("Calling get_fic_with_list()")

        url_list = []
        for url in urls:
            if not re.search(r"\barchiveofourown.org/works/\b", url):
                self.get_urls_from_page(url)
                if self.ao3_works_list:
                    url_list += self.ao3_works_list

            else:
                url_list.append(url)

        if not url_list:
            exit(1)

        with tqdm(total=len(url_list), ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            for url in url_list:

                supported_url,  self.exit_status = check_url(
                    pbar, url, self.debug, self.exit_status)

                if supported_url:
                    try:
                        download_processing_log(self.debug, url)
                        fic = ArchiveOfOurOwn(
                            url, self.debug, self.exit_status)
                        fic.get_fic_metadata(self.format_type)

                        # update the exit status
                        self.exit_status = fic.exit_status

                        if fic.ao3_works_name is None:
                            tqdm.write(
                                Fore.RED +
                                "Fanfiction not found")
                            self.exit_status = 1
                            continue

                        if fic.file_name is None:
                            self.exit_status = 1

                        else:
                            self.exit_status = save_data(
                                fic, self.out_dir,
                                fic.file_name,
                                fic.download_url, self.debug, self.force,
                                self.exit_status)

                        pbar.update(1)

                    # Error: 'ArchiveOfOurOwn' object has no attribute 'file_name'
                    # Reason: Unsupported URL
                    except AttributeError:
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    continue

    def get_fic_with_url(self, url: str):

        init_log(self.debug, self.force)
        if self.debug:
            logger.debug("Calling get_fic_with_url()")

        url_list = []
        if not re.search(r"\barchiveofourown.org/works/\b", url):
            self.get_urls_from_page(url)
            if self.ao3_works_list:
                url_list += self.ao3_works_list

        else:
            url_list.append(url)

        if not url_list:
            exit(1)

        with tqdm(total=len(url_list), ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            for url in url_list:

                supported_url, self.exit_status = check_url(
                    pbar, url, self.debug, self.exit_status)

                if supported_url:
                    try:
                        download_processing_log(self.debug, url)

                        fic = ArchiveOfOurOwn(
                            url, self.debug,  self.exit_status)
                        fic.get_fic_metadata(self.format_type)

                        # update the exit status
                        self.exit_status = fic.exit_status

                        if fic.ao3_works_name is None:
                            tqdm.write(
                                Fore.RED +
                                "Fanfiction not found")
                            self.exit_status = 1
                            exit(self.exit_status)

                        if fic.file_name is None:
                            self.exit_status = 1

                        else:
                            self.exit_status = save_data(
                                fic,
                                self.out_dir, fic.file_name,
                                fic.download_url, self.debug, self.force,
                                self.exit_status)

                        pbar.update(1)

                    # Error: 'ArchiveOfOurOwn' object has no attribute 'file_name'
                    # Reason: Unsupported URL
                    except AttributeError:
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    pass

    def get_urls_from_page(self, url: str):

        with console.status("[bold green]Processing..."):
            response = requests.get(url)

            if self.debug:
                logger.debug(f"GET: {response.status_code}: {response.url}")

            html_page = BeautifulSoup(response.content, 'html.parser')

            if re.search("https://archiveofourown.org/", url):
                ao3_series_works_html = []
                self.ao3_works_list = []
                self.ao3_series_list = []

                ao3_series_works_html_h4 = html_page.findAll(
                    'h4', attrs={'class': 'heading'})

                for i in ao3_series_works_html_h4:
                    ao3_series_works_html.append(i)

                ao3_series_works_html = ""
                for i in ao3_series_works_html_h4:
                    ao3_series_works_html += str(i)

                ao3_urls = BeautifulSoup(ao3_series_works_html, 'html.parser')

                for tag in ao3_urls.findAll('a', {'href': re.compile('/works/')}):
                    self.ao3_works_list.append(
                        "https://archiveofourown.org"+tag['href'])

                for tag in ao3_urls.findAll('a', {'href': re.compile('/series/')}):
                    self.ao3_series_list.append(
                        "https://archiveofourown.org"+tag['href'])

            else:
                self.ao3_works_list = None
                self.ao3_series_list = None
                tqdm.write(
                    Fore.RED + f"\nSkipping unsupported URL: {url}" + Style.RESET_ALL +
                    Fore.BLUE + "\nOnly archiveofourown.org is supported.")
