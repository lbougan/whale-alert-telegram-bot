from typing import Dict, Union
from six.moves.urllib import parse as urlparse


def build_url(base_url: str, query_params: Dict[str, Union[str, int]]) -> str:
    """
    Adds additional query parameters to the base_url
    e.g. build_url('https://example.ch', {'q': 'demo'}) -> https://example.ch?q=demo.
    It will also consider existing GET arguments.
    :param base_url: url string
    :param query_params: dict with additional arguments to be appended to the base_url
    :return: url string
    """
    assert isinstance(query_params, dict), "Dictionary is expected in `query_params` {}".format(
        query_params
    )
    url_parts = list(urlparse.urlparse(base_url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(query_params)

    url_parts[4] = urlparse.urlencode(query)

    return urlparse.urlunparse(url_parts)
