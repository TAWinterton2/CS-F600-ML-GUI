from flask import Flask, render_template, request
import pandas as pd
from sys import stderr

class DataSnapshot():
    def __init__(self):
        self.data = None

snapshot = DataSnapshot()

"""Input Parsing Functions"""
def csv_upload(file):
    """This function takes a file input and converts it to a pandas DataFrame."""
    df = pd.read_csv(file)
    return df


def zip_unpack(zip):
    pass


def test_tip():
    test = text_input_parse("Hello!")
    test = text_input_parse("80")
    test = text_input_parse("73.421356")
    test = text_input_parse("341.2")   


def text_input_parse(s):
    """This function takes in a string submitted by the user and converts it to a float or an integer. If an error occurs, it
    returns an error to the user."""
    try:
        if '.' in s:
            f = float(s)
            format_f = "{:.{}f}".format(f, 3)
            print(s, ": ", format_f, " ", type(float(format_f)), file=stderr)
            return float(format_f), ""
        else:
            print(s, ": ", int(s), " ", type(int(s)), file=stderr)
            return int(s), ""
    except ValueError as e:
        print(e, file=stderr)
        return ValueError, e


def clean_data(df):
    pass


def gen_points():
    """Generates a simple pandas dataframe to be displayed on the front end for "scaling" purposes."""
    dict = [{'x':.50, 'y':.7},
            {'x':.60, 'y':.8},
            {'x':.70, 'y':.8},
            {'x':.80, 'y':.9},
            {'x':.90, 'y':.9},
            {'x':.100, 'y':.9},
            {'x':.110, 'y':.10},
            {'x':.120, 'y':.11},
            {'x':.130, 'y':.14},
            {'x':.140, 'y':.14},
            {'x':.150, 'y':.15}]
    df = pd.DataFrame(dict)
    return df


app = Flask(__name__)

@app.route("/")
def index():
    """Renders the home page of the website, the first page that a user will land on when visiting the website."""
    return render_template('index.html')


@app.route("/linear", methods=['POST', 'GET'])
def ml_form():
    """Renders the machine learning form for the linear regression model. This is done by pressing the button on the navigation bar."""
    if request.method == 'POST':
        # If step 1 of the ml_form has been completed, return new information
        # Update this for WTForms later to better handle the data?
        if 'upload_file' in request.form:
            df = csv_upload(request.files['file'])
            snapshot.data = df
            test_tip()
            return render_template('ml_form.html',
                           tab=0, 
                           file_upload=True,
                           name="myChart",
                           data=df.to_json(orient="records"),
                           user_input=True,
                           filename=request.files['file'].filename,
                           og_df=snapshot.data.to_html())
        
        if 'scaling' in request.form:
            return render_template('ml_form.html',
                           tab=1,
                           user_input=True,
                           scaling=True,
                           tables=[snapshot.data.to_html(classes='data')],
                           titles=snapshot.data.columns.values,
                           og_df=snapshot.data.to_html())
        
        if 'tt' in request.form:
            train, e = text_input_parse(request.form['training'])
            test, e = text_input_parse(request.form['testing'])
            if train is ValueError:
                return render_template('ml_form.html',
                           tab=2,
                           user_input=True,
                           traintest=False,
                           error=e,
                           og_df=snapshot.data.to_html())
            if test is ValueError:
                return render_template('ml_form.html',
                           tab=2,
                           user_input=True,
                           traintest=False,
                           error=e,
                           og_df=snapshot.data.to_html())

            return render_template('ml_form.html',
                           tab=2,
                           user_input=True,
                           traintest=True,
                           tr=train,
                           te=test,
                           og_df=snapshot.data.to_html())
        
        if 'hyperparams' in request.form:
            return render_template('ml_form.html',
                           tab=3,
                           user_input=True,
                           hyper=True,
                           og_df=snapshot.data.to_html())
        
        if 'run' in request.form:
            return render_template('ml_form.html',
                           tab=4,
                           user_input=True,
                           start=True,
                           og_df=snapshot.data.to_html())
        

    return render_template('ml_form.html',
                           tab=0,
                           user_input=False)


if __name__ == "__main__":
    app.run(debug=True)