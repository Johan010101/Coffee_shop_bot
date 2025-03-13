import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import pyttsx3
import random
import time

def speak(text, rate=140, use_random_effects=True, volume=1.0):
    """Speaks the given text with enhanced random effects."""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    if use_random_effects:
        apply_random_effects(engine, text)
    else:
        engine.say(text)

    engine.runAndWait()
    engine.stop()

def apply_random_effects(engine, text):
    """Applies a wider range of random speech effects to the text."""
    words = text.split()
    new_words = []
    for i, word in enumerate(words):
        new_words.append(word)

        # Pause after punctuation
        if word.endswith(('.', ',', '!', '?')) and random.random() < 0.5:
          time.sleep(random.uniform(0.3, 0.6))

        # Random interjection
        if random.random() < 0.1:  # 10% chance
            interjection = random.choice(["uh", "um", "err", "like", "you know", "well"])
            new_words.append(interjection)

        # Pitch variation
        if random.random() < 0.05:
            current_rate = engine.getProperty('rate')
            engine.setProperty('rate', random.uniform(current_rate - 15, current_rate + 15))

        # Volume Variation
        if random.random() < 0.05:
            engine.setProperty('volume', random.uniform(0.7, 1.0))

        # Word emphasis
        if random.random() < 0.03:  # 3% chance
            current_volume = engine.getProperty('volume')
            engine.setProperty('volume', random.uniform(1.0, 1.3))
            engine.say(word)
            engine.runAndWait()
            engine.setProperty('volume', current_volume)

        # Reset rate before the next word
        engine.setProperty('rate', 140)

    engine.say(" ".join(new_words))
    engine.runAndWait()
    engine.setProperty('rate', 140)  # Reset rate
    engine.setProperty('volume', 1.0) # Reset volume

class Name:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_input(cls, master):
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
        speak(f"Here is our menu: {menu_string}")
        return menu_string

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

