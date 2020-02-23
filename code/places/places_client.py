import logging
import os
import requests
from requests.adapters import HTTPAdapter
from requests import Session
from urllib.parse import urljoin
from rest_framework import status

logger = logging.getLogger('Places')
DEFAULT_TIMEOUT = (4, 10)  # 4 second connect, 10 second read time
JSON_CONTENT_TYPE = 'application/json'


session = Session()
session.mount('https://', HTTPAdapter(max_retries=3,))


class PlacesClient():
    GOOGLE_PLACES_API = 'place'
    
    def __init__(self):
        self.token = os.environ['PLACES_TOKEN']
        self.base_url = self._get_base_url()
        self.logger = logging.getLogger('PlacesClient')

    def _log_request_debug(self, uri, data):
        self.logger.debug(f'debugging request to {uri}: {data}')

    def _log_request_info(self, uri):
        self.logger.info(f'made a request to {uri}')

    def _log_request_conflict(self, uri):
        self.logger.warning('request to %s resulted in a conflict', uri)

    def _log_request_error(self, uri):
        self.logger.error('request to %s resulted in error', uri)

    def _get_base_url(self):
        return f'https://maps.googleapis.com/maps/api/place'

    def _get_api_token(self):
        return self.token

    def _perform_request(
        self,
        request_function,
        relative_uri,
        data=None,
        timeout=DEFAULT_TIMEOUT,
        **params,
    ):
        try:
            uri = urljoin(
                self.base_url,
                os.path.join(
                    self.GOOGLE_PLACES_API,
                    relative_uri
                )
            )
            self.logger.info(uri)
            response = request_function(
                uri,
                timeout=timeout,
                json=data,
                params=params
            )
            response.raise_for_status()
            content_type = response.headers.get('Content-Type')
            is_json = content_type and JSON_CONTENT_TYPE in content_type
            has_content = (
                response.status_code != status.HTTP_204_NO_CONTENT
                and response.text
            )
            body = (
                response.json()
                if has_content and is_json
                else response.text or {}
            )
            self._log_request_info(uri)
            return response, body

        except requests.exceptions.RequestException as ex:
            if (
                ex.response is not None
                and ex.response.status_code == status.HTTP_409_CONFLICT
            ):
                self._log_request_conflict(uri)
            raise ex

        except Exception:
            self._log_request_error(uri)
            raise

    def get(self, relative_uri, timeout=DEFAULT_TIMEOUT, **params):
        return self._perform_request(
            session.get,
            relative_uri,
            timeout=timeout,
            **params
        )
