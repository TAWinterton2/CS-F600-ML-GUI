from flask import Flask, render_template, request
import pandas as pd
import zipfile, csv, io
from website.utils.linear_regression import LinearRegression as lr
from website.utils import data_snapshot as ds
from website.utils import error_handle as err
from werkzeug.utils import secure_filename


"""Flask Operation"""
app = Flask(__name__)
snapshot = ds.DataSnapshot()


"""Input Parsing Functions"""
def has_header(df):
    """Determine if the file has a header. It returns a list of headers to use when uploading the full file."""
    return isinstance(df.columns[0], str)


def gen_headers(df):
    """This function generates generic column names for a csv file based on the number of columns."""
    cols = []
    x = df.shape[1]
    for n in range(x): cols.append("Column " + str(n+1))
    df.columns = cols
    return df


"""File Upload Functions"""
def csv_upload(file):
    """This function takes a file input and converts it to a pandas DataFrame."""
    try:
        # Read in the csv file.
        # Currently, if there is a bad line it will warn the user. 
        df = pd.read_csv(file, header=None, encoding="ISO-8859-1", on_bad_lines='warn')

        # Convert the dataframe to a string object for the sniffer.
        strIO = io.StringIO()
        df.to_csv(strIO)

        # Determine if the dataframe has column names. If it doesn't, generate column names.
        header = csv.Sniffer().has_header(strIO.getvalue())
        if not header:
            df = gen_headers(df)
        else:
            col = df.iloc[0]
            df=df.set_axis(col.fillna(0), axis='columns')
            df.drop(index=0, axis=0, inplace=True)
            # If the first column of the csv is an index, set the index.
            if df.columns.values[0] == 0:
                df.set_index(0, inplace=True)
                df.index.name = None
            
        return df
    except Exception as e:
        return "Program returned error while uploading the csv: " + str(e)