class CoffeeShopGUI:
    def __init__(self, master):
        self.master = master
        master.title("Robot Coffee Shop")

        # --- Styling ---
        self.master.configure(bg="#e8d4b6")  # Light beige background
        self.customFont = tkFont.Font(family="Helvetica", size=12)
        self.buttonFont = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.labelFont = tkFont.Font(family="Helvetica", size=14)

        style = ttk.Style()
        style.configure("TButton", font=self.buttonFont, background="#a57a53", foreground="white", padding=10) # Brown Buttons
        style.map("TButton", background=[("active", "#87654a")])  # Darker brown on hover

        # --- Welcome Frame ---
        self.welcome_frame = tk.Frame(master, bg="#e8d4b6")
        self.welcome_frame.pack(pady=20)

        self.welcome_label = tk.Label(self.welcome_frame, text="Welcome to the Robot Coffee Shop!", font=self.labelFont, bg="#e8d4b6")
        self.welcome_label.pack(pady=(0, 10))

        self.name_label = tk.Label(self.welcome_frame, text="Enter your name:", font=self.customFont, bg="#e8d4b6")
        self.name_label.pack(pady=(0, 5))

        self.name_entry = tk.Entry(self.welcome_frame, font=self.customFont, justify="center")
        self.name_entry.pack(pady=(0, 10), ipadx=5, ipady=5)

        self.continue_button = ttk.Button(self.welcome_frame, text="Continue", command=self.continue_to_menu, style="TButton")
        self.continue_button.pack()

        # --- Menu Frame ---
        self.menu_frame = tk.Frame(master, bg="#e8d4b6")

        # --- Order Frame ---
        self.order_frame = tk.Frame(master, bg="#e8d4b6")

        # --- Confirmation Frame ---
        self.confirmation_frame = tk.Frame(master, bg="#e8d4b6")

        # --- Initialize variables ---
        self.user = None
        self.menu = None
        self.order = None
        self.menu_items = [
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

    def continue_to_menu(self):
        name = self.name_entry.get()
        if name:
            self.user = Name(name)
            speak(f"Hello {self.user}! Welcome to the Robot Coffee Shop!", use_random_effects=True)
            self.welcome_frame.pack_forget() #hide the welcome frame
            self.show_menu()
        else:
            self.name_label.config(text="Please enter a valid name:") #modify the label if the name is invalid.

    def show_menu(self):
        self.menu_frame.pack(pady=20)

        self.menu = Menu(self.menu_items)
        menu_text = self.menu.display()

        self.menu_label = tk.Label(self.menu_frame, text=f"{self.user}, what would you like to order?", font=self.labelFont, bg="#e8d4b6")
        self.menu_label.pack(pady=(0, 10))

        self.menu_display_label = tk.Label(self.menu_frame, text=menu_text, font=self.customFont, bg="#e8d4b6")
        self.menu_display_label.pack(pady=(0, 10))

        self.order_entry = tk.Entry(self.menu_frame, font=self.customFont, justify="center")
        self.order_entry.pack(pady=(0, 10), ipadx=5, ipady=5)

        self.order_button = ttk.Button(self.menu_frame, text="Place Order", command=self.show_order_options, style="TButton")
        self.order_button.pack()

        self.error_label = tk.Label(self.menu_frame, text="", font=self.customFont, fg="red", bg="#e8d4b6")
        self.error_label.pack()

    def show_order_options(self):
        order_name = self.order_entry.get().strip()
        self.order = self.menu.get_item(order_name)
        self.menu_frame.pack_forget() # hide the menu frame
        if self.order:
            self.order_frame.pack(pady=20)
            self.quantity_label = tk.Label(self.order_frame, text=f"How many {self.order.name}(s) would you like?", font=self.labelFont, bg="#e8d4b6")
            self.quantity_label.pack(pady=(0, 10))

            self.quantity_entry = tk.Entry(self.order_frame, font=self.customFont, justify="center")
            self.quantity_entry.pack(pady=(0, 10), ipadx=5, ipady=5)

            self.quantity_button = ttk.Button(self.order_frame, text="Confirm Quantity", command=self.confirm_quantity, style="TButton")
            self.quantity_button.pack()

            self.error_quantity_label = tk.Label(self.order_frame, text="", font=self.customFont, fg="red", bg="#e8d4b6")
            self.error_quantity_label.pack()
        else:
            speak(f"Sorry {self.user}, we don't have that here.", use_random_effects=True)
            self.error_label.config(text=f"Sorry, {self.user}, we don't have that here.")
            self.show_menu()

    def confirm_quantity(self):
        try:
            quantity = int(self.quantity_entry.get())
            if quantity > 0:
                self.order_frame.pack_forget()
                self.handle_options(quantity)
            else:
                self.error_quantity_label.config(text="Invalid quantity. Please enter a positive number.")
                speak("Invalid quantity. Please enter a positive number.", use_random_effects=True)
        except ValueError:
            self.error_quantity_label.config(text="Invalid input. Quantity must be a number.")
            speak("Invalid input. Quantity must be a number.", use_random_effects=True)

    def handle_options(self, quantity):
        self.order.quantity = quantity
        self.whipped_cream_var = tk.BooleanVar()
        self.iced_var = tk.BooleanVar()

        options_frame = tk.Frame(self.confirmation_frame, bg="#e8d4b6")
        options_frame.pack(pady=20)

        if self.order.whipped_cream_option:
          self.whipped_cream_check = tk.Checkbutton(options_frame, text="Whipped Cream", variable=self.whipped_cream_var, font=self.customFont, bg="#e8d4b6")
          self.whipped_cream_check.pack(pady=(0, 10))

        if self.order.iced_option and self.order.name != "Iced Coffee":
            self.iced_check = tk.Checkbutton(options_frame, text="Iced", variable=self.iced_var, font=self.customFont, bg="#e8d4b6")
            self.iced_check.pack(pady=(0, 10))

        self.confirm_order_button = ttk.Button(options_frame, text="Confirm Order", command=self.confirm_order, style="TButton")
        self.confirm_order_button.pack()

        self.confirmation_frame.pack(pady=20)

    def confirm_order(self):
        whipped_cream = self.whipped_cream_var.get() if hasattr(self, 'whipped_cream_var') else False
        iced = self.iced_var.get() if hasattr(self, 'iced_var') else False
        # If the order is an Iced Coffee, it's already iced
        if self.order.name == "Iced Coffee":
            iced = True

        customer_order = Order(self.order, self.order.quantity, whipped_cream, iced)
        total_price = customer_order.get_price()

        confirmation_text = f"\nGreat {self.user}, your order of {self.order.quantity} {self.order.name}(s) will be ready in a moment.\n"

        speak(f"Great {self.user}, your order of {self.order.quantity} {self.order.name}s will be ready in a moment.", use_random_effects=True)

        if whipped_cream:
            confirmation_text += "with whipped cream\n"
            speak("with whipped cream", use_random_effects=True)
        if iced and self.order.name != "Iced Coffee":
            confirmation_text += "Iced\n"
            speak("Iced", use_random_effects=True)
        elif iced and self.order.name == "Iced Coffee":
            confirmation_text += "It's an iced coffee\n"
            speak("It's an iced coffee", use_random_effects=True)

        confirmation_text += f"Your total will be: R{total_price}"
        speak(f"Your total will be {total_price}", use_random_effects=True)

        self.confirmation_frame.pack_forget()
        confirmation_label = tk.Label(self.master, text=confirmation_text, font=self.customFont, bg="#e8d4b6")
        confirmation_label.pack(pady=20)



def main():
    root = tk.Tk()
    CoffeeShopGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()