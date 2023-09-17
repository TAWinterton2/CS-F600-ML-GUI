from flask import Flask, render_template, request
from markupsafe import escape

# Name of the module initializing / running the program
app = Flask(__name__)

@app.route("/")
def index():
    """ Displays the index page at url '/' """

    return render_template('index.html')


# Route can also be used to bind a function to a URL.
# If a user wishes to view this webpage at this url, they will see this text.
@app.route("/hello")
def hello():
    """ Route for a simple 'Hello, World' message."""
    return "Hello, World"


# If the user is providing text input, it needs to be escaped to prevent injection attacks.
@app.route("/<name>")
def name(name):
    """ Route for a simple 'Hello, <name> message. This utilizes HTML escaping. """

    return f"Hello, {escape(name)}!"


# "render_template" allows Jinja2 to load html for webpages.
@app.route("/hello/")
@app.route("/hello/<name>")
def hello_name(name=None):
    """ Routes that return 'Hello, World' or a personalized greeting. """
    return render_template('name.html', name=name)


# Practice using form requests
@app.route("/calculator/", methods=['GET'])
def calculator():
    """ Route for displaying the calculator form. """

    return render_template('calculator.html')


@app.route('/calculator_result/', methods=['POST'])
def calculator_result():
    """ Route for displaying the result of the calculator form. """

    input_1 = request.form['Input1']
    input_2 = request.form['Input2']
    operation = request.form['Operation']

    try:
        input_1, input_2 = float(input_1), float(input_2)
        if operation == "+":
            r = input_1 + input_2
        elif operation == "-":
            r = input_1 - input_2
        elif operation == "/":
            r = input_1 / input_2
        elif operation == "*":
            r = input_1 * input_2
        elif operation == "%":
            r = input_1 % input_2
        
        return render_template(
            'calculator.html',
            input1=input_1,
            input2=input_2,
            operation=operation,
            result=r,
            calculation_success=True
        )
    
    except ZeroDivisionError:
        return render_template(
            'calculator.html',
            input1=input_1,
            input2=input_2,
            operation=operation,
            result="Bad Input",
            calculation_success=False,
            error="Division by zero."
        )
    except ValueError:
        return render_template(
            'calculator.html',
            input1=input_1,
            input2=input_2,
            operation=operation,
            result="Bad Input",
            calculation_success=False,
            error="Cannot perform operation with provided input."
        )
    
    except Exception as e:
        return render_template(
            'calculator.html',
            input1=input_1,
            input2=input_2,
            operation=operation,
            result="Bad Input",
            calculation_succession=False,
            error=str(e)
        )
    #return (render_template, 'calculator.html')


if __name__ == "__main__":
    app.run(debug=True)