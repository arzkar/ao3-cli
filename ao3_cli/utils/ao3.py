# Copyright 2021 Arbaaz Laskar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import re
import time
from loguru import logger
from bs4 import BeautifulSoup


params = {
    'view_adult': 'true'
}


class ArchiveOfOurOwn:
    def __init__(self, BaseUrl: str, debug: bool, exit_status: int):
        self.BaseUrl = BaseUrl
        self.debug = debug
        self.exit_status = exit_status
        self.session = requests.Session()

    def get_fic_metadata(self, format_type: int):

        time.sleep(1)
        response = self.session.get(self.BaseUrl, params=params)
        if self.debug:
            logger.debug(f"GET: {response.status_code}: {response.url}")

        ao3_soup = BeautifulSoup(response.content, 'html.parser')

        try:
            self.ao3_works_name = (ao3_soup.find(
                'h2', attrs={'class': 'title heading'}).contents[0]).strip()

        except AttributeError:
            if self.debug:
                logger.error(
                    "ao3_works_name is missing. Fanfiction not found")
            self.ao3_works_name = None
            return

        self.ao3_author_name_list = ao3_soup.find(
            'h3', attrs={'class': 'byline heading'}).find_all('a')

        self.ao3_author_name = []
        for author in self.ao3_author_name_list:
            self.ao3_author_name.append(author.string.strip())
        self.ao3_author_name = " and ".join(self.ao3_author_name)

        # fetch download urls
        try:
            self.ao3_works_download = ao3_soup.find(
                'ul', attrs={'class': 'expandable secondary'}).findAll('a')

        except AttributeError:
            self.log.info(
                "ao3_works_download is missing. Fanfiction not available for download.")
            self.ao3_works_download = None
            return

        for url in self.ao3_works_download:

            if format_type == 0:
                if re.search("epub", url['href'], re.I):
                    self.download_url = f"https://archiveofourown.org{url['href']}"
                self.file_format = "epub"

            elif format_type == 1:
                if re.search("mobi", url['href'], re.I):
                    self.download_url = f"https://archiveofourown.org{url['href']}"
                self.file_format = "mobi"

            elif format_type == 2:
                if re.search("pdf", url['href'], re.I):
                    self.download_url = f"https://archiveofourown.org{url['href']}"
                self.file_format = "pdf"

            elif format_type == 3:
                if re.search("html", url['href'], re.I):
                    self.download_url = f"https://archiveofourown.org{url['href']}"
                self.file_format = "html"

            elif format_type == 4:
                if re.search("azw3", url['href'], re.I):
                    self.download_url = f"https://archiveofourown.org{url['href']}"
                self.file_format = "azw3"

        self.file_name = f"{self.ao3_works_name} by {self.ao3_author_name}.{self.file_format}"

    def get_fic_data(self, download_url: str):

        self.response_data = self.session.get(
            download_url, allow_redirects=True
        )

        if self.debug:
            logger.debug(
                f"GET: {self.response_data.status_code}: {self.response_data.url}")
