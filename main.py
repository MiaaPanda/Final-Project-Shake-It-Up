import json
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

BASE_API_URL = "https://www.thecocktaildb.com/api/json/v1/1/"

all_cocktails = []  # Define all_cocktails as a global list to store cocktails
def search_cocktails_by_ingredient(ingredient):
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
    # Construct the URL to retrieve details of a specific cocktail by its ID
    cocktail_url = BASE_API_URL + "lookup.php?i=" + cocktail_id
    response = requests.get(cocktail_url)
    data = response.json()
    return data["drinks"][0]

def display_cocktail_details():
    selected_index = result_text.curselection()
    if selected_index:
        selected_cocktail_name = result_text.get(selected_index)
        # Find the selected cocktail ID based on its name
        for cocktail in all_cocktails:
            if cocktail["strDrink"] == selected_cocktail_name:
                selected_cocktail_id = cocktail["idDrink"]
                break
        cocktail_details = search_cocktail_details(selected_cocktail_id)
        if cocktail_details:
            # Display ingredients, instructions, and image
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
                image_label.image = photo  # Keep a reference to the image to avoid garbage collection
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
    global all_cocktails  # Declare all_cocktails as a global variable
    ingredient1 = ingredient1_entry.get()
    ingredient2 = ingredient2_entry.get()
    all_cocktails.clear()
    cocktails1 = search_cocktails_by_ingredient(ingredient1)
    cocktails2 = search_cocktails_by_ingredient(ingredient2)
    if not cocktails1 and not cocktails2:
        result_text.delete(0, tk.END)
        result_text.insert(tk.END, "No cocktails found for the given ingredients.")
        return
    # Intersect the results to get cocktails that contain both ingredients
    cocktails1_ids = set(cocktail["idDrink"] for cocktail in cocktails1)
    cocktails2_ids = set(cocktail["idDrink"] for cocktail in cocktails2)
    common_ids = cocktails1_ids.intersection(cocktails2_ids)
    all_cocktails.extend(cocktail for cocktail in cocktails1 if cocktail["idDrink"] in common_ids)
    if all_cocktails:
        result_text.delete(0, tk.END)
        for cocktail in all_cocktails:
            result_text.insert(tk.END, cocktail["strDrink"])
    else:
        result_text.delete(0, tk.END)
        result_text.insert(tk.END, "No cocktails found")


window = tk.Tk()
window.title("Cocktail Search")
window.iconbitmap('cocktail.ico')
window.configure(bg='light blue')

# Create a frame for the search section
search_frame = tk.Frame(window)
search_frame.grid(row=0, column=0, columnspan=2)

# Create labels and entry widgets for entering ingredients
ingredient1_label = tk.Label(search_frame, text="Ingredient 1:")
ingredient1_label.pack(side=tk.LEFT)
ingredient1_entry = tk.Entry(search_frame)
ingredient1_entry.pack(side=tk.LEFT)

ingredient2_label = tk.Label(search_frame, text="Ingredient 2:")
ingredient2_label.pack(side=tk.LEFT)
ingredient2_entry = tk.Entry(search_frame)
ingredient2_entry.pack(side=tk.LEFT)

# Create a search button
search_button = tk.Button(search_frame, text="Search Cocktails", command=search_cocktails)
search_button.pack(side=tk.LEFT)

# Create a listbox to display the results
result_text = tk.Listbox(window, width=40, height=10)
result_text.grid(row=1, column=0, padx=10, pady=10)

# Open the image file
img = Image.open('button.ico')
# Resize the image if necessary
img = img.resize((50, 50), Image.LANCZOS)
# Convert the image to a PhotoImage
photo = ImageTk.PhotoImage(img)

# Now you can use 'photo' to set the image of the button
display_button = tk.Button(window, text="Display Details", command=display_cocktail_details, image=photo, compound=tk.LEFT)
display_button.grid(row=2, column=0, padx=10, pady=10)  # Change column to 0

# Create labels for displaying cocktail details
ingredients_text = tk.Text(window, width=40, height=10)
ingredients_text.grid(row=1, column=1, padx=10, pady=10)

instructions_text = tk.Text(window, width=40, height=10)
instructions_text.grid(row=2, column=1, padx=10, pady=10)

# Create an image label
image_label = tk.Label(window, text="Image:")
image_label.grid(row=1, column=2, rowspan=2)  # Change column to 2

window.mainloop()

