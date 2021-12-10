import logging
from typing import (
    Dict,
    Any,
    List, Optional,
)

logger = logging.getLogger(__name__)


class ParserBase:
    """
    Parser base for the different responses from the commands.
    """

    def __init__(self, response: Dict[str, Any], keys: Optional[List[str]]):
        """
        :param response: response of the request
        :param keys: strings defining the data points that we want to track within the reponses.
        """
        self.response = response
        self.keys = keys
        self.errors = {}

    def is_response_valid(self) -> bool:
        """
        Function validates the reponse payload based on the 'result' data in the payload.
        :return: boolean
        """
        flag = True
        error_message = 'Error : wrong response from the Whale Alert API'
        if 'result' not in self.response:
            logger.error(error_message + f': {self.response}')
            self.errors['result'] = error_message
            flag = False

        elif self.response['result'] != 'success':
            logger.error(f'Request unsuccessful : {self.response}')
            self.errors['result'] = error_message + self.response['result']
            flag = False

        return flag

    @staticmethod
    def format_dict_to_text(dictionary: Dict[str, Any]) -> str:
        """
        :param dictionary: dictionary to format
        :return: String displayed in a pretty way in a telegram channel.
        """
        result_text = ''
        for key, value in dictionary.items():
            result_text += f'{key}: {value}\n'

        return result_text

    def clean_response(self, result_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cleans the response from the unrequested data.
        :return: Cleaned response, without the useless data
        """
        if not self.keys:
            return result_dict

        result = {}
        error_message = 'Data is missing in the payload'

        for key in self.keys:
            data = result_dict.get(key)

            if not data:
                logger.error(error_message + f': {key}')
                self.errors[key] = error_message
                continue
            result[key] = data

        return result

    def parse_response(self) -> Optional[str]:
        """
        Function user to parse the response into a readable text in telegram.
        Take the response and performs validation on it, then cleaning and finally formatting.
        :return: Formatted text
        """
        if not self.is_response_valid():
            return
        text_items = ''
        if self.items_key in self.response:
            for item in self.response.pop(self.items_key):
                cleaned_item = self.clean_response(item)
                # We 'stringify' the blockchains part of the payload
                stringified_item = self.format_dict_to_text(cleaned_item)
                text_items += stringified_item

            self.response[self.items_key] = text_items
        # We 'stringify' the whole payload
        text = self.format_dict_to_text(self.response)
        return text


class CheckStatusParser(ParserBase):
    """
    Parser for the check_status command of the bot.
    """
    items_key = 'blockchains'


class TransactionsDetailParser(ParserBase):
    """
    Parser for the watcher_timer command of the bot.
    """
    items_key = 'transactions'
