import requests
import json
import config


class ITop(object):

    def __init__(self, itop_login=config.itop_login,
                 itop_pass=config.itop_pass,
                 itop_fqdn=config.itop_fqdn):
        self.core_get = {
            'operation': 'core/get',
            'output_fields': 'name'
        }
        self.core_create = {
            'operation': 'core/create',
            'output_fields': 'name'
        }
        self.itop_login = itop_login
        self.itop_pass = itop_pass
        self.itop_fqdn = itop_fqdn
        self.itop_api_url = 'http://' + self.itop_fqdn + '/webservices/rest.php?version=1.0'
        self.itop_sync_url = 'http://' + self.itop_fqdn + '/synchro/synchro_exec.php?data_sources='

    def get_data(self, itop_class, filter_query=None, output_fields=None):
        self.core_get['class'] = itop_class
        if filter_query:
            self.core_get['key'] = 'SELECT ' + itop_class + ' ' + filter_query
        else:
            self.core_get['key'] = 'SELECT ' + itop_class

        if output_fields:
            self.core_get['output_fields'] = output_fields

        return self.generate_dict(self._post_data(self.core_get), self.core_get['output_fields'])

    def run_sync(self, table_id):
        sync = requests.get(self.itop_sync_url + table_id, auth=(self.itop_login, self.itop_pass))
        return sync.status_code

    def _post_data(self, json_request):
        payload = dict(json_data=json.dumps(json_request))
        result = requests.post(self.itop_api_url, auth=(self.itop_login, self.itop_pass), data=payload)
        return result

    @staticmethod
    def generate_dict(json_input, output_fields):
        result = []
        data = json.loads(json_input.text)['objects']
        if data is None:
            return False
        for obj in data.iterkeys():
            obj_id = {'id': data[obj]['key']}
            result.append(obj_id)
            for key, value in data[obj]['fields'].iteritems():
                if key in output_fields:
                    obj_id[key] = value

        return result
