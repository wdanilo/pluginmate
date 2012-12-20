from collections import defaultdict

class AssociationMap:
    class Reversed():
        def __init__(self, map):
            self.__map = map
        def bind       (self, key, val): return self.__map.bind(val, key)
        def unbind     (self, key, val): return self.__map.unbind(val, key)
        def keys       (self):           return self.__map.vals()
        def vals       (self):           return self.__map.keys()
        def key        (self, key):      return self.__map.val(key)
        def val        (self, val):      return self.__map.key(val)
        def remove_key (self, key):      return self.__map.remove_val(key)
        def remove_val (self, val):      return self.__map.remove_key(val)
        def reversed   (self):           return self.__map

    def __init__(self, keys=None, vals=None):
        if keys is None: keys = defaultdict(set)
        if vals is None: vals = set()
        self.__keys = keys
        self.__vals = vals
        self.__reversed = AssociationMap.Reversed(self)

    def bind(self, key, val):
        self.__keys[key].add(val)
        self.__vals.add(val)

    def add_key(self, key):
        self.__keys[key] = set()

    def add_val(self, val):
        self.__vals.add(val)

    def keys(self):
        return self.__keys.keys()

    def vals(self):
        return self.__vals

    def key(self, key):
        return self.__keys[key]

    def items(self):
        return self.__keys.items()

    def unbind(self, key, val):
        self.__keys[key].remove(val)
        #self.__clean_vals(key)
        #self.__clean_keys(val)

    def remove_key(self, key):
        for val in self.key(key):
            self.__vals[val].remove(key)
            #self.__clean_keys(val)
        del self.__keys[key]

    def remove_val(self, val):
        self.__vals.remove(val)

    def reversed(self):
        return self.__reversed

    def create_domain(self):
        return Domain(self)

    def __clean_vals(self, key):
        if not self.__keys[key]: del self.__keys[key]

    def __clean_keys(self, val):
        if not self.__vals[val]: del self.__vals[val]

    def __str__(self):
        return '\n'.join(['%s -> {%s}'%(key, ', '.join([str(val) for val in vals])) for key, vals in self.items()])


class BiAssociationMap(AssociationMap):
    def __init__(self, keys=None, vals=None):
        if keys is None: keys = defaultdict(set)
        if vals is None: vals = defaultdict(set)
        super().__init__(keys, vals)
        self.__keys = keys
        self.__vals = vals

    def bind(self, key, val):
        self.__keys[key].add(val)
        self.__vals[val].add(key)

    def add_val(self, val):
        self.__vals[val] = set()

    def vals(self):
        return self.__vals.keys()

    def val(self, val):
        return self.__vals[val]

    def unbind(self, key, val):
        super().unbind(key, val)
        self.__vals[val].remove(key)

    def remove_val(self, val):
        for key in self.val(val):
            self.__keys[key].remove(val)
            #self.__clean_vals(key)
        del self.__vals[val]

'''
class Interface:
    pass
class Service:
    pass
class Plugin:
    pass

i1 = Interface()
i2 = Interface()
i3 = Interface()
s1 = Service()
s2 = Service()
s3 = Service()
p1 = Plugin()
p2 = Plugin()
p3 = Plugin()

map = AssociationMap()
map.bind(s1, i1)
map.bind(p1, i1)

print (list(map.keys()))
#'''

class Domain:
    def __init__(self, map, name=None):
        self.__name = name
        self.__map = map
        self.__set = set()

    def add(self, element):
        self.__set.add(element)

    def __contains__(self, item):
        return item in self.__set

    def __iter__(self):
        return self.__map.__iter__()

    def remove(self, element):
        self.__set.remove(element)
        for map in self.__map.get_maps(self):
            map.remove_key(element)

    def __str__(self):
        return "Domain '%s'" % self.__name

class MulitAssociationMap:
    def __init__(self):
        self.__maps = {}
        self.__domain_map = {}

    def create_domain(self, name=None):
        domain = Domain(self, name)
        self.__domain_map[domain] = set()
        return domain

    def get_maps(self, domain):
        return self.__domain_map[domain]

    def __call__(self, srcdomain, dstdomain):
        key = (srcdomain, dstdomain)
        if not key in self.__maps:
            rkey = (dstdomain, srcdomain)
            map = AssociationMap()
            rmap = map.reversed()
            self.__domain_map[dstdomain].add(rmap)
            self.__domain_map[srcdomain].add(map)
            self.__maps[rkey] = rmap
            self.__maps[key] = map
        return self.__maps[key]




'''
a = MulitAssociationMap()
d1 = a.create_domain()
d2 = a.create_domain()

d1.add('a')
d1.add('b')

d2.add(1)

a(d1,d2).bind('a', 1)
a(d1,d2).bind('b', 1)

print(a(d1, d2).reversed().key(1))
#'''

'''
assocation = MulitAssociationMap()
interfaces = assocation.get_domain()
services = assocation.get_domain()

interfaces.add('a')
interfaces.add('b')
interfaces.add('c')
services.add(1)
services.add(2)
services.add(3)

assocation = MulitAssociationMap()
assocation(interfaces, services)
'''

