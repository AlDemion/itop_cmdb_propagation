import model.relations as relations
import config


class ContentItem(object):

    def __init__(self, ):
        self.id = int()


class User(ContentItem):

    def __init__(self):
        ContentItem.__init__(self)
        self.contactid = int()
        self._login = ''
        self._language = 'EN US'
        self._profile_list = 'profileid->name:Portal User;reason:Default role for user'
        self._email = ''

    @property
    def email(self):
        return self._email

    @property
    def login(self):
        return self._login

    @property
    def profile_list(self):
        return self._profile_list

    @property
    def language(self):
        return self._language

    @email.setter
    def email(self, value):
        self._email = value[0]

    @login.setter
    def login(self, value):
        self._login = value[0]

    @profile_list.setter
    def profile_list(self, value):
        start_pattern = 'profileid->name:'
        reason = ';reason:Membership in proper AD group'
        for role, groups in relations.roles.iteritems():
            for group in groups:
                if group in value:
                    self._profile_list = start_pattern + role + reason
                    return

    @language.setter
    def language(self, value):
        possible_values = ('EN US', 'DE DE')
        if value in possible_values:
            self._language = value
        else:
            return


class Person(ContentItem):

    def __init__(self):
        ContentItem.__init__(self)
        self.notify = 'yes'
        self.org_id = int()
        self.location_id = int()
        self._name = ''
        self._status = ''
        self._email = ''
        self._first_name = ''
        self._employee_number = ''

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def email(self):
        return self._email

    @property
    def first_name(self):
        return self._first_name

    @property
    def employee_number(self):
        return self._employee_number

    @name.setter
    def name(self, value):
        self._name = value[0]

    @status.setter
    def status(self, value):
        if value[0] == '514':
            self._status = 'inactive'
        else:
            self._status = 'active'

    @email.setter
    def email(self, value):
        self._email = value[0]

    @first_name.setter
    def first_name(self, value):
        self._first_name = value[0]

    @employee_number.setter
    def employee_number(self, value):
        self._employee_number = value[0]


class UserLDAP(User):

    def __init__(self):
        User.__init__(self)


class UserExternal(User):

    def __init__(self):
        User.__init__(self)
        self._login = ''

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = config.ldap_domain_prefix + value[0]


class Farm(ContentItem):

    def __init__(self):
        ContentItem.__init__(self)
        self.name = ''
        self.org_id = int()


class Server(ContentItem):

    def __init__(self):
        ContentItem.__init__(self)
        self.name = ''
        self._brand = ''
        self._model = ''
        self._description = 'Not available'
        self.org_id = int()
        self._serialnumber = ''
        self.location_id = int()
        self.brand_id = int()
        self.model_id = int()
        self._asset_number = ''
        self.managementip = ''
        self._osfamily = ''
        self._osversion = ''
        self.osfamily_id = int()
        self.osversion_id = int()
        self.cpu_type = ''
        self.cpu_count = ''
        self._ram = ''

    @property
    def description(self):
        return self._description.replace('"', '\\"')

    @property
    def ram(self):
        return str(self._ram) + ' MB'

    @property
    def serialnumber(self):
        return self._serialnumber

    @property
    def asset_number(self):
        return self._asset_number

    @property
    def brand(self):
        return self._brand

    @property
    def cpu(self):
        return str(self.cpu_count) + ' x ' + self.cpu_type

    @property
    def status(self):
        for key, value in relations.server_status.iteritems():
            for item in value:
                if item in self.name:
                    return key
        return 'production'

    @property
    def model(self):
        return self._model

    @property
    def osfamily(self):
        return self._osfamily

    @property
    def osversion(self):
        return self._osversion

    @osfamily.setter
    def osfamily(self, value):
        for key, val in relations.os_familys_substitution.iteritems():
            if value in val:
                self._osfamily = key
                break

        if not self._osfamily:
            self._osfamily = value

    @osversion.setter
    def osversion(self, value):
        for key, val in relations.os_versions_substitution.iteritems():
            if value in val:
                self._osversion = key
                break

        if not self._osversion:
            self._osversion = value

    @model.setter
    def model(self, value):
        for key, val in relations.os_models_substitution.iteritems():
            if value in val:
                self._model = key
                break

        if not self._model:
            self._model = value

    @ram.setter
    def ram(self, value):
        self._ram = int(float(value))

    @brand.setter
    def brand(self, value):
        for key, val in relations.brands_substitution.iteritems():
            if value in val:
                self._brand = key
                break

        if not self._brand:
            self._brand = value

    @serialnumber.setter
    def serialnumber(self, value):
        for key, val in relations.serial_number_substitution.iteritems():
            if value in val:
                self._serialnumber = key
                break

        if not self._serialnumber:
            self._serialnumber = value

    @asset_number.setter
    def asset_number(self, value):
        for key, val in relations.asset_number_substitution.iteritems():
            if value in val:
                self._asset_number = key
                break

        if not self._asset_number:
            self._asset_number = value

    @description.setter
    def description(self, value):
        self._description = value



class Hypervisor(ContentItem):

    def __init__(self):
        ContentItem.__init__(self)
        self.name = ''
        self._description = ''
        self.org_id = int()
        self.farm = ''
        self.farm_id = int()
        self.server = ''
        self.server_id = int()

    @property
    def description(self):
        return self._description.replace('"', '\\"')

    @property
    def status(self):
        for key, value in relations.server_status.iteritems():
            for item in value:
                if item in self.name:
                    return key
        return 'production'

    @description.setter
    def description(self, value):
        self._description = value



class VirtualMachine(ContentItem):

    def __init__(self):
        ContentItem.__init__(self)
        self.name = ''
        self.power_state = ''
        self._description = ''
        self.virtualhost = ''
        self._osfamily = ''
        self._osversion = ''
        self.org_id = int()
        self.virtualhost_id = int()
        self.osfamily_id = int()
        self.osversion_id = int()
        self.oslicence_id = int()
        self.cpu_type = 'Virtual CPU'
        self.cpu_count = ''
        self.ram = ''
        self.managementip = ''

    @property
    def cpu(self):
        return str(self.cpu_count) + ' x ' + self.cpu_type

    @property
    def status(self):
        if self.power_state == 'poweredOff':
            return 'obsolete'
        for key, value in relations.server_status.iteritems():
            for item in value:
                if item in self.name:
                    return key
        return 'production'

    @property
    def osfamily(self):
        return self._osfamily

    @property
    def description(self):
        return self._description.replace('"', '\\"')

    @property
    def osversion(self):
        return self._osversion

    @description.setter
    def description(self, value):
        self._description = value

    @osfamily.setter
    def osfamily(self, value):
        for key, val in relations.os_familys_substitution.iteritems():
            if value in val:
                self._osfamily = key
                break

        if not self._osfamily:
            self._osfamily = value

    @osversion.setter
    def osversion(self, value):
        for key, val in relations.os_versions_substitution.iteritems():
            if value in val:
                self._osversion = key
                break

        if not self._osversion:
            self._osversion = value
