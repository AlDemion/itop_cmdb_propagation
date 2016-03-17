import ldap
import config


class ActiveDirectory:

    def __init__(self):
        self.host = config.ldap_host
        self.user = config.ldap_bind_user
        self.password = config.ldap_bind_password
        self.base = config.ldap_search_base
        self.initialize = ldap.initialize(self.host)
        self.initialize.protocol_version = ldap.VERSION3
        self.initialize.set_option(ldap.OPT_REFERRALS, 0)
        self.connection = self.initialize.simple_bind_s(self.user, self.password)

    def get_users(self):
        result = self._query(config.ldap_filter, config.ldap_attributes)
        return result

    def _query(self, ldap_filter, ldap_attributes):
        result = self.initialize.search_s(self.base, ldap.SCOPE_SUBTREE, ldap_filter, ldap_attributes)
        results = [entry for dn, entry in result if isinstance(entry, dict)]

        return results

    def __del__(self):
        self.initialize.unbind()
