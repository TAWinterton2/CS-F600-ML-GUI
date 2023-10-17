from flask import Flask, render_template, request
import pandas as pd

class DataSnapshot():
    """This class handles keeping track of the data snapshot that the user submits."""
    def __init__(self):
        self.og_data = None
        self.data = None

    def select_columns(self, x, y):
        df = self.og_data[[x, y]].copy()
        self.data = df


snapshot = DataSnapshot()

"""Input Parsing Functions"""
def csv_upload(file):
    """This function takes a file input and converts it to a pandas DataFrame."""
    df = pd.read_csv(file)
    return df


def zip_unpack(zip):
    pass


def text_input_parse(s):
    """This function takes in a string submitted by the user and converts it to a float or an integer. If an error occurs, it
    returns an error to the user."""
    try:
        if '.' in s:
            f = float(s)
            format_f = "{:.{}f}".format(f, 3)
            return float(format_f), ""
        else:
            return int(s), ""
    except ValueError as e:
        return ValueError, e
    

def get_graph_data(df):
    """Chart.js scatter plot requires the dataset to be in the format: {'x': , 'y': }."""
    json = df.copy().rename(columns={df.columns[0]: 'x', df.columns[1]: 'y'})
    return json


def clean_data(df):
    pass


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
            snapshot.og_data = df
            return render_template('ml_form.html',
                           tab=0, 
                           file_upload=True,
                           filename=request.files['file'].filename,
                           og_df=snapshot.og_data.to_html(),
                           column_names=snapshot.og_data.columns.tolist())
        
        if 'select_xy' in request.form:
            snapshot.select_columns(request.form['X'], request.form['Y'])
            df = snapshot.get_graph_data(snapshot.data)
            return render_template('ml_form.html',
                           tab=0, 
                           columns_selected=True,
                           name="myChart",
                           data=df.to_json(orient="records"),
                           user_input=True,
                           og_df=snapshot.og_data.to_html(),
                           column_names=snapshot.data.columns.tolist())

        
        if 'scaling' in request.form:
            return render_template('ml_form.html',
                           tab=1,
                           user_input=True,
                           scaling=True,
                           tables=[snapshot.data.to_html(classes='data')],
                           titles=snapshot.data.columns.values,
                           og_df=snapshot.og_data.to_html())
        
        if 'tt' in request.form:
            train, e = text_input_parse(request.form['training'])
            test, e = text_input_parse(request.form['testing'])
            if train is ValueError:
                return render_template('ml_form.html',
                           tab=2,
                           user_input=True,
                           traintest=False,
                           error=e,
                           og_df=snapshot.og_data.to_html())
            if test is ValueError:
                return render_template('ml_form.html',
                           tab=2,
                           user_input=True,
                           traintest=False,
                           error=e,
                           og_df=snapshot.og_data.to_html())

            return render_template('ml_form.html',
                           tab=2,
                           user_input=True,
                           traintest=True,
                           tr=train,
                           te=test,
                           og_df=snapshot.og_data.to_html())
        
        if 'hyperparams' in request.form:
            return render_template('ml_form.html',
                           tab=3,
                           user_input=True,
                           hyper=True,
                           og_df=snapshot.og_data.to_html())
        
        if 'run' in request.form:
            return render_template('ml_form.html',
                           tab=4,
                           user_input=True,
                           start=True,
                           og_df=snapshot.og_data.to_html())
        

    return render_template('ml_form.html',
                           tab=0,
                           user_input=False)


if __name__ == "__main__":
    app.run(debug=True)