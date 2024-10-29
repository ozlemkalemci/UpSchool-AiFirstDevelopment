class Order:
    def __init__(self, coffee, quarters, dimes, nickels, pennies):
        self.coffee = coffee
        self.quarters = quarters
        self.dimes = dimes
        self.nickels = nickels
        self.pennies = pennies

    def process_coins(self):
        total = self.quarters * 0.25 + self.dimes * 0.10 + self.nickels * 0.05 + self.pennies * 0.01
        return total

    def check_transaction(self, money_received, cost):
        if money_received < cost:
            return False, f"Üzgünüz, eksik ödeme yaptınız. Para iade edildi: ${money_received}"
        change = round(money_received - cost, 2)
        return True, f"Para üstü: ${change}" if change > 0 else "İşlem başarılı, para üstü yok."

    def make_coffee(self, machine):
        resource_check = machine.check_resources(self.coffee)
        if resource_check == True:
            payment = self.process_coins()
            success, message = self.check_transaction(payment, self.coffee.money)

            if success:
                machine.water -= self.coffee.water
                machine.milk -= self.coffee.milk
                machine.coffeeBeans -= self.coffee.coffeeBeans
                machine.money += self.coffee.money

                return f"{self.coffee.coffeeName} hazır. Afiyet olsun! {message}"
            else:
                return message
        else:
            return resource_check

