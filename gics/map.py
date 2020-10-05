class Map(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    @staticmethod
    def create_recursively(data: dict) -> 'Map':
        data = Map(data)

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = Map.create_recursively(value)

        return data