def zip_unpack(file):
    try:
        file_like_object = file.stream._file  
        zipfile_ob = zipfile.ZipFile(file_like_object)
        file_names = zipfile_ob.infolist()
        names, files = [], []

        # Filter names to ensure that every file is correct in the directory. If it is a hidden file or subdirectory, ignore it.
        for name in file_names:
            if name.is_dir():
                continue
            elif name.filename.__contains__("__MACOSX") or name.filename.__contains__(".DS_Store"):
                continue
            elif name.filename.endswith(".csv"):
                names.append(name.filename)
            else:
                return "There are files in " + str(file.filename) + " that are not .csv files. Please try again with only .csv files."

        # Upload each csv file. Append the returned dataframe to a list.
        if names:
            for name in names:
                df = csv_upload(zipfile_ob.open(name))
                if isinstance(df, str):
                    return df
                files.append(df)

            # Determine if the csv files share the same column names.
            cols = files[0].columns
            if len(files) > 1:
                for df in files:
                    if list(cols) != list(df.columns):
                        return "The csv files within " + file.filename + """ do not have the same column names/number of columns. 
                                Please resubmit with .csvs that have matching columns."""
                # If all csv files match, return the concatted data.
                return pd.concat(files, axis=0)
            else:
                return files[0]
        else:
            return """No valid files were located within the submitted archive. 
                    Please submit a csv file or a zip folder containing csv file(s)."""

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
        return render_template('linear.html',
                    tab=0, 
                    filename=request.files['file'].filename,
                    error="No file attached in request. Please submit a file with a valid extension (csv or zip).")

    if request.files['file'].filename == "":
        return render_template('linear.html',
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
                result = zip_unpack(f)

            # Else, the uploaded file must be a csv file, and should go to csv_upload
            else:
                result = csv_upload(f)

            # If the upload functions return a string, an error was found and should be returned to the user.
            if isinstance(result, str):
                return render_template('linear.html',
                    tab=0, 
                    filename=request.files['file'].filename,
                    error=result)
            
            # Else, save the snapshot.
            else:
                snapshot.og_data = result
                snapshot.filename = secure_filename(f.filename)

            # Return the output to the user.
            return render_template('linear.html',
                        tab=0, 
                        file_upload=True,
                        filename=request.files['file'].filename,
                        og_df=snapshot.og_data.to_html(),
                        column_names=snapshot.og_data.columns.tolist())
        

        # In case something goes wrong, we ensure to render the template with a warning message.
        else:
            return render_template('linear.html',
                        tab=0, 
                        filename=request.files['file'].filename,
                        error="Please submit a file with a valid extension (csv or zip).")

    # In case something goes wrong, we ensure to render the template with a warning message.
    else:
        return render_template('linear.html',
                    tab=0, 
                    filename=request.files['file'].filename,
                    error="Please submit a file with a valid extension (csv or zip).")

def select_columns_form(request):
    if request.form['X'] == request.form['Y']:
        return render_template('linear.html',
                    tab=0, 
                    file_upload=True,
                    filename=snapshot.filename,
                    og_df=snapshot.og_data.to_html(),
                    column_names=snapshot.og_data.columns.tolist(),
                    error="Please select different columns for X and Y.")
    
    snapshot.select_columns(request.form['X'], request.form['Y'])
    df = get_graph_data(snapshot.data)
    return render_template('linear.html',
                    tab=0, 
                    columns_selected=True,
                    form_complete=True,
                    file_upload=True,
                    filename=snapshot.filename,
                    name="Selected Columns",
                    data=df.to_json(orient="records"),
                    user_input=True,
                    og_df=snapshot.og_data.to_html(),
                    column_names=snapshot.og_data.columns.tolist())

def scaling_form(request):
    snapshot.clean_data(snapshot.data)
    x, y = snapshot.create_x_y_split(snapshot.data)
    snapshot.x, snapshot.y = lr.scaling(x, y, request.form['scale'])
    snapshot.data = snapshot.merge_x_y(snapshot.x, snapshot.y)
    return render_template('linear.html',
                    tab=1,
                    user_input=True,
                    scaling=True,
                    tables=[snapshot.data.to_html(classes='data')],
                    titles=snapshot.data.columns.tolist(),
                    og_df=snapshot.og_data.to_html())

def test_train_form(request):
        
    train, e = err.text_input_parse(request.form['training'])
    test, e = err.text_input_parse(request.form['testing'])
    
    # If the user submitted a non-integer/float value, return an error.
    if train is Exception:
        return render_template('linear.html',
                    tab=2,
                    user_input=True,
                    traintest=False,
                    error=e,
                    og_df=snapshot.og_data.to_html())
    if test is Exception:
        return render_template('linear.html',
                    tab=2,
                    user_input=True,
                    traintest=False,
                    error=e,
                    og_df=snapshot.og_data.to_html())

    # Run the testing/train split.
    x_train, x_test, y_train, y_test, msg = lr.test_train_split(snapshot.x, snapshot.y, test, train)
    if x_train is None:
        return render_template('linear.html',
                    tab=2,
                    user_input=True,
                    traintest=False,
                    error=msg,
                    og_df=snapshot.og_data.to_html())
    train_df, test_df = snapshot.set_prediction_values(x_train, x_test, y_train, y_test)
    # If an error is found while trying to split the data, display the error.
    if train_df is None:
        return render_template('linear.html',
                    tab=2,
                    user_input=True,
                    traintest=False,
                    error=msg,
                    og_df=snapshot.og_data.to_html())
    
    # Otherwise, get the json graph data and return the information needed for chartJS.
    test_df = get_graph_data(test_df)
    train_df = get_graph_data(train_df)

    return render_template('linear.html',
                            tab=2,
                            user_input=True,
                            traintest=True,
                            tr=train,
                            te=test,
                            og_df=snapshot.og_data.to_html(),
                            test_name = "Test Values",
                            training_name = "Train Values",
                            test_data=test_df.to_json(orient="records"),
                            training_data=train_df.to_json(orient="records"),
                            column_names=snapshot.data.columns.tolist(),
                            error=msg)

def hyperparameter_form(request):
    val = get_hyperparams(request)
    if val is Exception:
        return render_template('linear.html',
                    tab=3,
                    og_df=snapshot.og_data.to_html(),
                    error="Please input proper integer/float values for the given hyperparameters.")
    snapshot.model = lr.initialize(val)
    return render_template('linear.html',
                    tab=3,
                    user_input=True,
                    hyper=True,
                    og_df=snapshot.og_data.to_html())

def run_model_form(request):
    snapshot.reshape_data()
    ml_model = lr.fit_model(snapshot.model, snapshot.x_train, snapshot.y_train)
    if isinstance(ml_model, str):
        return render_template('linear.html', 
                               tab=3, 
                               og_df=snapshot.og_data.to_html(), 
                               hyper_error=ml_model)
    y_pred = lr.predict_model(ml_model, snapshot.x_test)
    df = snapshot.merge_x_y(snapshot.x_test.flatten(), snapshot.y_test.flatten())
    prediction = snapshot.merge_x_y(snapshot.x_test.flatten(), y_pred)
    pred = get_graph_data(prediction)
    data = get_graph_data(df)
    results = lr.evaluate(snapshot.y_test, y_pred)
    tables,titles = display_table(pd.DataFrame([results]))
    return render_template('linear.html',
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

    return render_template('linear.html',
                           tab=0,
                           user_input=False)


if __name__ == "__main__":
    app.run(debug=True)