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
    q = data_dict.get('q', None)
    suggestions = _get_solr_suggestions(q)
    return suggestions


def _get_solr_suggestions(q) -> List[str]:
    u'''Makes a connection to SOLR suggester url and
    returns parsed result of the available suggestions
    based on the query term.

    :param q: the query term to search for suggestions
    :type q: str
    :returns: List of suggestions
    :rtype: list[str]
    '''

    solr_url, solr_user, solr_password = SolrSettings.get()
    suggest_solr_url = solr_url + u'{}'.format(u'/suggest')
    params = {
        u'suggest.q': q,
        u'wt': u'json'
    }

    try:
        response = requests.get(
            url=suggest_solr_url,
            params=params,
            auth=HTTPBasicAuth(solr_user,
                               solr_password),
            timeout=60)
    except requests.exceptions.Timeout as e:
        log.error(u'Connection to server '
                  u'{} timed out: {}'.format(suggest_solr_url, e))
    except requests.exceptions.ConnectionError as e:
        log.error(u'Failed to connect '
                  u'to server at {}: {}'.format(suggest_solr_url, e))
    except HTTPException as e:
        log.error(u'Unhandled error: '
                  u'{}: {}'.format(suggest_solr_url, e))

    result = _parse_solr_response(q, response.json())

    return result


def _parse_solr_response(q, solr_response) -> List[str]:
    u'''Helpr function that
    parses the SOLR response into a list of strings

    :param q: The query term
    :type q: str
    :returns: List of suggestions
    :rtype: list[str]
    '''
    suggest_root = solr_response['suggest']
    title_suggestions = [item['term'] for item in
                         suggest_root['datasetTitleSuggester'][q]['suggestions']]
    # Maybe the notes suggestions are not needed
    notes_suggestions = suggest_root['datasetNotesSuggester'][q]['suggestions']
    tags_suggestions = [item['term'] for item in
                        suggest_root['datasetTagsSuggester'][q]['suggestions']]
    return title_suggestions + tags_suggestions
