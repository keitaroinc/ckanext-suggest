import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.suggest.logic.action.get import suggest
import ckanext.suggest.cli as cli


class SuggestPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IClick)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'suggest')

    # IActions

    def get_actions(self):
        return {
            u'suggest': suggest
        }

    # IClick

    def get_commands(self):
        return cli.get_commands()
