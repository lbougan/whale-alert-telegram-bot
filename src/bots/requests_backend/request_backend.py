from typing import (
    Dict,
    Optional,
    Any,
)

import requests
import logging

from .utils import build_url


class WhaleAlertRequestBackendMixin:
    """
    Base Backend class to perform requests_backend to whale-alert api.
    """
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = {
            'api_key': api_key,
        }

    def build_full_url(self, additional_params: Optional[Dict[str, str]] = None):
        """
        Function to build the url on which we want to perform the requests_backend
        :param additional_params: Additional query parameters to add to the url
        :return: full url
        """
        if additional_params is None:
            additional_params = {}

        # The authentication for Whale Alert can be passed as a query parameter, 'api_token'
        query_params = self.api_key | additional_params

        return build_url(
            self.endpoint,
            query_params,
        )

    @staticmethod
    def request(
            url: str,
            method: str = 'get',
            payload: Optional[Dict[Any, Any]] = None,
            headers: Optional[Dict[Any, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Static method performing the actual requests_backend to Whale Alert.
        Catching the exceptions in case of connection error with the server, or wrong response.
        :param method: Method of the requests_backend. Default to get, since its the only method supported for now.
        :param url: full url including query params
        :param payload: optional payload
        :param headers: optional headers
        :return: Parsed response
        """
        result = {}
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                data=payload,
            )
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            result['error'] = 'No response from server'
            logging.error(e)
            return result

        try:
            result = response.json()
        except ValueError as e:
            result['error'] = 'Response from server cannot be serialized into JSON'
            logging.debug(
                'Error decoding response from Whale alert, not a JSON: %s', e
            )
        return result


class TransactionsDataRequestBackend(WhaleAlertRequestBackendMixin):
    """
    Backend class to retrieve transactions from Whale Alert API.
    """
    def fetch_transactions(
            self,
            start: str,
            end: Optional[str] = None,
            min_value: Optional[int] = None,
            limit: Optional[int] = None,
            currency: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Function fetching the transaction data between Unix timestamps on the different blockchains.
        :param start: Start date of the transaction data, as a Unix timestamp
        :param end: Optional : End date of the transaction data, as a Unix timestamp
        :param min_value: Minimum value of the transactions to fetch, in USD. Defaults to 500k USD
        :param limit: limit amount of transactions to fetch. Defaults to 100
        :param currency: currency code for which we want the transactions. ex: 'EUR', 'CHF', ...
        :return: List of transactions from Whale Alert.
        """
        query_params = {
            'start': start,
            'limit': limit,
            'min_value': min_value,
        }
        if end:
            query_params['end'] = end
        if currency:
            query_params['currency'] = currency

        full_url = self.build_full_url(query_params)
        response = self.request(full_url)

        return response


class TransactionDetailRequestBackend(WhaleAlertRequestBackendMixin):
    """
    Backend class to retrieve the data for a specific transaction from Whale Alert
    """
    def fetch_transaction_details(self, tx_hash: str, tx_blockchain: str) -> Dict[str, Any]:
        """
        :param tx_hash: Hash of the transaction to retrieve the data
        :param tx_blockchain: blockchain of the transaction
        :return:
        """
        self.endpoint = f'{self.endpoint}/{tx_blockchain}/{tx_hash}'
        full_url = self.build_full_url()
        response = self.request(full_url)

        return response


class ConnexionStatusBackend(WhaleAlertRequestBackendMixin):
    """
    Backend class to check the data for a specific transaction from Whale Alert
    """
    def check_status(self) -> Dict[str, Any]:
        full_url = self.build_full_url()
        response = self.request(full_url)

        return response
