import argparse

from flask import Flask
from flask import render_template
from shaney import train3 as train
from shaney import generate3 as generate


global LIMIT  # Limit the number of words displayed.
app = Flask(__name__)
shaney_bot = None


class Shaney:
    def __init__(self, file):
        self.data = train(file)

    def quote(self):
        try:
            quotes = generate(self.data, count=1, verbose=False)
            quote = quotes[0].strip()
        except:
            quote = "oops. I failed to generate a quote. Try again?"
        return quote


@app.route('/')
def hello_world():
    if shaney_bot:
        quote = shaney_bot.quote()
    else:
        quote = "oops."

    if LIMIT:  # limit the number of words in the quote
        words = quote.split()
        while len(words) > LIMIT:
            words = words[:-1]
        quote = " ".join(words)
    return render_template('index.html', quote=quote)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Path to the training text.", type=str)
    parser.add_argument(
        "-l",
        "--limit",
        help="Number of words to display",
        type=int,
        default=None
    )
    args = parser.parse_args()

    LIMIT = args.limit
    shaney_bot = Shaney(args.filename)
    app.run()
