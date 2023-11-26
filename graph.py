class GPS:
    number_cities = .8
    target_city = ["Чита", 52.0317, 113.501]
    start_city, start_city_coordinate = None, None
    min_dolg, min_shir, max_dolg, max_shir = None, None, None, None
    step = 10
    cities = None
    def parsing_coordinate(self) -> list:
        import requests
        from bs4 import BeautifulSoup as bs
        request = [i.text.strip("\xa0")
                   for i in bs(requests.get("https://alextyurin.ru/2014/04/%D0%B3%D0%B5%D0%"
                                            "BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5-%D0%BA%D0%BE%D0%BE%D1%80"
                                            "%D0%B4%D0%B8%D0%BD%D0%B0%D1%82%D1%8B-%D0%BE%D1%81"
                                            "%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D1%85/").text, "html.parser").find_all("td")
                   if not i.text in ("Россия", "Киргизия", "Украина", "Беларусь", "Абхазия", "Узбекистан")] + self.target_city
        result = [(i[0], (float(i[1]), float(i[2]))) for i in [request[i:i+3] for i in range(1, len(request) + 1) if i % 3 == 0] if i != []]
        self.cities = result
        self.number_cities = len(result) * self.number_cities
        self.start_city = input(">: ")
        self.start_city_coordinate, = [i[1] for i in result if self.start_city == i[0]]
        self.def_border()
        print(self.target_city, self.start_city_coordinate)
        print(self.min_dolg, self.max_dolg, self.min_shir, self.max_shir)
        #for i in result: print(i)
        return result

    def def_border(self):

        a, b = (self.target_city[1], self.target_city[2]), self.start_city_coordinate
        self.min_dolg  = a[1] if a[1] < b[1] else b[1]
        self.max_dolg = a[1] if a[1] > b[1] else b[1]
        self.min_shir = a[0] if a[0] < b[0] else b[0]
        self.max_shir = a[0] if a[0] > b[0] else b[0]

    def get_distance(self, array: list):
        from geopy.distance import geodesic as GD
        current_city_id, current_city, data_distance = -1, "",  {}
        for i in array:
            current_city_id += 1
            current_city = array[current_city_id][0]
            for j in array[current_city_id+1:]:
                data_distance.update({f"{current_city}%{j[0]}": round(GD(array[current_city_id][1], j[1]).km, 0)})
        return data_distance

    def def_allow_city(self, city):
        city_coordinate = None
        for i in self.cities:
            if i[0] == city: city_coordinate = i[1]
        return (self.min_dolg <= city_coordinate[1] <= self.max_dolg) and (self.min_shir <= city_coordinate[0] <= self.max_shir)

    def def_path(self, city: str, paths: dict, trash: list=[]) -> str:
        time_result, result, city_next = [], [], None
        for i in paths.items():
            objective = i[0].split("%")
            if city in objective: city_next = objective[(len(objective)-1) - objective.index(city)]
            if city in objective and not (objective[0] in trash or objective[1] in trash) and self.def_allow_city(city_next):
                time_result.append(i[1])
                result.append(i)
        return result[time_result.index(min(time_result))][0] if time_result else ""

    def get_min_path(self, dictionary: dict) -> list:
        trash, result = [], []
        current_city = self.start_city
        self.dictionary = dictionary
        while current_city != "Чита":
            result.append(current_path := self.def_path(current_city, dictionary, trash))
            current_path = current_path.split("%")
            previous_city = current_path[current_path.index(current_city)]
            for i in self.cities:
                if i[0] == previous_city: print(i[1])
            if not previous_city in trash: trash.append(previous_city)
            current_city = current_path[(len(current_path)-1) - current_path.index(current_city)]

        return result

    def print(self):
        result = self.get_min_path(self.get_distance(self.parsing_coordinate()))
        for i in result:
            row = i.split("%")
            print(f"{row[0]:20} - {row[1]:20}: {self.dictionary[i]}")
        print(f"Итог: {sum([i[1] for i in self.dictionary.items() if i[0] in result])} км")
    def start(self):
        self.print()


GPS().start()