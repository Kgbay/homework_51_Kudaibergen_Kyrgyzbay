import json

class JsonWriterReader:

    def __init__(self, name, age, happiness, satiety, age_naming):
        self.satiety = satiety
        self.happiness = happiness
        self.age = age
        self.name = name
        self.age_naming = age_naming

    def write_into(self):
        dict = {}
        dict["name"] = self.name
        dict["age"] = self.age
        dict["happiness"] = self.happiness
        dict["satiety"] = self.satiety
        dict["age_naming"] = self.age_naming
        data = self.read_from()
        data.append(dict)
        with open("webapp/data.json", "w") as file:
            json.dump(data, file)

    @staticmethod
    def read_from() -> list:
        with open("webapp/data.json", "r") as file:
            lst = json.load(file)
        return lst


