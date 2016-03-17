import config
import model.relations as relations
import ssl
from pysphere import VIServer, VIProperty
import requests
requests.packages.urllib3.disable_warnings()
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class Vmware:

    def __init__(self):
        self.host = config.vmware_host
        self.user = config.vmware_user
        self.pwd = config.vmware_pass
        self.connection = VIServer()
        self.connection.connect(self.host, self.user, self.pwd)
        self.props = VIProperty(self.connection, self.connection._do_service_content.CustomFieldsManager)
        self.custom_fields = dict((cf.key, cf.name) for cf in self.props.field)

    def get_servers(self):
        obj_type = 'HostSystem'
        return self._get_initial_data(relations.vmware_server, obj_type)

    def get_hypervisors(self):
        obj_type = 'HostSystem'
        return self._get_initial_data(relations.vmware_hypervisor, obj_type)

    def get_virtual_machines(self):
        obj_type = 'VirtualMachine'
        return self._get_initial_data(relations.vmware_virtual_machine, obj_type)

    def get_farm(self):
        obj_type = 'ClusterComputeResource'
        return self._get_initial_data(relations.vmware_farm, obj_type)

    def get_os_versions(self):
        hosts_os_versions = self._get_initial_data(relations.vmware_hosts_os_versions, 'HostSystem')
        vms_os_versions = self._get_initial_data(relations.vmware_vms_os_versions, 'VirtualMachine')
        os_versions = []
        hosts_os_versions.extend(vms_os_versions)
        for os_version in hosts_os_versions:
            if len(os_version.keys()) >= 2:
                if os_version not in os_versions:
                    os_versions.append(os_version)
        return os_versions

    def get_os_familys(self):
        hosts_os_familys = self.get_facts('summary.config.product.name', 'HostSystem')
        vms_os_familys = self.get_facts('guest.guestFamily', 'VirtualMachine')
        os_familys = []
        for os_family in hosts_os_familys | vms_os_familys:
            os_familys.append({'name': os_family})

        return os_familys

    def get_brands(self):
        facts_brand = self.get_facts('summary.hardware.vendor', 'HostSystem')
        brands = []
        for brand in facts_brand:
            brands.append({'name': brand})

        return brands

    def get_models(self):
        obj_type = 'HostSystem'
        return self._get_initial_data(relations.vmware_models, obj_type)

    def _get_initial_data(self, data_map, obj_type):
        properties = self.connection._retrieve_properties_traversal(property_names=data_map.values(), obj_type=obj_type)
        result = []
        for obj in properties:
            if not hasattr(obj, "PropSet"):
                continue
            host = {}
            result.append(host)
            for prop in obj.PropSet:
                for key, value in data_map.iteritems():
                    if prop.Name == value:
                        if prop.Name == "summary.hardware.otherIdentifyingInfo":
                            for license_info in prop.Val.HostSystemIdentificationInfo:
                                if 'Service tag of the system' in license_info.IdentifierType.Summary:
                                    host['serialnumber'] = license_info.IdentifierValue
                                elif 'Product ID:' in license_info.IdentifierValue:
                                    host['asset_number'] = license_info.IdentifierValue.split(": ")[1]
                        elif prop.Name == "customValue":
                            for annotation in prop.Val.CustomFieldValue:
                                try:
                                    host['description'] += str(self.custom_fields.get(annotation.Key)) + ": " + str(annotation.Value) + "\n"
                                except KeyError:
                                    host['description'] = str(self.custom_fields.get(annotation.Key)) + ": " + str(annotation.Value) + "\n"
                        elif prop.Name == "summary.hardware.memorySize":
                            host[key] = prop.Val / (1024 * 1024)
                        else:
                            try:
                                host[key] = prop.Val
                            except SyntaxError:
                                host[key] = None

        return result

    def get_relations(self, first_fact, second_fact, obj_type):
        result = {}
        data_map = {'first_fact': first_fact,
                    'second_fact': second_fact
                    }
        data = self._get_initial_data(data_map, obj_type)

        for item in data:
                try:
                    result[item['first_fact']] = item['second_fact']
                except KeyError:
                    continue

        return result

    def get_facts(self, fact_name, obj_type):
        data_map = {'fact_name': fact_name}
        data = self._get_initial_data(data_map, obj_type)
        result = set()

        for item in data:
                try:
                    result.add(item['fact_name'])
                except KeyError:
                    continue

        return result

    def __del__(self):
        self.connection.disconnect()
