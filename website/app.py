from flask import Flask, render_template, request
import pandas as pd
import zipfile, os, shutil, csv
from zipfile import ZipFile
from website.models import linear_regression as lr
from website.utils import snapshot as ds
from website.utils import error_handle as err
from werkzeug.utils import secure_filename


"""Flask Operation"""
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./temp/"
snapshot = ds.snapshot()


"""Input Parsing Functions"""
def has_header(df):
    """Determine if the file has a header. It returns a list of headers to use when uploading the full file."""
    return isinstance(df.columns[0], str)


def gen_headers(x):
    """This function generates generic column names for a csv file based on the number of columns."""
    col = []
    for n in range(x): col.append("Column " + str(n+1))
    return col

"""File Upload Functions"""
def csv_upload(file):
    """This function takes a file input and converts it to a pandas DataFrame."""
    try:
        path = app.config['UPLOAD_FOLDER'] + file
        with open(path,"r") as f:
            sample = f.read(1024)
            header = csv.Sniffer().has_header(sample)
        if header:
            header='infer'
        else:
            header=None
        df = pd.read_csv(path, header=header, index_col=0)
        if not header:
            cols = gen_headers(df.shape[1])
            df = df.set_axis(cols, axis='columns')
        return df
    except Exception as e:
        return "Program returned error while uploading the csv: " + str(e)
    
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
        if os.path.isdir(temp_path) is False:
            temp_path = tmp

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
            with open(tmp_path, "r") as f:
                sample = f.read(1024)
                header = csv.Sniffer().has_header(sample)
            if header:
                header='infer'
            else:
                header=None
            df = pd.read_csv(tmp_path, on_bad_lines='skip', header=None, index_col=0)
            if not header:
                cols = gen_headers(df.shape[1])
                df = df.set_axis(cols, axis='columns')
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
    except Exception as e:
        return "Program returned error while uploading the zip: " + str(e)
    
"""Output Parsing Functions"""
def get_graph_data(df):
    """Chart.js scatter plot requires the dataset to be in the format: {'x': , 'y': }."""
    json = df.copy().rename(columns={df.columns[0]: 'x', df.columns[1]: 'y'})
    return json

def display_table(df):
    tables = df.to_html()
    titles = df.columns.tolist()
    return tables, titles

"""Gather/Validate form information."""
def validate_hyperparameter(val):
    item, e = err.text_input_parse(val)
    if item is Exception:
        return Exception
    else:
        return item
    
def get_hyperparams(request):
    try:
        val = []
        val.append(request.form['loss_strength'])
        val.append(request.form['penalty'])
        val.append(validate_hyperparameter(request.form['alpha']))
        val.append(validate_hyperparameter(request.form['l1_ratio']))
        val.append(request.form['fit_intercept'])
        val.append(validate_hyperparameter(request.form['max_iter']))
        val.append(validate_hyperparameter(request.form['tol']))
        val.append(request.form['shuffle'])
        val.append(validate_hyperparameter(request.form['verbose']))
        val.append(validate_hyperparameter(request.form['epsilon']))
        val.append(validate_hyperparameter(request.form['rand_state']))
        val.append(request.form['learning_rate'])
        val.append(validate_hyperparameter(request.form['eta0']))
        val.append(validate_hyperparameter(request.form['power_t']))
        val.append(request.form['early_stopping'])
        val.append(validate_hyperparameter(request.form['validation_fraction']))
        val.append(validate_hyperparameter(request.form['n_iter_no_change']))
        val.append(request.form['warm_start'])
        val.append(request.form['average'])
    except Exception:
        return Exception
    return val

def validate_file(request):
    print(request.files['file'])
    print(request.files['file'].filename)
    if 'file' not in request.files:
        return render_template('ml_form.html',
                    tab=0, 
                    filename=request.files['file'].filename,
                    error="No file attached in request. Please submit a file with a valid extension (csv or zip).")

    if request.files['file'].filename == "":
        return render_template('ml_form.html',
                    tab=0, 
                    filename=request.files['file'].filename,
                    error="No file submitted. Please submit a file with a valid extension (csv or zip).")
    return True

"""Forms"""
def upload_form(request):
    test = validate_file(request)
    if test is True:
        f = request.files['file']
        type = err.allowed_file(f.filename)
        if type:
            # If the uploaded file is a zip, send it to zip_unpack.
            if type == 'zip':
                f.save(secure_filename(f.filename))
                result = zip_unpack(f.filename)

            # Else, the uploaded file must be a csv file, and should go to csv_upload
            else:
                f = request.files.get('file')
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                result = csv_upload(f.filename)

            # If the upload functions return a string, an error was found and should be returned to the user.
            if isinstance(result, str):
                return render_template('ml_form.html',
                    tab=0, 
                    filename=request.files['file'].filename,
                    error=result)
            
            # Else, save the snapshot.
            else:
                snapshot.og_data = result
                snapshot.filename = secure_filename(f.filename)

            # Return the output to the user.
            return render_template('ml_form.html',
                        tab=0, 
                        file_upload=True,
                        filename=request.files['file'].filename,
                        og_df=snapshot.og_data.to_html(),
                        column_names=snapshot.og_data.columns.tolist())
        
    # In case something goes wrong, we ensure to render the template with a warning message.
    else:
        return render_template('ml_form.html',
                    tab=0, 
                    filename=request.files['file'].filename,
                    error="Please submit a file with a valid extension (csv or zip).")

