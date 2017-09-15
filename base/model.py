class Field(object):
    def __init__(self):
        self.value = None

    def set(self, value):
        self.value = value
        return True

    def get(self):
        return self.value

    def delete(self):
        self.value = None


class Item(object):
    def __getattr(self, key):
        try:
            feild = getattr(self, key)
        except:
            raise ValueError('没有这种key存在' + key)
        return feild

    @classmethod
    def get_all(cls):
        field_dict = cls.__dict__
        all_attr = {}
        for key, field in field_dict.items():
            if isinstance(field, Field):
                all_attr[key] = field.value
        return all_attr

    def get(self, key, default=None):
        feild = self.__getattr(key)
        if feild.get():
            return feild.get()
        else:
            return default

    def set(self, key, value, default=None):
        feild = self.__getattr(key)
        if not value:
            value = default
        if feild.set(value):
            return True

    def delete(self, key):
        feild = self.__getattr(key)
        feild.delete()

    def delete_list(self, key_list):
        for key in key_list:
            self.delete(key)

    def set_list(self, data_dict):
        if isinstance(data_dict, list) or isinstance(data_dict, tuple):
            for idx, data in enumerate(data_dict):
                if isinstance(data, dict):
                    if not self.set(data[0], data[1]):
                        self.delete_list(data_dict[0:idx])
                        return False, '第%s元素存入不成功' % (idx + 1)
                else:
                    return False, 'data_dict的元素应为字典'
            return True, ''
        else:
            return False, 'data_dict类型应该是列表或元组'
