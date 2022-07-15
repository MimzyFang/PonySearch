# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""
 Derpibooru (Images)
"""
from urllib.parse import urlencode
from json import loads

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
filter_id = 100073


def request(query, params):
    params['url'] = search_url + urlencode(
        {'q': query, 'filter_id': filter_id, 'page': params['pageno'], 'per_page': page_size}
    )
    logger.debug("query_url --> %s", params['url'])
    return params


def response(resp):
    results = []
    json_data = loads(resp.text)

    if 'results' in json_data:
        for result in json_data['images']:
            results.append(
                {
                    'template': 'images.html',
                    'url': 'https://derpibooru.org/images/' + result.get('id'),
                    'thumbnail_src': result.get(result['representations']['thumb']),
                    'img_src': result.get(result['representations']['full']),
                    'title': result.get('name') or 'unknown',
                    'content': result.get('description') or '',
                }
            )
    logger.debug(results)
    return results
