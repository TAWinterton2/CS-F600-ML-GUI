from flask import Flask, render_template, request
import pandas as pd
import zipfile
from zipfile import ZipFile
import pathlib 
import os, shutil


"""Input Parsing Functions"""
def csv_upload(file):
    pass

def zip_unpack(zip_file):
   #Get current wording directory of server and save it as a string
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


def text_input_parse(s):
    pass


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
            f = request.files['file']
            f.save(f.filename)
            if zipfile.is_zipfile(f):
                result = zip_unpack(f.filename)
                if isinstance(result, str):
                    return render_template('ml_form.html',
                           tab=0, 
                           filename=request.files['file'].filename,
                           error=result)
                else:
                    return render_template('ml_form.html',
                           tab=0, 
                           filename=request.files['file'].filename,
                           error=type(result))


            return render_template('ml_form.html',
                           tab=0, 
                           file_upload=True,
                           user_input=True,
                           filename=request.files['file'].filename)
        
        if 'scaling' in request.form:
            df = gen_points()
            return render_template('ml_form.html',
                           tab=1,
                           user_input=True,
                           scaling=True,
                           tables=[df.to_html(classes='data')],
                           titles=df.columns.values)
        
        if 'tt' in request.form:
            return render_template('ml_form.html',
                           tab=2,
                           user_input=True,
                           traintest=True,
                           tr=request.form['training'],
                           te=request.form['testing'])
        
        if 'hyperparams' in request.form:
            return render_template('ml_form.html',
                           tab=3,
                           user_input=True,
                           hyper=True)
        
        if 'run' in request.form:
            return render_template('ml_form.html',
                           tab=4,
                           user_input=True,
                           start=True)
        

    return render_template('ml_form.html',
                           tab=0,
                           user_input=False)


if __name__ == "__main__":
    app.run(debug=True)
