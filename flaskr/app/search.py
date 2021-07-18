"""Module for interacting with elasticsearch through flask"""


from retrying import retry
from flask import current_app
from elasticsearch.exceptions import ConnectionError


def retry_if_connection_error(exception):
    """Return True if we should retry (in this case when it's an IOError), False otherwise"""
    return isinstance(exception, ConnectionError)


# Retry to allow elasticsearch container start
@retry(retry_on_exception=retry_if_connection_error, stop_max_attempt_number=20, wait_fixed=2000)
def add_to_index(index, model):
    """Add model to elasticsearch index"""
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """Remove model form elasticsearch index"""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """Find items in elasticsearch index"""
    if not current_app.elasticsearch:
        return [], 0

    query['from'] = (page - 1) * per_page
    query['size'] = per_page

    search = current_app.elasticsearch.search(
        index=index,
        body=query
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
