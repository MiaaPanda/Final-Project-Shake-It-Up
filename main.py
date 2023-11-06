import json
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

BASE_API_URL = "https://www.thecocktaildb.com/api/json/v1/1/"
all_cocktails = []

def search_cocktails_by_ingredient(ingredient):
    print(f"Searching cocktails with ingredient: {ingredient}")
    search_url = BASE_API_URL + "filter.php?i=" + ingredient
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

def search_cocktail_details(cocktail_id):
    print(f"Fetching details for cocktail ID: {cocktail_id}")
    cocktail_url = BASE_API_URL + "lookup.php?i=" + cocktail_id
    response = requests.get(cocktail_url)
    data = response.json()
    return data["drinks"][0]

def display_cocktail_details():
    print("Displaying cocktail details  ")
    selected_index = result_text.curselection()
    if selected_index:
        selected_cocktail_name = result_text.get(selected_index)
        for cocktail in all_cocktails:
            if cocktail["strDrink"] == selected_cocktail_name:
                selected_cocktail_id = cocktail["idDrink"]
                break
        cocktail_details = search_cocktail_details(selected_cocktail_id)
        if cocktail_details:
            ingredients_text.delete(1.0, tk.END)
            ingredients_text.insert(tk.END, "Ingredients:\n")
            for i in range(1, 16):
                ingredient = cocktail_details[f"strIngredient{i}"]
                measure = cocktail_details[f"strMeasure{i}"]
                if ingredient:
                    ingredients_text.insert(tk.END, f"{measure} {ingredient}\n")
            instructions_text.delete(1.0, tk.END)
            instructions_text.insert(tk.END, f"Instructions:\n{cocktail_details['strInstructions']}\n")
            image_url = cocktail_details['strDrinkThumb']
            image_label.config(text="Image:")
            try:
                image_data = requests.get(image_url).content
                image = Image.open(BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)
                image_label.config(image=photo)
                image_label.image = photo
            except Exception as e:
                print(f"Failed to load the image: {e}")
        else:
            ingredients_text.delete(1.0, tk.END)
            instructions_text.delete(1.0, tk.END)
            image_label.config(text="Image:")
    else:
        ingredients_text.delete(1.0, tk.END)
        instructions_text.delete(1.0, tk.END)
        image_label.config(text="Image:")

def search_cocktails():
    print("Searching cocktails")
    global all_cocktails
    ingredient1 = ingredient1_entry.get()
    all_cocktails.clear()
    cocktails1 = search_cocktails_by_ingredient(ingredient1)
    if not cocktails1:
        result_text.delete(0, tk.END)
        result_text.insert(tk.END, "No cocktails found")
        return
    all_cocktails.extend(cocktail for cocktail in cocktails1)
    if all_cocktails:
        result_text.delete(0, tk.END)
        for cocktail in all_cocktails:
            result_text.insert(tk.END, cocktail["strDrink"])
    else:
        result_text.delete(0, tk.END)
        result_text.insert(tk.END, "No cocktails found")

    ingredient2 = ingredient2_entry.get()
    if ingredient2:
        cocktails2 = search_cocktails_by_ingredient(ingredient2)
        if not cocktails2:
            return
        cocktails1_ids = set(cocktail["idDrink"] for cocktail in cocktails1)
        cocktails2_ids = set(cocktail["idDrink"] for cocktail in cocktails2)
        common_ids = cocktails1_ids.intersection(cocktails2_ids)
        all_cocktails.clear()
        all_cocktails.extend(cocktail for cocktail in cocktails1 if cocktail["idDrink"] in common_ids)
        if all_cocktails:
            result_text.delete(0, tk.END)
            for cocktail in all_cocktails:
               result_text.insert(tk.END, cocktail["strDrink"])
        else:
            result_text.delete(0, tk.END)
            result_text.insert(tk.END, "No common cocktails found")

window = tk.Tk()
window.title("Cocktail Search")
window.iconbitmap('cocktail.ico')
window.configure(bg='light blue')

search_frame = tk.Frame(window)
search_frame.grid(row=0, column=0, columnspan=2)

ingredient1_label = tk.Label(search_frame, text="Ingredient 1:")
ingredient1_label.pack(side=tk.LEFT)
ingredient1_entry = tk.Entry(search_frame)
ingredient1_entry.pack(side=tk.LEFT)

ingredient2_label = tk.Label(search_frame, text="Ingredient 2:")
ingredient2_label.pack(side=tk.LEFT)
ingredient2_entry = tk.Entry(search_frame)
ingredient2_entry.pack(side=tk.LEFT)

search_button = tk.Button(search_frame, text="Search Cocktails", command=search_cocktails)
search_button.pack(side=tk.LEFT)

result_text = tk.Listbox(window, width=40, height=10)
result_text.grid(row=1, column=0, padx=10, pady=10)

img = Image.open('button.ico')
img = img.resize((50, 50), Image.LANCZOS)

photo = ImageTk.PhotoImage(img)

display_button = tk.Button(window, text="Display Details", command=display_cocktail_details, image=photo, compound=tk.LEFT)
display_button.grid(row=2, column=0, padx=10, pady=10)

ingredients_text = tk.Text(window, width=40, height=10)
ingredients_text.grid(row=1, column=1, padx=10, pady=10)

instructions_text = tk.Text(window, width=40, height=10)
instructions_text.grid(row=2, column=1, padx=10, pady=10)

image_label = tk.Label(window, text="Image:")
image_label.grid(row=1, column=2, rowspan=2)

window.mainloop()
