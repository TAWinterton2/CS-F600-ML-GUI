from flask import Flask, render_template, request
import pandas as pd
import zipfile
from zipfile import ZipFile
import pathlib 
import os, shutil

class DataSnapshot():
    """This class handles keeping track of the data snapshot that the user submits."""
    def __init__(self):
        self.og_data = None
        self.data = None
        self.filename = None

    def select_columns(self, x, y):
        df = self.og_data[[x, y]].copy()
        self.data = df


snapshot = DataSnapshot()



"""Input Parsing Functions"""
ALLOWED_EXTENSIONS = {'csv', 'zip'}
def allowed_file(filename):
    """Method to ensure that the user supplied a file with the correct extension."""
    # https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def csv_upload(file):
    """This function takes a file input and converts it to a pandas DataFrame."""
    df = pd.read_csv(file)
    return df

def zip_unpack(zip_file):
   #Get current wording directory of server and save it as a string
    try:
        cwd = os.getcwd()
        zip_file_path = os.path.join(cwd, zip_file)

        temp_dir = "temp"
        temp_path = os.path.join(cwd, temp_dir)

        ext = ('.csv')

        #check if temp already exists
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        with ZipFile(zip_file_path, 'r') as zObject:
        #Extract all files in the zip into a specific location
            zObject.extractall(path=temp_path)
            zObject.close()

        temp_folder_name = os.path.splitext(zip_file)[0]
        tmp = temp_path
        temp_path = os.path.join(temp_path, temp_folder_name)

        files = []
        for file in os.listdir(temp_path):
            # Mac
            if not file.startswith('.'):
                if file.endswith(ext):
                    files.append(file)

                else:
                    shutil.rmtree(tmp)
                    os.remove(zip_file_path)
                    os.chdir(cwd)
                    return "There are files in " + zip_file + " that are not .csv files. Please try again with only .csv files."
        
        d = []
        for f in files:
            tmp_path = os.path.join(temp_path, f)
            df = pd.read_csv(tmp_path, on_bad_lines='skip')
            d.append(df)

        columns = d[0].columns
        for df in d:
            if df.columns.difference(columns).empty is False:
                shutil.rmtree(tmp)
                os.remove(zip_file_path)
                os.chdir(cwd)
                return "The csv files within " + zip_file +" do not have the same column names. Please resubmit with .csvs that have matching columns."
            # load all csv files, check if columns match, return either a dataframe or a string error
        
        shutil.rmtree(tmp)
        os.remove(zip_file_path)
        os.chdir(cwd)
        return pd.concat(d, axis=0)
    except:
        return "Something went wrong."


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
            f = request.files['file']
            if allowed_file(f.filename):
                f.save(f.filename)
                if zipfile.is_zipfile(f):
                    result = zip_unpack(f.filename)
                    if isinstance(result, str):
                        return render_template('ml_form.html',
                            tab=0, 
                            filename=request.files['file'].filename,
                            error=result)
                    else:
                        snapshot.og_data = result

                else:
                    df = csv_upload(request.files['file'])
                    snapshot.og_data = df

                return render_template('ml_form.html',
                            tab=0, 
                            file_upload=True,
                            filename=request.files['file'].filename,
                            og_df=snapshot.og_data.to_html(),
                            column_names=snapshot.og_data.columns.tolist())
            else:
                return render_template('ml_form.html',
                            tab=0, 
                            filename=request.files['file'].filename,
                            error="Please submit a file with a valid extension (csv or zip).")

        if 'select_xy' in request.form:
            snapshot.select_columns(request.form['X'], request.form['Y'])
            df = get_graph_data(snapshot.data)
            return render_template('ml_form.html',
                           tab=0, 
                           columns_selected=True,
                           form_complete=True,
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
