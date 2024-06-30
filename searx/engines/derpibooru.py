# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""
 Derpibooru (Images)
"""
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
from json import loads

from searx import logger

# about
about = {
    "website": 'https://derpibooru.org/',
    "wikidata_id": 'Q28233552',
    "official_api_documentation": 'https://derpibooru.org/pages/api/',
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

base_url = 'https://derpibooru.org/'
search_url = base_url + 'api/v1/json/search/images?'
categories = ['images']
page_size = 20
paging = True
filter_id = 214606
sort_field = "wilson_score"
sort_direction = "desc"


def clean_url(url):
    parsed = urlparse(url)
    query = [(k, v) for (k, v) in parse_qsl(parsed.query) if k not in ['ixid', 's']]

    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, urlencode(query), parsed.fragment))


def request(query, params):
    params['url'] = search_url + urlencode(
        {'q': query, 'filter_id': filter_id, 'page': params['pageno'], 'per_page': page_size, 'sf': sort_field,
         'sd': sort_direction}
    )
    logger.debug("query_url --> %s", params['url'])
    return params


def response(resp):
    results = []
    json_data = loads(resp.text)

    if 'images' in json_data:
        for result in json_data['images']:
            results.append(
                {
                    'template': 'images.html',
                    'url': base_url + 'images/' + str(result.get('id')),
                    'thumbnail_src': clean_url(result['representations']['thumb']),
                    'img_src': clean_url(result['representations']['full']),
                    'title': result.get('name') or 'unknown',
                    'content': result.get('description') or '',
                }
            )

    return results
