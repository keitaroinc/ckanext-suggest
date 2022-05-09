[![Tests](https://github.com/duskobogdanovski/ckanext-suggest/workflows/Tests/badge.svg?branch=main)](https://github.com/duskobogdanovski/ckanext-suggest/actions)

# ckanext-suggest

An extension that utilizes Solr Suggest component to provide auto-suggest feature in CKAN's main dataset search.


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible? |
| --------------- |-------------|
| 2.6 and earlier | not tested  |
| 2.7             | not tested  |
| 2.8             | not tested  |
| 2.9             | yes         |


## Installation

To install ckanext-suggest:

1. In order to enable SOLR suggest component you need to edit solrconfig.xml 
 in your application's SOLR core settings and add the following snippet in the components section:
```xml

 <!-- Suggester Component

       The SuggestComponent in Solr provides users 
       with automatic suggestions for query terms.
  -->
  <searchComponent name="suggest" class="solr.SuggestComponent">
    <lst name="suggester">
      <str name="name">datasetTitleSuggester</str>
      <str name="lookupImpl">AnalyzingInfixLookupFactory</str>
      <str name="dictionaryImpl">DocumentDictionaryFactory</str>
      <str name="field">title</str>
      <str name="minPrefixChars">2</str>
      <str name="suggestAnalyzerFieldType">text</str>
      <str name="buildOnStartup">false</str>
      <str name="highlight">false</str>
    </lst>
    <lst name="suggester">
      <str name="name">datasetNotesSuggester</str>
      <str name="lookupImpl">AnalyzingInfixLookupFactory</str>
      <str name="dictionaryImpl">DocumentDictionaryFactory</str>
      <str name="field">notes</str>
      <str name="minPrefixChars">2</str>
      <str name="suggestAnalyzerFieldType">text</str>
      <str name="buildOnStartup">false</str>
      <str name="highlight">false</str>
    </lst>
    <lst name="suggester">
      <str name="name">datasetTagsSuggester</str>
      <str name="lookupImpl">FuzzyLookupFactory</str>
      <str name="dictionaryImpl">DocumentDictionaryFactory</str>
      <str name="field">tags</str>
      <str name="suggestAnalyzerFieldType">text</str>
      <str name="buildOnStartup">false</str>
    </lst>
  </searchComponent>

  <!-- A request handler for demonstrating the suggest component.
  -->
  <requestHandler name="/suggest" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <str name="suggest">true</str>
      <str name="suggest.count">5</str>
      <str name="suggest.dictionary">datasetTitleSuggester</str>
      <str name="suggest.dictionary">datasetNotesSuggester</str>
      <str name="suggest.dictionary">datasetTagsSuggester</str>
    </lst>
    <arr name="components">
      <str>suggest</str>
    </arr>
  </requestHandler>


```

2. Restart SOLR:

```commandline
sudo service solr restart
```
4. Activate your CKAN virtual environment, for example:
 
```commandline
. /usr/lib/ckan/default/bin/activate
```

6. Clone the source and install it on the virtualenv
```commandline
git clone https://github.com/keitaroinc/ckanext-suggest.git
cd ckanext-suggest
pip install -e .
pip install -r requirements.txt
```
8. Add `suggest` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

9. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:
```commandline
sudo service apache2 reload
```
8. Build the lookup data structure in SOLR: TODO
```commandline
ckan -c /etc/ckan/default/ckan.ini suggest buid
```
9. Set up a CRON job that will update the lookup data structure on regular basis: TODO

## Config settings

None at the moment.

## Developer installation

To install ckanext-suggest for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/duskobogdanovski/ckanext-suggest.git
    cd ckanext-suggest
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-suggest

If ckanext-suggest should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
