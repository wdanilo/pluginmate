class ListDict:
    class __KeyView:
        def __init__(self, map):
            self.__map = map

        def __getitem__(self, idx):
            return self.__map.key_at(idx)

    class __ValView:
        def __init__(self, map):
            self.__map = map

        def __getitem__(self, idx):
            return self.__map.val_at(idx)

    # implementation
    def __init__(self):
        self.__map = {}
        self.__list = []
        self.__key_view = ListDict.__KeyView(self)
        self.__val_view = ListDict.__ValView(self)

    @property
    def key(self): return self.__key_view

    @property
    def val(self): return self.__val_view

    def append(self, key, val):
        if key in self:
            raise KeyError
        self.__append(key,val)

    def push(self, key, val):
        return self.append(key, val)

    def pop(self):
        key = self.__list.pop()
        val = self.__map[key]
        del self.__map[key]
        return key, val

    def items(self):       return self.__map.items()

    def keys(self):        return self.__map.keys()

    def values(self):      return self.__map.values()

    def key_at(self, idx): return self.__list[idx]

    def val_at(self, idx): return self.__map[self.key_at(idx)]

    def __contains__(self, key):
        return key in self.__map

    def __setitem__(self, key, val):
        if key in self:
            del self[key]
        self.__append(key, val)

    def __getitem__(self, key):
        return self.__map[key]

    def __delitem__(self, key):
        del self.__map[key]
        self.__list.remove(key)

    def __append(self, key, val):
        self.__map[key] = val
        self.__list.append(key)

    def __len__(self):
        return len(self.__list)

    def __str__(self):
        return '{%s}'%(', '.join(['%s: %s'%(key, val) for key, val in self.items()]))
