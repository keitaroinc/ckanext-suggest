import logging
import requests
from typing import List
from requests.auth import HTTPBasicAuth
from http.client import HTTPException

from ckan.logic import side_effect_free
from ckan.lib.search import SolrSettings


log = logging.getLogger(__name__)


@side_effect_free
def suggest(context, data_dict):
    u'''Returns SOLR suggestions based on an input query (text)
    '''

    do_suggest = data_dict.get('suggest')
    build = data_dict.get('build')
    query = data_dict.get('q')

    suggestions = _get_solr_suggest(do_suggest, build, query)
    return suggestions


def _get_solr_suggest(do_suggest='true', build='false', query=None) -> List[str]:
    u'''Makes a connection to SOLR suggester url and
    returns parsed result of the available suggestions
    based on the query term and can also be used to build
    the lookup data structure.

    :param do_suggest: parameter that tells solr
    whether to make suggestions or not (true or false)
    :type do_suggest: str
    :param build: parameter that tells solr
    whether to build the lookup data structure or not (true or false)
    :type build: str
    :param query: the query term to search for suggestions
    :type query: str
    :returns: List of suggestions
    :rtype: list[str]
    '''

    solr_url, solr_user, solr_password = SolrSettings.get()
    suggest_solr_url = solr_url + u'{}'.format(u'/suggest')
    params = {
        u'suggest': do_suggest,
        u'suggest.build': build,
        u'suggest.q': query,
        u'wt': u'json'
    }

    try:
        response = requests.get(
            url=suggest_solr_url,
            params=params,
            auth=HTTPBasicAuth(solr_user,
                               solr_password),
            timeout=60,
            verify=True)
    except requests.exceptions.Timeout as e:
        log.error(u'Connection to server '
                  u'{} timed out: {}'.format(suggest_solr_url, e))
    except requests.exceptions.ConnectionError as e:
        log.error(u'Failed to connect '
                  u'to server at {}: {}'.format(suggest_solr_url, e))
    except HTTPException as e:
        log.error(u'Unhandled error: '
                  u'{}: {}'.format(suggest_solr_url, e))

    result = _parse_solr_response(query, response.json())

    return result


def _parse_solr_response(q, solr_response) -> List[str]:
    u'''Helpr function that
    parses the SOLR response into a list of strings

    :param q: The query term
    :type q: str
    :returns: List of suggestions
    :rtype: list[str]
    '''
    res = []
    suggest_root = solr_response.get('suggest', None)

    if suggest_root:
        title_suggestions = [item['term'] for item in
                             suggest_root['datasetTitleSuggester'][q]['suggestions']]
        # Maybe the notes suggestions are not needed
        notes_suggestions = suggest_root['datasetNotesSuggester'][q]['suggestions']
        tags_suggestions = [item['term'] for item in
                            suggest_root['datasetTagsSuggester'][q]['suggestions']]

        res = tags_suggestions + title_suggestions

    return res
