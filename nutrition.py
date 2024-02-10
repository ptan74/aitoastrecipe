# A simple nutrition calculator using the CalorieNinjas API
# Author: Patrick Tan
# contact: patrick.patricktan@gmail.com


import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

def calculate_nutrition():
    query = query_text.get("1.0", "end-1c")
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query=' + query
    response = requests.get(api_url, headers={'X-Api-Key': 'replace with your own key from https://calorieninjas.com/api'})

    if response.status_code == requests.codes.ok:
        nutrition_data = response.json()["items"]
        formatted_result = format_nutrition_result(nutrition_data)
        show_result_popup(formatted_result)
    else:
        error_message = f"Error: {response.status_code}\n{response.text}"
        show_result_popup(error_message)

def format_nutrition_result(nutrition_data):
    formatted_result = ""
    for item in nutrition_data:
        formatted_result += (
            f"Name: {item['name']}\n"
            f"Calories: {item['calories']}\n"
            f"Fat (g): {item['fat_total_g']}\n"
            f"Carbs (g): {item['carbohydrates_total_g']}\n"
            f"Protein (g): {item['protein_g']}\n\n"
        )
    return formatted_result

def show_result_popup(result):
    popup = tk.Toplevel(root)
    popup.title("Nutrition Result")

    result_text = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=40, height=10)
    result_text.insert(tk.END, result)
    result_text.pack(expand=True, fill="both", pady=10)

# Create Tkinter window
root = tk.Tk()
root.title("Nutrition Calculator")

# Create text area for query input
query_text = tk.Text(root, height=5, width=40)
query_text.pack(pady=10)

# Create button to calculate nutrition
calculate_button = tk.Button(root, text="Calculate Nutrition", command=calculate_nutrition)
calculate_button.pack()

# Start Tkinter event loop
root.mainloop()
