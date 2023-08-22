import openai
import json
import os
from dotenv import load_dotenv
import os

load_dotenv(".env")

openai.api_key = os.getenv("OPENAI_API_KEY")


from flask import Flask, render_template, request

app = Flask(
    __name__,
    template_folder="templates",
    static_url_path="",
    static_folder="static",
)


def get_colors(msg):
    messages = [
        {
            "role": "system",
            "content": "You are a color palette, generating assistant, that responds to text prompts for color palette. You should generate color palettes that fit, the theme, mood, or instructions in the prompt. The palettes should be between two and eight colors.",
        },
        {
            "role": "user",
            "content": "Convert the following verbal description of a color palette into a list of color: a beautiful sunset",
        },
        {
            "role": "system",
            "content": '[ "#752920", "#D1AC54", "#E4A133", "#F6B554", "#F8D9AB"]',
        },
        {
            "role": "user",
            "content": "Convert the following verbal description of a color palette into a list of color: The Mediterranean Sea",
        },
        {
            "role": "system",
            "content": '["#006A93", "#00A59F", "#8CD3BF", "#FFF7D6", "#E4A548", "#BF7532"]',
        },
        {
            "role": "user",
            "content": f"Convert the following verbal description of a color palette into a list of color: {msg}",
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
    )

    colors = json.loads(response["choices"][0]["message"]["content"])

    return colors


@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    # app.logger.info("Request received")
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
