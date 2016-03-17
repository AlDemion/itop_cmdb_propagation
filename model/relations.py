roles = {
    'Administrator': ('CN=Administrator,OU=Groups,DC=example,DC=org',),
    'Configuration Manager': ('CN=Configuration Manager,OU=Groups,DC=example,DC=org',),
    'Portal power user': ('CN=Portal power user,OU=Groups,DC=example,DC=org',),
    'Support Agent': ('CN=Support Agent,OU=Groups,DC=example,DC=org',),
}

brands = {
    'name': 'name'
}

os_familys = {
    'name': 'name'
}

os_versions = {
    'name': 'name',
    'osfamily': 'osfamily',
}

models = {
    'name': 'name',
    'brand': 'brand',
}

hypervisor = {
    'name': 'name',
    'description': 'description',
    'server': 'server',
}

server_status = {
    'production': ('sp', 'sd'),
    'implementation': ('ss', 'st'),
}

servers = {
    'asset_number': 'asset_number',
    'brand': 'brand',
    'cpu_count': 'cpu_count',
    'cpu_type': 'cpu_type',
    'description': 'description',
    'managementip': 'managementip',
    'model': 'model',
    'name': 'name',
    'osfamily': 'osfamily',
    'osversion': 'osversion',
    'ram': 'ram',
    'serialnumber': 'serialnumber',
}

vms = {
    'name': 'name',
    'description': 'description',
    'virtualhost': 'virtualhost',
    'osfamily': 'osfamily',
    'osversion': 'osversion',
    'cpu_count': 'cpu_count',
    'cpu_type': 'cpu_type',
    'ram': 'ram',
    'managementip': 'managementip',
    'power_state': 'power_state',
}

'''
Here we map class attributes with Active Directory values
'''
user = {
    'login': ('sAMAccountName',),
    'profile_list': ('memberOf',),
    'email': ('mail',),
}

person = {
    'name': ('sn',),
    'status': ('userAccountControl',),
    'email': ('mail',),
    'first_name': ('givenName',),
    'employee_number': ('employeeNumber',),
}


'''
Here we map class attributes with Foreman values
'''
foreman_os_versions = {
    'name': 'operatingsystemrelease',
    'osfamily': 'osfamily',
}

foreman_server = {
    'brand': 'manufacturer',
    'model': 'productname',
    'osfamily': 'osfamily',
    'osversion': 'operatingsystemrelease',
    'cpu_count': 'processorcount',
    'cpu_type': 'processor0',
    'ram': 'memorysize_mb',
    'serialnumber': 'serialnumber',
    'asset_number': 'serialnumber',
    'managementip': 'ipaddress'
}

foreman_virtual_machine = {
    'osfamily': 'osfamily',
    'osversion': 'operatingsystemrelease',
    'cpu_type': 'processor0',
    'cpu_count': 'processorcount',
    'ram': 'memorysize_mb',
    'managementip': 'ipaddress'
}

foreman_models = {
    'name': 'productname',
    'brand': 'manufacturer',
}

'''
Here we map class attributes with VMware values
'''
vmware_server = {
    'name': 'name',
    'host': 'summary.host',
    'description': 'customValue',
    'licensing': 'summary.hardware.otherIdentifyingInfo',
    'brand': 'summary.hardware.vendor',
    'model': 'summary.hardware.model',
    'managementip': 'name',
    'osfamily': 'summary.config.product.name',
    'osversion': 'summary.config.product.version',
    'cpu_type': 'summary.hardware.cpuModel',
    'cpu_count': 'summary.hardware.numCpuThreads',
    'ram': 'summary.hardware.memorySize',
}

vmware_hypervisor = {
    'name': 'name',
    'description': 'customValue',
    'server': 'summary.host',
}

vmware_virtual_machine = {
    'name': 'name',
    'power_state': 'runtime.powerState',
    'description': 'customValue',
    'virtualhost': 'runtime.host',
    'osfamily': 'guest.guestFamily',
    'osversion': 'guest.guestFullName',
    'ram': 'summary.config.memorySizeMB',
    'cpu_count': 'summary.config.numCpu',
    'managementip': 'guest.ipAddress',
}

vmware_farm = {
    'name': 'name'
}

vmware_brands = {
    'name': 'manufacturer'
}

vmware_hosts_os_versions = {
    'name': 'summary.config.product.version',
    'osfamily': 'summary.config.product.name',
}

vmware_vms_os_versions = {
    'name': 'guest.guestFullName',
    'osfamily': 'guest.guestFamily',
}

vmware_models = {
    'name': 'summary.hardware.model',
    'brand': 'summary.hardware.vendor',
}

# Here we store MySQL fields for iTop
itop_person = [
    'name',
    'status',
    'org_id',
    'email',
    'notify',
    'first_name',
    'employee_number',
    'location_id'
]

itop_user = [
    'login',
    'language',
    'profile_list',
    'contactid',
]

itop_farm = [
    'name',
    'org_id',
]

itop_brand = [
    'name'
]

itop_osfamily = [
    'name'
]

itop_osversion = [
    'name',
    'osfamily_id',
]

itop_model = [
    'name',
    'brand_id',
    'type'
]

itop_server = [
    'name',
    'description',
    'org_id',
    'serialnumber',
    'location_id',
    'status',
    'brand_id',
    'model_id',
    'asset_number',
    'managementip',
    'osfamily_id',
    'osversion_id',
    'cpu',
    'ram',
]

itop_hypervisor = [
    'name',
    'description',
    'org_id',
    'farm_id',
    'server_id',
    'status',
]

itop_vms = [
    'name',
    'description',
    'org_id',
    'virtualhost_id',
    'osfamily_id',
    'osversion_id',
    'cpu',
    'ram',
    'managementip',
    'status',
]

# Here we store substitution database
brands_substitution = {
    'Desktop PC': ('System manufacturer',
                   'Phoenix Technologies LTD',
                   'American Megatrends Inc.',
                   )
}

os_familys_substitution = {
    'Linux': ('linuxGuest',
              'Suse',
              'Debian',
              'RedHat',
              ),
    'Windows': ('windowsGuest',
                'windows',
                ),
}

os_versions_substitution = {
    'Microsoft Windows 7 (64-bit)': ('6.1.7601',),
    'Ubuntu Linux 12.04': ('12.04',),
    'Ubuntu Linux 14.04': ('14.04',
                           'Ubuntu Linux (64-bit)',
                           'Ubuntu Linux (32-bit)',
                           ),
    'VMware ESXi 6': ('6.0.0',),
}

os_models_substitution = {
    'Desktop PC': ('System Product Name',),
}

asset_number_substitution = {
    'Not available': ('System Serial Number',),
}

serial_number_substitution = {
    'Not available': ('System Serial Number',),
}
