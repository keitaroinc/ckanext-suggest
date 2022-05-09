import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.suggest.logic.action.get import suggest


class SuggestPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)

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
