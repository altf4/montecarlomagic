class ManaCost():
    def __init__(self, cost_string):
        self.cmc = 0
        self.colors = {}
        self.colorless = 0
        self.cost_string = cost_string
        if cost_string[0].isdigit():
            self.colorless = int(cost_string[0])
        self.colors["red"] = cost_string.count("r")
        self.colors["blue"] = cost_string.count("u")
        self.colors["white"] = cost_string.count("w")
        self.colors["black"] = cost_string.count("b")
        self.colors["green"] = cost_string.count("g")

        self.cmc = self.colors["red"] + self.colors["blue"] + \
            self.colors["white"] + self.colors["black"] + self.colors["green"] + self.colorless

    def __str__(self):
        return self.cost_string
