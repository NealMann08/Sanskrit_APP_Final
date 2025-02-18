from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()
used_words = []

def generate_translation_exercise():
    used_words_str = ", ".join(used_words)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Sanskrit teacher."},
            {
                "role": "user",
                "content": f"""Generate one Sanskrit word, its transliteration, and the English translation using one word.
                The word should NOT be any of these previously used words: [{used_words_str}].
                Print in this format: Word - Transliteration - Translation"""
            }
        ],
        temperature=1.2
    )
    response = completion.choices[0].message.content.strip()
    
    completion_1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Sanskrit teacher. Format your responses clearly."},
            {
                "role": "user",
                "content": f"""
                Using this Sanskrit word data: {response}
                Create an exercise in this format:
                
                <EXERCISE>
                Instructions: Translate this Sanskrit word into English.
                Sanskrit Word: [Word] ([Transliteration])
                </EXERCISE>
                
                <ANSWER>
                [Translation]
                </ANSWER>
                """
            }
        ],
        temperature=0.7
    )
    response_1 = completion_1.choices[0].message.content.strip()
    
    exercise = response_1.split('<EXERCISE>')[1].split('</EXERCISE>')[0].strip()
    answer = response_1.split('<ANSWER>')[1].split('</ANSWER>')[0].strip()
    
    used_words.append(response)
    
    return {"exercise": exercise, "correct_answer": answer}

@app.route("/translation", methods=["GET"])
def translation_exercise_api():
    result = generate_translation_exercise()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
