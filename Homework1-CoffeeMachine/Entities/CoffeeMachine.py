class CoffeeMachine():
    def __init__(self, coffeeBeans, water, milk, money):
        self.coffeeBeans = coffeeBeans
        self.water = water
        self.milk = milk
        self.money = money

    def check_resources(self, recipe): # kaynak yeterliliği kontrol etmek için
        if self.water < recipe.water:
            return "Yeterli miktarda su bulunmamaktadır"
        if self.milk < recipe.milk:
            return "Yeterli miktarda süt bulunmamaktadır"
        if self.coffeeBeans < recipe.coffeeBeans:
            return "Yeterli miktarda kahve çekirdeği bulunmamaktadır"
        return True

    def report(self):
        return (f"Su: {self.water}ml\n"
                f"Süt: {self.milk}ml\n"
                f"Kahve: {self.coffeeBeans}g\n"
                f"Para: ${self.money}")