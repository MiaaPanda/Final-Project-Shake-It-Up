https://github.com/MiaaPanda/pythonProject3/blob/master/Shake_It_Up/Arhitecture%20Diagram%20.jpg
![Arhitecture Diagram.jpg](..%2F..%2F..%2FDesktop%2FArhitecture%20Diagram.jpg)
Flow Diagram
1. Start
2. Setup Tkinter GUI: Create window, frames, labels, buttons and entry fields.
3. Input Ingredients: User inputs ingredients into the entry fields.
4. Search Cocktails: On clicking the "Search Cocktails" button, the search_cocktail function is called.
        - print "Searching cocktails"
        - Get the ingredient from the entry field
        - Call search_cocktails_by_ingredient function for each ingredient:
            * Print "Searching Cocktails with ingredient: {ingredient}"
            * Construct the API URL with the ingredient
            * Send API request to get cocktails with the given ingredient.
            * Receive API response and decode the JSON data.
            * If "drinks" are present in the data, return the list of drinks.
            * If an error occurs during JSON decoding, print an error message and return an empty list.
        - Display the list of cocktails in the result text box or display "No cocktails found" if the list ist empty.
5. Select Cocktail: User selects a cocktail from the list.
6. Display Cocktail Details: On clicking the "Display Details" button, the display_cocktail_details function is called:
         - Print "Displaying cocktail details".
         - Get the selected cocktail name from the list box.
         - Find the ID of the selected cocktail.
         - Call search_cocktail_details function with the ID of the selected cocktail:
            * Print "Fetching details for cocktail ID: {cocktail_id}
            * Construct the API URL with the cocktail ID
            * Send API request to get details of the selected cocktail
            * Receive API responde and decode JSON data.
            * Return the details of the cocktail.
         - Display the cocktail details (ingredients, instructions, image) in the respective fields.
7. End 

https://github.com/MiaaPanda/pythonProject3/blob/master/Shake_It_Up/FlowDiagram.JPG