def select_columns_form(request):
    if request.form['X'] == request.form['Y']:
        return render_template('ml_form.html',
                    tab=0, 
                    file_upload=True,
                    filename=snapshot.filename,
                    og_df=snapshot.og_data.to_html(),
                    column_names=snapshot.og_data.columns.tolist(),
                    error="Please select different columns for X and Y.")
    
    snapshot.select_columns(request.form['X'], request.form['Y'])
    df = get_graph_data(snapshot.data)
    return render_template('ml_form.html',
                    tab=0, 
                    columns_selected=True,
                    form_complete=True,
                    file_upload=True,
                    filename=snapshot.filename,
                    name="myChart",
                    data=df.to_json(orient="records"),
                    user_input=True,
                    og_df=snapshot.og_data.to_html(),
                    column_names=snapshot.og_data.columns.tolist())

def scaling_form(request):
    snapshot.clean_data(snapshot.data)
    snapshot.data = lr.scaling(snapshot, request.form['scale'])
    return render_template('ml_form.html',
                    tab=1,
                    user_input=True,
                    scaling=True,
                    tables=[snapshot.data.to_html(classes='data')],
                    titles=snapshot.data.columns.values,
                    og_df=snapshot.og_data.to_html())

def test_train_form(request):
    train, e = err.text_input_parse(request.form['training'])
    test, e = err.text_input_parse(request.form['testing'])
    
    # If the user submitted a non-integer/float value, return an error.
    if train is Exception:
        return render_template('ml_form.html',
                    tab=2,
                    user_input=True,
                    traintest=False,
                    error=e,
                    og_df=snapshot.og_data.to_html())
    if test is Exception:
        return render_template('ml_form.html',
                    tab=2,
                    user_input=True,
                    traintest=False,
                    error=e,
                    og_df=snapshot.og_data.to_html())

    # df = snapshot.data
    # Run the testing/train split.
    train_df, test_df, msg = lr.test_train_split(snapshot, test, train)
    
    # If an error is found while trying to split the data, display the error.
    if train_df is None:
        return render_template('ml_form.html',
                    tab=2,
                    user_input=True,
                    traintest=False,
                    error=msg,
                    og_df=snapshot.og_data.to_html())
    
    # Otherwise, get the json graph data and return the information needed for chartJS.
    test_df = get_graph_data(test_df)
    train_df = get_graph_data(train_df)
    return render_template('ml_form.html',
                            tab=2,
                            user_input=True,
                            traintest=True,
                            tr=train,
                            te=test,
                            og_df=snapshot.og_data.to_html(),
                            test_name = "testing",
                            training_name = "training",
                            test_data=test_df.to_json(orient="records"),
                            training_data=train_df.to_json(orient="records"),
                            column_names=snapshot.data.columns.tolist(),
                            error=msg)

def hyperparameter_form(request):
        val = get_hyperparams(request)
        if val is Exception:
            return render_template('ml_form.html',
                        tab=3,
                        og_df=snapshot.og_data.to_html(),
                        error="Please input proper integer/float values for the given hyperparameters.")
        lr.initialize(snapshot, val)
        return render_template('ml_form.html',
                        tab=3,
                        user_input=True,
                        hyper=True,
                        og_df=snapshot.og_data.to_html())

def run_model_form(request):
    # df = snapshot.data
    # return display_table(df)
    
    lr.fit_model(snapshot)
    df, prediction = lr.predict_model(snapshot)
    pred = get_graph_data(prediction)
    data = get_graph_data(df)
    results = lr.evaluate(snapshot)
    tables,titles = display_table(pd.DataFrame([results]))
    return render_template('ml_form.html',
                    tab=4,
                    user_input=True,
                    start=True,
                    name='eval',
                    tables=[tables],
                    titles=titles,
                    data=data.to_json(orient="records"),
                    pred=pred.to_json(orient="records"),
                    og_df=snapshot.og_data.to_html(),
                    eval=results)


@app.route("/")
def index():
    """Renders the home page of the website, the first page that a user will land on when visiting the website."""
    return render_template('index.html')


@app.route("/linear", methods=['POST', 'GET'])
def ml_form():
    """Renders the machine learning form for the linear regression model. This is done by pressing the button on the navigation bar."""
    if request.method == 'POST':
        # If step 1 of the ml_form has been completed, return new information
        if 'upload_file' in request.form:
            return upload_form(request)

        # If the user selects columns, display output.
        if 'select_xy' in request.form:
            return select_columns_form(request)

        # If the user submits the scaling form, clean the data and perform data scaling.
        if 'scaling' in request.form:
            return scaling_form(request)
        
        # If the user submits the testing/training form
        if 'tt' in request.form:
            return test_train_form(request)
        
        if 'hyperparams' in request.form:
            return hyperparameter_form(request)
        
        if 'run' in request.form:
            return run_model_form(request)
        

    return render_template('ml_form.html',
                           tab=0,
                           user_input=False)


if __name__ == "__main__":
    app.run(debug=True)