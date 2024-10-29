from Entities.CoffeeMachine import CoffeeMachine
from Entities.CoffeeRecipe import CoffeeRecipe
from Entities.Order import Order
import streamlit as st

st.title(":coffee: Coffee Machine")


if 'machine' not in st.session_state:
    st.session_state.machine = CoffeeMachine(100, 300, 200, 0)

machine = st.session_state.machine
paymentVisibility = False


machine_on = st.sidebar.toggle("Makineyi Aç", value=False)
showReport = st.sidebar.toggle("Raporu Göster", value=False)


if showReport:
    st.sidebar.text(machine.report())
else:
    st.sidebar.text("")

placeholderCoffee = None
placeholderPayment = None
payment_completed = False

if machine_on:
    tab1, tab2 = st.tabs(["Kahve Seçimi", "Ödeme"])

    with tab1:
        containerCoffee = st.container()
        placeholderCoffee = containerCoffee.empty()

        coffeeChoice = containerCoffee.radio("Kahve seçiminizi yapınız", ["Espresso $1.5", "Cappuccino $3", "Latte $2.5", "Special $3.5"], horizontal=True)

        if coffeeChoice == "Espresso $1.5":
            coffee = CoffeeRecipe("Espresso", 18, 18, 0, 1.5)
        elif coffeeChoice == "Latte $2.5":
            coffee = CoffeeRecipe("Latte", 24, 200, 150, 2.5)
        elif coffeeChoice == "Cappuccino $3":
            coffee = CoffeeRecipe("Cappuccino", 24, 150, 100, 3)
        elif coffeeChoice == "Special $3.5":
            coffeeBeans = containerCoffee.slider("Kahve çekirdeği (gr):", 0, 300, 25)
            milk = containerCoffee.slider("Süt (ml):", 0, 300, 25)
            water = containerCoffee.slider("Su (ml)", 0, 300, 25)
            coffee = CoffeeRecipe("Special", coffeeBeans, water, milk, 3.5)

    with tab2:
        containerPayment = st.container()

        if not payment_completed:
            placeholderPayment = containerPayment.empty()
            quarters = containerPayment.number_input("Insert a quarters", 0)
            dimes = containerPayment.number_input("Insert a dimes", 0)
            nickels = containerPayment.number_input("Insert a nickels", 0)
            pennies = containerPayment.number_input("Insert a pennies", 0)

            order = Order(coffee, quarters, dimes, nickels, pennies)
            payment = containerPayment.button("Ödemeyi Tamamla")

            if payment:
                result = order.make_coffee(machine)
                payment_completed = True 
                containerPayment.empty() 
                st.success(result) 
else:

    if placeholderPayment is not None:
        placeholderPayment.empty() 
    if placeholderCoffee is not None:
        placeholderCoffee.empty()

    # Makine kapandığında gösterilecek mesaj
    st.markdown("Makine kapalı. :zzz:")
