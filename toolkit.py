import model.typology as typology
import model.content_item as ci
import model.relations as relations
import config
from datasources.active_directory import ActiveDirectory
from datasources.itop import ITop
from datasources.vmware import Vmware
from datasources.foreman import Foreman
from datasources.database import Database
from controller.generator import generate_attributes
from controller.generator import merge_dicts
from controller.generator import merge_vms
from controller.generator import generate_sql
from controller.generator import generate_dict

ad = ActiveDirectory()
vw = Vmware()
fm = Foreman()
itop = ITop()
db = Database()


org_id = itop.get_data('Organization')[0]['id']
location_id = itop.get_data('Location')[0]['id']
ad_users = ad.get_users()
farms = vw.get_farm()
brands = merge_dicts(vw.get_brands(), fm.get_brands())
os_familys = merge_dicts(vw.get_os_familys(), fm.get_os_familys())
os_versions = merge_dicts(vw.get_os_versions(), fm.get_os_versions())
models = merge_dicts(vw.get_models(), fm.get_models())
servers = merge_dicts(vw.get_servers(), fm.get_servers())
hypervisors = vw.get_hypervisors()
vmware_vms = vw.get_virtual_machines()
foreman_vms = fm.get_virtual_machines()
vms = merge_vms(vmware_vms, foreman_vms)

# Ready now
person_sql_set = set()
for item in generate_attributes(ad_users, relations.person, ci.Person):
    item.org_id = org_id
    item.location_id = location_id
    person_sql_set.add(generate_sql(config.persons_table, item.email, generate_dict(item, relations.itop_person)))

for query in person_sql_set:
    db.execute(query)

itop.run_sync(config.persons_table_id)


# Get synced iTop contacts id's for Ldap Users and External users
itop_contacts = itop.get_data('Contact', output_fields='email')

# Ready now
user_external_sql_set = set()
for item in generate_attributes(ad_users, relations.user, ci.UserExternal):
    for contact in itop_contacts:
        if item.email in contact['email']:
            item.contactid = contact['id']
            break

    user_external_sql_set.add(generate_sql(config.userexternal_table, item.email, generate_dict(item, relations.itop_user)))

for query in user_external_sql_set:
    db.execute(query)

itop.run_sync(config.userexternal_table_id)

# Ready now
user_ldap_sql_set = set()
for item in generate_attributes(ad_users, relations.user, ci.UserLDAP):
    for contact in itop_contacts:
        if item.email in contact['email']:
            item.contactid = contact['id']
            break

    user_ldap_sql_set.add(generate_sql(config.userldap_table, item.email, generate_dict(item, relations.itop_user)))

for query in user_ldap_sql_set:
    db.execute(query)

itop.run_sync(config.userldap_table_id)


# Ready now
farms_sql_set = set()
for item in generate_attributes(farms, relations.vmware_farm, ci.Farm):
    item.org_id = org_id
    farms_sql_set.add(generate_sql(config.farm_table, item.name, generate_dict(item, relations.itop_farm)))

for query in farms_sql_set:
    db.execute(query)

itop.run_sync(config.farm_table_id)


# Ready now
brands_sql_set = set()
for item in generate_attributes(brands, relations.brands, typology.Brand):
    brands_sql_set.add(generate_sql(config.brand_table, item.name, generate_dict(item, relations.itop_brand)))

for query in brands_sql_set:
    db.execute(query)

itop.run_sync(config.brand_table_id)


# Ready now
osfamily_sql_set = set()
for item in generate_attributes(os_familys, relations.os_familys, typology.OSFamily):
    osfamily_sql_set.add(generate_sql(config.osfamily_table, item.name, generate_dict(item, relations.itop_osfamily)))

for query in osfamily_sql_set:
    db.execute(query)

itop.run_sync(config.osfamily_table_id)

# Get synced iTop os_familys id's for OS Versions
itop_os_family = itop.get_data('OSFamily', output_fields='name')

# Ready now
os_versions_sql_set = set()
for item in generate_attributes(os_versions, relations.os_versions, typology.OSVersion):
    for os_family in itop_os_family:
        if item.osfamily in os_family['name']:
            item.osfamily_id = os_family['id']
            break
    os_versions_sql_set.add(generate_sql(config.osversion_table, item.name, generate_dict(item, relations.itop_osversion)))

for query in os_versions_sql_set:
    db.execute(query)

itop.run_sync(config.osversion_table_id)

# Get synced iTop brands id's for Models
itop_brand = itop.get_data('Brand', output_fields='name')

brands_sql_set = set()
for item in generate_attributes(models, relations.models, typology.Model):
    for brand in itop_brand:
        if item.brand in brand['name']:
            item.brand_id = brand['id']
            break
    brands_sql_set.add(generate_sql(config.model_table, item.name, generate_dict(item, relations.itop_model)))

for query in brands_sql_set:
    db.execute(query)

itop.run_sync(config.model_table_id)


itop_model = itop.get_data('Model', output_fields='name')
itop_osversions = itop.get_data('OSVersion', output_fields='name')


servers_sql_set = set()
for item in generate_attributes(servers, relations.servers, ci.Server):
    item.org_id = org_id
    item.location_id = location_id

    for brand in itop_brand:
        if item.brand in brand['name']:
            item.brand_id = brand['id']
            break

    for model in itop_model:
        if item.model in model['name']:
            item.model_id = model['id']
            break

    for os_family in itop_os_family:
        if item.osfamily in os_family['name']:
            item.osfamily_id = os_family['id']
            break

    for osversion in itop_osversions:
        if item.osversion in osversion['name']:
            item.osversion_id = osversion['id']
            break

    servers_sql_set.add(generate_sql(config.server_table, item.name, generate_dict(item, relations.itop_server)))

for query in servers_sql_set:
    db.execute(query)

itop.run_sync(config.server_table_id)

itop_server = itop.get_data('Server', output_fields='name')
itop_farm = itop.get_data('Farm', output_fields='name')

hypervisors_sql_set = set()
for item in generate_attributes(hypervisors, relations.hypervisor, ci.Hypervisor):
    item.org_id = org_id

    for farm in itop_farm:
        if item.farm in farm['name']:
            item.farm_id = farm['id']
            break

    for server in itop_server:
        if item.name in server['name']:
            item.server_id = server['id']
            break

    hypervisors_sql_set.add(generate_sql(config.hypervisor_table, item.name, generate_dict(item, relations.itop_hypervisor)))

for query in hypervisors_sql_set:
    db.execute(query)

itop.run_sync(config.hypervisor_table_id)

itop_hypervisor = itop.get_data('Hypervisor', output_fields='name')

virtualhost_sql_set = set()
for item in generate_attributes(vms, relations.vms, ci.VirtualMachine):
    item.org_id = org_id
    for hv in hypervisors:
        if item.virtualhost == hv['server']:
            item.virtualhost = hv['name']
            break

    for hypervisor in itop_hypervisor:
        if item.virtualhost in hypervisor['name']:
            item.virtualhost_id = hypervisor['id']
            break

    for os_family in itop_os_family:
        if item.osfamily in os_family['name']:
            item.osfamily_id = os_family['id']
            break

    for osversion in itop_osversions:
        if item.osversion in osversion['name']:
            item.osversion_id = osversion['id']
            break

    virtualhost_sql_set.add(generate_sql(config.virtualmachine_table, item.name, generate_dict(item, relations.itop_vms)))

for query in virtualhost_sql_set:
    db.execute(query)

itop.run_sync(config.virtualmachine_table_id)

