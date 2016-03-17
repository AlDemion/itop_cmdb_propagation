import json
import requests
from requests.auth import HTTPBasicAuth
import model.relations as relations
import config


class Foreman:

    def __init__(self, login=config.foreman_login, pwd=config.foreman_pwd, url=config.foreman_url):
        self.foreman_login = login
        self.foreman_password = pwd
        self.foreman_url = url
        self.foreman_api_url = self.foreman_url + '/api/v2/fact_values?per_page=1000000'
        self.hosts_data = requests.get(self.foreman_api_url,
                                       auth=HTTPBasicAuth(self.foreman_login, self.foreman_password),
                                       verify=False).json()['results']

    def get_servers(self):
        return self._get_initial_data(relations.foreman_server)

    def get_models(self):
        return self._get_initial_data(relations.foreman_models)

    def get_virtual_machines(self):
        return self._get_initial_data(relations.foreman_virtual_machine, 'true')

    def get_os_versions(self):
        hosts_os_versions = self._get_initial_data(relations.foreman_os_versions)
        vms_os_versions = self._get_initial_data(relations.foreman_os_versions)
        os_versions = []
        hosts_os_versions.extend(vms_os_versions)
        for os_version in hosts_os_versions:
            if len(os_version.keys()) >= 2:
                if os_version not in os_versions:
                    os_versions.append(os_version)
        return os_versions

    def get_os_familys(self):
        facts_os_familys = self.get_facts('osfamily')
        os_familys = []
        for os_family in facts_os_familys:
            os_familys.append({'name': os_family})

        return os_familys

    def get_brands(self):
        facts_brand = self.get_facts('manufacturer')
        brands = []
        for brand in facts_brand:
            brands.append({'name': brand})

        return brands

    def _get_initial_data(self, data_map, is_virtual='false'):
        result = []
        for host, facts in self.hosts_data.iteritems():
            host = {'name': host}
            if facts['is_virtual'] == is_virtual:
                result.append(host)
                for key, value in data_map.iteritems():
                    try:
                        host[key] = facts[value]
                    except KeyError:
                        host[key] = None

        return result

    def get_relations(self, first_fact, second_fact):
        result = {}
        for facts in self.hosts_data.itervalues():
                try:
                    result[facts[first_fact]] = facts[second_fact]
                except KeyError:
                    continue

        return result

    def get_facts(self, fact_name):
        search_url = self.foreman_api_url + '&search=' + fact_name
        json_input = requests.get(search_url, auth=(self.foreman_login, self.foreman_password), verify=False)

        return self.generate_set(json_input, fact_name)

    @staticmethod
    def generate_set(json_input, fact_name):
        result = set()
        data = json.loads(json_input.text)['results']
        for key in data.iterkeys():
            for item, value in data[key].iteritems():
                if item == fact_name:
                    result.add(value)

        return result
