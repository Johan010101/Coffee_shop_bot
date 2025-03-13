import pyttsx3
import random

def speak(text, rate=120, use_random_effects=True):
    """Speaks the given text with optional random effects."""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    if use_random_effects:
        apply_random_effects(engine, text)
    else:
        engine.say(text)

    engine.runAndWait()
    engine.stop()

def apply_random_effects(engine, text):
    """Applies random speech effects to the text."""
    words = text.split()
    new_words = []
    for word in words:
        new_words.append(word)
        if random.random() < 0.1:  # 10% chance for a random effect
            engine.setProperty('rate', random.randint(100, 200))  # Vary rate
            new_words.append(random.choice(["uh", "um", "err"])) # Random interjection
        elif random.random() < 0.05: #5% chance to pause
            engine.say("")
            engine.runAndWait()
            engine.setProperty('rate', random.randint(130, 170))
            engine.setProperty('volume', random.uniform(0.6,1.0)) # Vary volume slightly.
        elif random.random() < 0.03:
            engine.setProperty('rate', random.randint(100, 200))  # Vary rate
            engine.setProperty('volume', random.uniform(0.6,1.0)) # Vary volume slightly.

    engine.say(" ".join(new_words)) #Join the words and speak it.
    engine.setProperty('rate', 120)  # Reset rate
    engine.setProperty('volume', 1.0) # Reset volume

class Name:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_input(cls):
        while True:
            name = input("Enter your name: ").strip()
            if name:
                return cls(name)
            else:
                print("Invalid input. Please enter your name.")

    def __str__(self):
        return self.name

class MenuItem:
    def __init__(self, name, price, iced_option=False, whipped_cream_option=False):
        self.name = name
        self.price = price
        self.iced_option = iced_option
        self.whipped_cream_option = whipped_cream_option

    def __str__(self):
        return f"{self.name}: R{self.price}"

class Menu:
    def __init__(self, items):
        self.items = items

    def display(self):
        menu_string = "\n".join(str(item) for item in self.items)
        print(f"Here is our menu:\n{menu_string}")
        speak(f"Here is our menu: {menu_string}")

    def get_item(self, order_name):
        for item in self.items:
            if item.name.lower() == order_name.lower():
                return item
        return None

class Order:
    def __init__(self, item, quantity, whipped_cream=False, iced=False):
        self.item = item
        self.quantity = quantity
        self.whipped_cream = whipped_cream
        self.iced = iced

    def get_price(self):
        price = self.item.price
        if self.whipped_cream:
            price += 10  # R10 extra for whipped cream
        if self.iced:
            price += 7  # R7 extra for iced
        return price * self.quantity

def main():
    # Get the user's name
    user = Name.from_input()
    speak(f"Hello {user}! Welcome to the Robot Coffee Shop!", use_random_effects=True)

    # Define the menu
    menu_items = [
        MenuItem("Black Coffee", 20),
        MenuItem("Espresso", 25),
        MenuItem("Latte", 40, iced_option=True, whipped_cream_option=True),
        MenuItem("Cappuccino", 35, whipped_cream_option=True),
        MenuItem("Mocha", 50, iced_option=True, whipped_cream_option=True),
        MenuItem("Americano", 25, iced_option=True),
        MenuItem("Macchiato", 35),
        MenuItem("Iced Coffee", 35, iced_option=True),
        MenuItem("Caramel Frappuccino", 65, iced_option=True, whipped_cream_option=True),
        MenuItem("Chai Latte", 45, iced_option=True),
        MenuItem("Hot Chocolate", 35, whipped_cream_option=True),
    ]
    menu = Menu(menu_items)

    # Display and speak the menu
    menu.display()
    speak(f"{user}, what would you like to order?", use_random_effects=True)

    # Get the order
    while True:
        order_name = input(f"Enter your order: ").strip()
        order = menu.get_item(order_name)
        if order:
            break
        else:
            print(f"Sorry, {user}, we don't have that here.")
            speak(f"Sorry {user}, we don't have that here.", use_random_effects=True)

    # Get the quantity
    while True:
        try:
            quantity_str = input(f"How many {order.name}(s) would you like? ")
            quantity = int(quantity_str)
            if quantity > 0:
                break
            else:
                print("Invalid quantity. Please enter a positive number.")
                speak("Invalid quantity. Please enter a positive number.", use_random_effects=True)
        except ValueError:
            print("Invalid input. Quantity must be a number.")
            speak("Invalid input. Quantity must be a number.", use_random_effects=True)

    # Check for whipped cream
    whipped_cream = False
    if order.whipped_cream_option:
        while True:
            whipped_cream_str = input("Do you want whipped cream? (yes/no)\n").lower().strip()
            if whipped_cream_str in ["yes", "no"]:
                whipped_cream = whipped_cream_str == "yes"
                break
            else:
                print("Invalid input.")
                speak("Invalid input.", use_random_effects=True)

    # Check if iced
    iced = False
    if order.iced_option and order.name != "Iced Coffee":
        while True:
            iced_str = input("Do you want it iced? (yes/no)\n").lower().strip()
            if iced_str in ["yes", "no"]:
                iced = iced_str == "yes"
                break
            else:
                print("Invalid input.")
                speak("Invalid input.", use_random_effects=True)

    # If the order is an Iced Coffee, it's already iced
    if order.name == "Iced Coffee":
        iced = True

    # Create the order
    customer_order = Order(order, quantity, whipped_cream, iced)
    total_price = customer_order.get_price()

    # Print and speak the confirmation
    print(f"\nGreat {user}, your order of {quantity} {order.name}(s) will be ready in a moment.")
    speak(f"Great {user}, your order of {quantity} {order.name}s will be ready in a moment.", use_random_effects=True)

    # Display if whipped cream or iced
    if whipped_cream:
        print(f"with whipped cream")
        speak("with whipped cream", use_random_effects=True)
    if iced and order.name != "Iced Coffee":
        print("Iced")
        speak("Iced", use_random_effects=True)
    elif iced and order.name == "Iced Coffee":
        print("It's an iced coffee")
        speak("It's an iced coffee", use_random_effects=True)

    print(f"Your total will be: R{total_price}")
    speak(f"Your total will be {total_price}", use_random_effects=True)

if __name__ == "__main__":
    main()
    print("test")