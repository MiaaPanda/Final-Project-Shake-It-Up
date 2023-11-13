
![Architecture_Diagram](C:\Users\Tetragammon\PycharmProjects\pythonProject3\Shake_It_Up\Architecture_Diagram.PNG)

Architecture Diagram:
The program has two main classes:
1.	CocktailAPI Class: This class handles interactions with the CocktailDB API. It has methods to search for cocktails by ingredient and fetch detailed information about a specific cocktail.
2.	CocktailApp Class: This class is responsible for the GUI and overall application flow. It initializes the CocktailAPI, sets up the GUI using Tkinter, and defines methods to search for cocktails and display their details.
   	Attributes:
   •	api: An instance of the CocktailAPI class.
   •	all_cocktails: A list to store information about all the fetched cocktails.
   	Methods:
   •	setup_gui: Sets up the Tkinter GUI with labels, entry fields, buttons, and text areas.
   •	search_cocktails: Handles the logic for searching and displaying cocktails based on user input.
   •	display_cocktail_details: Fetches and displays detailed information about a selected cocktail.
3.	Main Execution:
   •	The program starts by creating an instance of the CocktailApp class.
   •	It then calls the run method to start the Tkinter main loop, allowing the GUI to run.
4.	External Libraries:
   •	The program uses the requests, json, tkinter, PIL, and io modules for API requests, JSON decoding, GUI development, image handling, and file I/O, respectively.


![Flow Diagram](C:\Users\Tetragammon\PycharmProjects\pythonProject3\Shake_It_Up\FlowDiagram.png)

Flow Diagram:
1.	Start: The program starts when you execute it.
2.	User Input: The user enters ingredient names in the GUI.
3.	Search Cocktails Button Pressed: When the user clicks the "Search Cocktails" button, it triggers the search_cocktails method.
4.	API Interaction: The search_cocktails method interacts with the CocktailAPI class to search for cocktails based on the entered ingredients.
5.	Display Results: The results are displayed in the GUI in the result_text Listbox.
6.	Display Details Button Pressed: If the user clicks the "Display Details" button, it triggers the display_cocktail_details method.
7.	Fetch Cocktail Details: The display_cocktail_details method fetches detailed information about the selected cocktail using the CocktailAPI.
8.	Display Details: The detailed information is displayed in the GUI in the ingredients_text, instructions_text, and image_label.
9.	End: The program ends when the user closes the GUI.