from flask import Flask, render_template, request, url_for, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Need for DB 
class Base(DeclarativeBase):
    pass


# Needed to init db
db = SQLAlchemy(model_class=Base)


# Name of the module initializing / running the program
app = Flask(__name__)

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialize the app with db extension
db.init_app(app)

class Todo(db.Model):
    """ Creates a table in the db that contains tasks and their respective IDs."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

    def __rep__(self):
        return '<Task %r>' % self.id

# Creates the tables in the db    
with app.app_context():
    db.create_all()


@app.route("/", methods=['POST','GET'])
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
    

@app.route('/tasks', methods=['POST','GET'])
def tasks():
    """Displays a list of tasks that are stored in the db."""
    # If POST request, allow user to create a new task in the db.
    if request.method == 'POST':
        task = request.form['content']
        new = Todo(content=task)
        try:
            # Add new task to the db.
            db.session.add(new)
            db.session.commit()

            # If the db successfully adds a new task, return to home page.
            return redirect(url_for("tasks"))
        
        except Exception as e:
            print("There was an exception: ", e)

    # If GET request, query the db for all current tasks.
    else:
        tasks = Todo.query.all()
        return render_template('tasks.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete_task(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("tasks"))
    except Exception as e:
        print("There was an exception: ", e)


@app.route('/update/<int:id>', methods=['GET','POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for("tasks"))
        except Exception as e:
            print("There was an exception: ", e)
    
    else:
        return render_template('update.html', task=task)
      

if __name__ == "__main__":
    app.run(debug=True)