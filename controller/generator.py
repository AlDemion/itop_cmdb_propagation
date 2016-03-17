from datasources.database import Database

db = Database()


def generate_attributes(data, relation_name, class_name):
    result = []
    for item in data:
        class_object = class_name()
        for prop, val in item.iteritems():
            for key, values in relation_name.iteritems():
                if prop in values:
                    class_object.__setattr__(key, val)

        result.append(class_object)

    return result


def merge_dicts(lst1, lst2):
    result = []
    lst1.extend(lst2)
    for myDict in lst1:
        if myDict not in result:
            result.append(myDict)

    return result


def merge_vms(vmware_vms_data, foreman_vms_data):
    all_vms = []
    merge_facts = ['cpu_type',
                   'cpu_count',
                   'managementip',
                   'osfamily',
                   'osversion',
                   ]
    for vmware_vm in vmware_vms_data:
        node = vmware_vm
        all_vms.append(node)
        for foreman_vm in foreman_vms_data:
            try:
                if vmware_vm['name'] in foreman_vm['name'] or foreman_vm['managementip'] == vmware_vm['managementip']:
                    for fact in merge_facts:
                        try:
                            node[fact] = foreman_vm[fact]
                        except KeyError:
                            pass
            except KeyError:
                pass

    return all_vms


def generate_sql(mysql_table, primary_key, item):
    pk = db.query(db.generate_select_pk_query(mysql_table, db.generate_primary_key(primary_key)))
    if pk:
        return db.generate_query(mysql_table, db.generate_primary_key(primary_key), item, 'update')
    else:
        return db.generate_query(mysql_table, db.generate_primary_key(primary_key), item)


def generate_dict(obj, values):
        result = {}
        for value in values:
            result[value] = getattr(obj, value)

        return result
