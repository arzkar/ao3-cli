from typing import Tuple
import re
import os

from colorama import Fore, Style
from tqdm import tqdm
from loguru import logger

from .logging import downloaded_log


def get_format_type(_format: str = "epub") -> int:
    if re.search(r"\bepub\b", _format, re.I):
        format_type = 0

    elif re.search(r"\bmobi\b", _format, re.I):
        format_type = 1

    elif re.search(r"\bpdf\b", _format, re.I):
        format_type = 2

    elif re.search(r"\bhtml\b", _format, re.I):
        format_type = 3

    elif re.search(r"\azw3\b", _format, re.I):
        format_type = 4

    else:  # default epub format
        format_type = 0

    return format_type


def check_url(pbar, url: str, debug: bool = False,
              exit_status: int = 0) -> Tuple[bool, int]:

    if re.search(r"archiveofourown.org", url):
        supported_flag = True

    else:
        supported_flag = False

    if not supported_flag:
        pbar.update(1)
        exit_status = 1

        if debug:
            logger.error(
                f"Skipping unsupported URL: {url}\nOnly archiveofourown.org is supported.")
        else:
            tqdm.write(
                Fore.RED + f"Skipping unsupported URL: {url}" +
                Style.RESET_ALL + "\nOnly archiveofourown.org is supported.")

    return supported_flag, exit_status


def save_data(fic, out_dir: str, file_name:  str, download_url: str,
              debug: bool, force: bool, exit_status: int) -> int:

    ebook_file = out_dir+file_name

    if os.path.exists(out_dir+file_name) and force is False:

        exit_status = 1
        if debug:
            logger.error(
                f"{out_dir+file_name} already exists. Skipping download. Use --force flag to overwrite.")

        else:
            tqdm.write(
                Fore.RED +
                f"{out_dir+file_name} already exists. Skipping download. Use --force flag to overwrite.")

    else:
        if force and debug:
            logger.warning(
                f"--force flag was passed. Overwriting {out_dir+file_name}")

        fic.get_fic_data(download_url)

        downloaded_log(debug, file_name)

        with open(ebook_file, "wb") as f:
            f.write(fic.response_data.content)

        exit_status = 0

    return exit_status


def show_urls_from_page(fic):
    exit_status = 0
    found_flag = False
    if fic.ao3_works_list:
        found_flag = True
        tqdm.write(Fore.GREEN +
                   f"\nFound {len(fic.ao3_works_list)} works urls.")
        ao3_works_list = '\n'.join(fic.ao3_works_list)
        tqdm.write(ao3_works_list)

    if fic.ao3_series_list:
        found_flag = True
        tqdm.write(Fore.GREEN +
                   f"\nFound {len(fic.ao3_series_list)} series urls.")
        ao3_series_list = '\n'.join(fic.ao3_series_list)
        tqdm.write(ao3_series_list)

    if found_flag is False:
        tqdm.write(Fore.RED + "\nFound 0 urls.")
        exit_status = 1

    return exit_status
