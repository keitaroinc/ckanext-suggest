import click
from ckanext.suggest.logic.action.get import _get_solr_suggest


@click.group()
def suggest():
    pass


@suggest.command(u'build', short_help=u'' )
def build():
    _get_solr_suggest(do_suggest='false', build='true')
    click.secho(
        'Build lookup data structure in SOLR done.',
        fg=u'green',
        bold=True)


def get_commands():
    return [suggest]
