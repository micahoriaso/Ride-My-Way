from flask import Flask, render_template

# Create the appliction instance
app = Flask(__name__, template_folder='../UI')

# Create a URL route in our application for "/""

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
