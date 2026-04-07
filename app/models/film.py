class Film:
    def __init__(self, id, name, genre, age_rating, description, time_duration):
        self.id = id
        self.name = name
        self.genre = genre
        self.age_rating = age_rating
        self.description = description
        self.time_duration = time_duration

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_genre(self):
        return self.genre

    def get_age_rating(self):
        return self.age_rating

    def get_description(self):
        return self.description

    def get_time_duration(self):
        return self.time_duration
