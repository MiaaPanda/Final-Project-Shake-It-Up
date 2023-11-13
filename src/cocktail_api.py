import json
import requests

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
