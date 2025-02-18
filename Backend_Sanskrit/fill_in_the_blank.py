from flask import Flask, request, jsonify
from openai import OpenAI
import random

app = Flask(__name__)
client = OpenAI()

used_sentences = []

def generate_fill_in_the_blank():
    used_sentence_str = ", ".join(used_sentences)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Sanskrit teacher."},
            {
                "role": "user",
                "content": f"""Generate one beginner-level fill-in-the-blank Sanskrit exercise.
                The exercise should not be any of the following sentences: [{used_sentence_str}].
                Do not provide the English translation at all.
                Use this structure and replace the [Verb] or [Object] with a blank:
                Sentence: [Subject] + [Verb] + [Object]
                Answer choices:
                1. [Option 1]
                2. [Option 2]
                3. [Option 3]
                Correct answer: [Correct option]
                """
            }
        ],
        temperature=1.2
    )
    response = completion.choices[0].message.content

    completion_1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Sanskrit teacher. Format responses cleanly."},
            {
                "role": "user",
                "content": f"""
                Use this Sanskrit fill-in-the-blank exercise: {response}
                
                Format as:
                <EXERCISE>
                Instructions: Identify which option best completes this sentence:
                Sanskrit Sentence: [Sentence with ___ for blank]
                Options:
                # 1. [Option 1]
                # 2. [Option 2]
                # 3. [Option 3]
                </EXERCISE>
                
                <ANSWER>
                [Correct Option Number]
                </ANSWER>
                """
            }
        ],
        temperature=0.7
    )
    response_1 = completion_1.choices[0].message.content
    
    exercise = response_1.split("<EXERCISE>")[1].split("</EXERCISE>")[0].strip()
    correct_answer = response_1.split("<ANSWER>")[1].split("</ANSWER>")[0].strip()
    
    used_sentences.append(exercise)
    
    return {"exercise": exercise, "correct_answer": correct_answer}

@app.route("/fill-in-the-blank", methods=["GET"])
def fill_in_the_blank_api():
    result = generate_fill_in_the_blank()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
