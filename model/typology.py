import relations


class Typology(object):

    def __init__(self):
        self.id = int()


class Organization(Typology):

    def __init__(self):
        Typology.__init__(self)
        self.name = None


class Location(Typology):

    def __init__(self):
        Typology.__init__(self)
        self.name = None


class Brand(Typology):

    def __init__(self):
        Typology.__init__(self)
        self._name = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        for key, val in relations.brands_substitution.iteritems():
            if value in val:
                self._name = key
                break

        if not self._name:
            self._name = value


class Model(Typology):

    def __init__(self):
        Typology.__init__(self)
        self._name = None
        self._brand = None
        self.brand_id = int()
        self.type = 'Server'

    @property
    def brand(self):
        return self._brand

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        for key, val in relations.os_models_substitution.iteritems():
            if value in val:
                self._name = key
                break

        if not self._name:
            self._name = value

    @brand.setter
    def brand(self, value):
        for key, val in relations.brands_substitution.iteritems():
            if value in val:
                self._brand = key
                break

        if not self._brand:
            self._brand = value


class OSFamily(Typology):

    def __init__(self):
        Typology.__init__(self)
        self._name = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        for key, val in relations.os_familys_substitution.iteritems():
            if value in val:
                self._name = key
                break

        if not self._name:
            self._name = value


class OSVersion(Typology):

    def __init__(self):
        Typology.__init__(self)
        self._osfamily = None
        self.osfamily_id = int()
        self._name = None

    @property
    def name(self):
        return self._name

    @property
    def osfamily(self):
        return self._osfamily

    @name.setter
    def name(self, value):
        for key, val in relations.os_versions_substitution.iteritems():
            if value in val:
                self._name = key
                break

        if not self._name:
            self._name = value

    @osfamily.setter
    def osfamily(self, value):
        for key, val in relations.os_familys_substitution.iteritems():
            if value in val:
                self._osfamily = key
                break

        if not self._osfamily:
            self._osfamily = value
