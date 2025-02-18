# import openai
# import random

# def generate_image_exercise(client, word):
#     """Generates an image and multiple-choice question for Sanskrit learning."""
#     try:
#         response = client.images.generate(
#             model="dall-e-2",
#             prompt=f"Generate a simple image of {word} in a clear, educational style.",
#             size="512x512",
#             quality="standard",
#             n=1
#         )

#         image_url = response.data[0].url
        

#         completion = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a Sanskrit teacher."},
#                 {"role": "user", "content": f"Generate four Sanskrit words for {word}, mark the correct one with an asterisk (*)."}
#             ],
#             temperature=1.2
#         )

#         response_text = completion.choices[0].message.content

#         options = [line.strip() for line in response_text.split("\n") if line.strip()]
#         options = [opt.split('. ')[1] for opt in options if '. ' in opt]
#         correct_answer = next(opt for opt in options if "*" in opt).replace("*", "")

#         random.shuffle(options)
#         print(image_url, options, correct_answer)

#         return image_url, options, correct_answer

#     except Exception as e:
#         return None, ["Error generating options"], "Error"


from flask import Flask, request, jsonify
from openai import OpenAI
import random

app = Flask(__name__)
client = OpenAI()

VOCABULARY = {
    'Nature': ["Sun", "Moon", "Star", "Cloud", "Rain", "Tree", "Mountain", "River", "Ocean", "Flower"],
    'Animals': ["Dog", "Cat", "Bird", "Fish", "Elephant", "Tiger", "Lion", "Monkey", "Rabbit"],
    'Body Parts': ["Eye", "Ear", "Nose", "Mouth", "Hand", "Foot", "Hair", "Teeth", "Tongue"],
    'Common Objects': ["Chair", "Table", "Bed", "Cup", "Plate", "Spoon", "Knife", "Bottle", "Clock", "Pen"],
    'Food & Drink': ["Apple", "Banana", "Orange", "Bread", "Rice", "Milk", "Water", "Egg", "Cake", "Ice Cream"],
    'People & Relationships': ["Man", "Woman", "Child", "Baby", "Mother", "Father", "Friend", "Family", "Boy", "Girl"]
}
used_words = []

def get_new_word():
    all_words = [word for category in VOCABULARY.values() for word in category]
    available_words = [word for word in all_words if word not in used_words]
    new_word = random.choice(available_words) if available_words else None
    if new_word:
        used_words.append(new_word)
    return new_word

def generate_image(word):
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=f"A clear, simple depiction of {word}",
            size="512x512",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        return str(e)

def generate_options(word):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Sanskrit teacher."},
                {"role": "user", "content": f"Generate 4 Sanskrit words with transliterations. One must be for '{word}'. Mark the correct answer with an asterisk (*)."}
            ],
            temperature=1.2
        )
        response = completion.choices[0].message.content
        
        completion_1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Format Sanskrit translations into numbered options."},
                {"role": "user", "content": f"Format these words into 4 numbered options: {response}. Mark the correct one inside <ANSWER> tags."}
            ],
            temperature=0.3
        )
        
        response_text = completion_1.choices[0].message.content
        options = [line.split('. ')[1] for line in response_text.split('\n') if line.strip() and not line.startswith('<ANSWER>')]
        correct_answer = response_text.split('<ANSWER>')[1].split('</ANSWER>')[0].strip()
        random.shuffle(options)
        return options, correct_answer
    except Exception as e:
        return ["Option 1", "Option 2", "Option 3", "Option 4"], "Option 1"

@app.route("/image-learning", methods=["GET"])
def image_learning_api():
    word = get_new_word()
    if not word:
        return jsonify({"error": "No new words available."})
    image_url = generate_image(word)
    options, correct_answer = generate_options(word)
    return jsonify({"word": word, "image_url": image_url, "options": options, "correct_answer": correct_answer})

if __name__ == "__main__":
    app.run(debug=True)
