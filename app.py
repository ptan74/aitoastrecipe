# this is a test for different preparation of food
# Author:  Patrick Tan
# contact: patrick.patricktan@gmail.com
# This will generate a recipe for the selected category and ingredients using GPT-2 model


from flask import Flask, render_template, request
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import textwrap

app = Flask(__name__)

# Load pre-trained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Recipe categories
recipe_categories = [
    "Biscuit",
    "Cake",
    "French Toast",
    "Cookies",
    "Drink",
    "Drinks Powder",
    "Baking Flour",
    "Bread",
    "Croissant",
    "Crusty Hard Rolls"
]


# Flask route for the home page
@app.route('/')
def index():
    return render_template('index_with_ai.html', recipe_categories=recipe_categories)


# Flask route to handle form submission
@app.route('/generate_recipe', methods=['POST'])
def generate_recipe_route():
    selected_category = request.form['recipe_category']
    ingredients = request.form['ingredients']

    prompt = f"Recipe for {selected_category} with ingredients: {ingredients}"
    input_ids = tokenizer.encode(prompt, return_tensors="pt", max_length=100, truncation=True)
    output = model.generate(input_ids, max_length=200, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95,
                            temperature=0.7)

    generated_recipe = tokenizer.decode(output[0], skip_special_tokens=True)

    # Split the generated recipe into rows of 25 words each
    wrapped_recipe = textwrap.fill(generated_recipe, width=25)

    return render_template('recipe_with_ai.html', generated_recipe=wrapped_recipe, selected_category=selected_category)


if __name__ == '__main__':
    app.run(debug=True)


