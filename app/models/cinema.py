class Cinema:
    def __init__(self, id, name, city_id, city_name=None):
        self.id = id
        self.name = name
        self.city_id = city_id
        self.city_name = city_name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_city_id(self):
        return self.city_id

    def get_city_name(self):
        return self.city_name
