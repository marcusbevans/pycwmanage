import json
import logging
from base64 import b64encode
from dataclasses import dataclass, field

import requests

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CWManage:
    connectwise_site: str
    company_id: str
    public_key: str = field(repr=False)
    private_key: str = field(repr=False)
    client_id: str = field(repr=False)
    _url: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, '_url', self._get_url)

    def _authorization(self) -> dict:
        auths = b64encode(f"{self.company_id}+{self.public_key}:{self.private_key}".encode("utf8")).decode("utf8")
        return {
            'Authorization': f'Basic {auths}',
            'clientId': self.client_id
        }

    @property
    def _get_url(self) -> str:
        calling_company_info_url = f'https://{self.connectwise_site}/login/companyinfo/{self.company_id}'
        response = requests.get(calling_company_info_url)

        if response.status_code == 200:
            code_base = response.json()['Codebase']
            api_url = f'https://{response.json()["SiteUrl"]}/{code_base}apis/3.0'
            return api_url

    def get(self, endpoint: str, verbose: bool = False, log_endpoint: bool = False, return_response: bool = False):
        url = join_url(self._url, endpoint)
        try:
            response = requests.get(url, headers=self._authorization())
        except requests.exceptions.ConnectionError as e:
            logging.error(f'Connection Error - {e}')
            return None if return_response else []

        if verbose:
            verbose_logging(response)
        if log_endpoint:
            logging.info(url)

        if return_response:
            return response

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logging.error(f'404 - Endpoint Not Found - {url}')
        return []

    def get_all_pages(self, endpoint: str, page: int = 0, verbose: bool = False, log_endpoint: bool = False, return_response: bool = False):
        if "?" in endpoint:
            url = join_url(self._url, endpoint + f'&pagesize=50&page={page}')
        else:
            url = join_url(self._url, endpoint + f'?pagesize=50&page={page}')
        response = requests.get(url, headers=self._authorization())

        if verbose:
            verbose_logging(response)
        if log_endpoint:
            logging.info(url)

        if return_response:
            # For return_response mode, return list of response objects
            responses = [response]
            if response.status_code == 200 and 'Link' in response.headers:
                if 'rel="next"' in response.headers['Link']:
                    next_responses = self.get_all_pages(endpoint, page + 1, verbose=verbose, log_endpoint=log_endpoint, return_response=True)
                    if next_responses:
                        responses.extend(next_responses)
            return responses

        if response.status_code == 200:
            data = response.json()
            if 'Link' in response.headers:
                if 'rel="next"' in response.headers['Link']:
                    data = data + self.get_all_pages(endpoint, page + 1, verbose=verbose, log_endpoint=log_endpoint)
        else:
            data = []

        return data

    def get_all_pages_mt(self, endpoint: str, verbose: bool = False, log_endpoint: bool = False, return_response: bool = False):
        """
        gets all pages of a given endpoint using multi-threading
        """
        import re
        from concurrent.futures import ThreadPoolExecutor
        from functools import partial

        def get_page(page: int, authorization: dict, page_url: str, log_url: bool = False, return_resp: bool = False):
            get_page_url = f'{page_url}&page={page}'
            get_page_response = requests.get(get_page_url, headers=authorization)

            if log_url:
                logging.info(get_page_url)

            return get_page_response if return_resp else get_page_response.json()

        # get last page information
        url = join_url(self._url, endpoint)
        response = requests.get(url, headers=self._authorization())
        last = response.links.get('last')
        if last is None:
            logging.debug(f'No last page on {endpoint} to pull')
            return [] if not return_response else [response]
        last_url = last.get('url')
        last_page = re.search(r'page=(\d+)', last_url).group(1)
        page_url = re.search(r'(.+)&page=', last_url).group(1)
        pages = range(1, int(last_page) + 1)

        results = []
        with ThreadPoolExecutor() as executor:
            results.append(executor.map(
                partial(get_page,
                        authorization=self._authorization(), page_url=page_url,
                        log_url=log_endpoint, return_resp=return_response), pages)
            )

        if return_response:
            # Return list of response objects
            responses = [response]  # Include the initial response
            for result in results[0]:
                if log_endpoint:
                    logging.info(f'Response: {result.status_code}')
                responses.append(result)
            return responses

        data = []
        for i, result in enumerate(results[0]):
            if log_endpoint:
                logging.info(f'Page {i + 1}')
            data.extend(result)

        return data

    def post(self, endpoint: str, data: dict, verbose: bool = False, log_endpoint: bool = False, return_response: bool = False):
        url = join_url(self._url, endpoint)
        response = requests.post(url, headers=self._authorization(), json=data)

        if verbose:
            verbose_logging(response)
        if log_endpoint:
            logging.info(url)

        if return_response:
            return response

        if response.status_code in [200, 201]:
            return response.json()
        return []

    def put(self, endpoint: str, data: dict, verbose: bool = False, log_endpoint: bool = False, return_response: bool = False):
        url = join_url(self._url, endpoint)
        response = requests.put(url, headers=self._authorization(), json=data)

        if verbose:
            verbose_logging(response)
        if log_endpoint:
            logging.info(url)

        if return_response:
            return response

        if response.status_code in [200, 201]:
            return response.json()
        return []

    def patch(self, endpoint: str, data: list, verbose: bool = False, log_endpoint: bool = False, return_response: bool = False):
        url = join_url(self._url, endpoint)
        response = requests.patch(url, headers=self._authorization(), json=data)

        if verbose:
            verbose_logging(response)
        if log_endpoint:
            logging.info(url)

        if return_response:
            return response

        if response.status_code in [200, 201]:
            return response.json()
        return []

    def delete(self, endpoint: str, verbose: bool = False, log_endpoint: bool = False, return_response: bool = False):
        url = join_url(self._url, endpoint)
        response = requests.delete(url, headers=self._authorization())

        if verbose:
            verbose_logging(response)
        if log_endpoint:
            logging.info(url)

        if return_response:
            return response

        if response.status_code == 204:
            return True
        return False


def join_url(base_url: str, *args: str):
    for arg in args:
        if arg[:1] != '/':
            base_url = base_url + '/' + arg
        else:
            base_url = base_url + arg

    return base_url


def verbose_logging(response: requests.Response):
    logging.info(f'{response.request.method}: {response.request.url} {response.status_code}')
    logging.info(response.headers)
    try:
        logging.info(response.json())
    except json.JSONDecodeError:
        pass
    logging.info(response.request.body)
