# Active Directory parameters
ldap_host = 'ldap://example.org'
ldap_domain_prefix = 'EXAMPLE\\\\'
ldap_bind_user = 'bind@example.org'
ldap_bind_password = ''
ldap_search_base = 'dc=example,dc=org'
ldap_filter = "(&(objectclass=user)(objectclass=person)(employeeNumber=*)(mail=*)(sn=*)(givenName=*))"
ldap_attributes = ('sAMAccountName',
                   'employeeNumber',
                   'memberOf',
                   'sn',
                   'givenName',
                   'mail',
                   'userAccountControl',
                   )

# iTop
itop_login = 'admin'
itop_pass = ''
itop_fqdn = 'itop.example.org'

# iTop Synchro tables
userldap_table = 'synchro_data_userldap_1'
userexternal_table = 'synchro_data_userexternal_2'
persons_table = 'synchro_data_person_3'
farm_table = 'synchro_data_farm_4'
brand_table = 'synchro_data_brand_5'
osfamily_table = 'synchro_data_osfamily_6'
osversion_table = 'synchro_data_osversion_7'
model_table = 'synchro_data_model_8'
server_table = 'synchro_data_server_9'
hypervisor_table = 'synchro_data_hypervisor_10'
virtualmachine_table = 'synchro_data_virtualmachine_11'

# iTop Synchro ID's
userldap_table_id = '1'
userexternal_table_id = '2'
persons_table_id = '3'
farm_table_id = '4'
brand_table_id = '5'
osfamily_table_id = '6'
osversion_table_id = '7'
model_table_id = '8'
server_table_id = '9'
hypervisor_table_id = '10'
virtualmachine_table_id = '11'

# VMware
vmware_host = 'vcenter.example.org'
vmware_user = 'admin'
vmware_pass = ''

# MySQL
mysql_host = 'mysql.itop.example.org'
mysql_user = 'admin'
mysql_pass = ''
mysql_db = 'itop_db'

# Foreman
foreman_login = 'admin'
foreman_pwd = ''
foreman_url = 'https://foreman.example.org'
