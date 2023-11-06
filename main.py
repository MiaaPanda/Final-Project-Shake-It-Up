import json
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class CocktailAPI:
    BASE_API_URL = "https://www.thecocktaildb.com/api/json/v1/1/"

    def search_cocktails_by_ingredient(self, ingredient):
        print(f"Searching cocktails with ingredient: {ingredient}")
        search_url = self.BASE_API_URL + "filter.php?i=" + ingredient
        response = requests.get(search_url)
        try:
            data = response.json()
            if "drinks" in data:
                return data["drinks"]
            else:
                return []
        except json.JSONDecodeError:
            print(f"Failed to decode JSON response for ingredient {ingredient}")
            return []

    def search_cocktail_details(self, cocktail_id):
        print(f"Fetching details for cocktail ID: {cocktail_id}")
        cocktail_url = self.BASE_API_URL + "lookup.php?i=" + cocktail_id
        response = requests.get(cocktail_url)
        data = response.json()
        return data["drinks"][0]

class CocktailApp:
    def __init__(self):
        self.api = CocktailAPI()
        self.all_cocktails = []
        self.setup_gui()

    def display_cocktail_details(self):
        print("Displaying cocktail details")
        selected_index = self.result_text.curselection()
        if selected_index:
            selected_cocktail_name = self.result_text.get(selected_index)
            for cocktail in self.all_cocktails:
                if cocktail["strDrink"] == selected_cocktail_name:
                    selected_cocktail_id = cocktail["idDrink"]
                    break
            cocktail_details = self.api.search_cocktail_details(selected_cocktail_id)
            if cocktail_details:
                self.ingredients_text.delete(1.0, tk.END)
                self.ingredients_text.insert(tk.END, "Ingredients:\n")
                for i in range(1, 16):
                    ingredient = cocktail_details[f"strIngredient{i}"]
                    measure = cocktail_details[f"strMeasure{i}"]
                    if ingredient:
                        self.ingredients_text.insert(tk.END, f"{measure} {ingredient}\n")
                self.instructions_text.delete(1.0, tk.END)
                self.instructions_text.insert(tk.END, f"Instructions:\n{cocktail_details['strInstructions']}\n")
                image_url = cocktail_details['strDrinkThumb']
                self.image_label.config(text="Image:")
                try:
                    image_data = requests.get(image_url).content
                    image = Image.open(BytesIO(image_data))
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
                except Exception as e:
                    print(f"Failed to load the image: {e}")
            else:
                self.ingredients_text.delete(1.0, tk.END)
                self.instructions_text.delete(1.0, tk.END)
                self.image_label.config(text="Image:")
        else:
            self.ingredients_text.delete(1.0, tk.END)
            self.instructions_text.delete(1.0, tk.END)
            self.image_label.config(text="Image:")

    def search_cocktails(self):
        print("Searching cocktails")
        global all_cocktails
        ingredient1 = self.ingredient1_entry.get()
        self.all_cocktails.clear()
        cocktails1 = self.api.search_cocktails_by_ingredient(ingredient1)
        if not cocktails1:
            self.result_text.delete(0, tk.END)
            self.result_text.insert(tk.END, "No cocktails found")
            return
        self.all_cocktails.extend(cocktail for cocktail in cocktails1)
        if self.all_cocktails:
            self.result_text.delete(0, tk.END)
            for cocktail in self.all_cocktails:
                self.result_text.insert(tk.END, cocktail["strDrink"])
        else:
            self.result_text.delete(0, tk.END)
            self.result_text.insert(tk.END, "No cocktails found")
        ingredient2 = self.ingredient2_entry.get()
        if ingredient2:
            cocktails2 = self.api.search_cocktails_by_ingredient(ingredient2)
            if not cocktails2:
                return
            cocktails1_ids = set(cocktail["idDrink"] for cocktail in cocktails1)
            cocktails2_ids = set(cocktail["idDrink"] for cocktail in cocktails2)
            common_ids = cocktails1_ids.intersection(cocktails2_ids)
            self.all_cocktails.clear()
            self.all_cocktails.extend(cocktail for cocktail in cocktails1 if cocktail["idDrink"] in common_ids)
            if self.all_cocktails:
                self.result_text.delete(0, tk.END)
                for cocktail in self.all_cocktails:
                   self.result_text.insert(tk.END, cocktail["strDrink"])
            else:
                self.result_text.delete(0, tk.END)
                self.result_text.insert(tk.END, "No cocktails found")

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.title("Cocktail Search")
        self.window.iconbitmap('cocktail.ico')
        self.window.configure(bg='light blue')

        self.search_frame = tk.Frame(self.window)
        self.search_frame.grid(row=0, column=0, columnspan=2)

        self.ingredient1_label = tk.Label(self.search_frame, text="Ingredient 1:")
        self.ingredient1_label.pack(side=tk.LEFT)
        self.ingredient1_entry = tk.Entry(self.search_frame)
        self.ingredient1_entry.pack(side=tk.LEFT)

        self.ingredient2_label = tk.Label(self.search_frame, text="Ingredient 2:")
        self.ingredient2_label.pack(side=tk.LEFT)
        self.ingredient2_entry = tk.Entry(self.search_frame)
        self.ingredient2_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.search_frame, text="Search Cocktails", command=self.search_cocktails)
        self.search_button.pack(side=tk.LEFT)

        self.result_text = tk.Listbox(self.window, width=40, height=10)
        self.result_text.grid(row=1, column=0, padx=10, pady=10)

        self.img = Image.open('button.ico')
        self.img = self.img.resize((50, 50), Image.LANCZOS)

        self.photo = ImageTk.PhotoImage(self.img)

        self.display_button = tk.Button(self.window, text="Display Details", command=self.display_cocktail_details, image=self.photo, compound=tk.LEFT)
        self.display_button.grid(row=2, column=0, padx=10, pady=10)

        self.ingredients_text = tk.Text(self.window, width=40, height=10)
        self.ingredients_text.grid(row=1, column=1, padx=10, pady=10)

        self.instructions_text = tk.Text(self.window, width=40, height=10)
        self.instructions_text.grid(row=2, column=1, padx=10, pady=10)

        self.image_label = tk.Label(self.window, text="Image:")
        self.image_label.grid(row=1, column=2, rowspan=2)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CocktailApp()
    app.run()
