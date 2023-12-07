from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import zipfile, csv, io
from website.utils.linear_regression import LinearRegression as lr
from website.utils.supportvector import SupportVectorMachine as svm
from website.utils.poly import PolynomialRegression as poly
from website.utils.logistic_regression import LogRegr as logistic
from website.utils.neural_network import NeuralNetwork as neural
from website.utils.model import Model
from website.utils import data_snapshot as ds
from website.utils import error_handle as err
from werkzeug.utils import secure_filename
import itertools
import matplotlib, matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from io import BytesIO
import base64


"""Flask Operation"""
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB filesize limit
matplotlib.use("Agg")


snapshot = ds.DataSnapshot()

"""Input Parsing Functions"""


def has_header(df):
    """Determine if the file has a header. It returns a list of headers to use when uploading the full file."""
    return isinstance(df.columns[0], str)


def gen_headers(df):
    """This function generates generic column names for a csv file based on the number of columns."""
    cols = []
    x = df.shape[1]
    for n in range(x):
        cols.append("Column " + str(n + 1))
    df.columns = cols
    return df


def check_numeric_df(df):
    """This function checks if any columns contain non numeric values."""
    first_str = df.apply(lambda s: pd.to_numeric(s, errors="coerce").notnull().all())
    if first_str.all() == True:
        return True
    return False


"""File Upload Functions"""


def csv_upload(file):
    """This function takes a file input and converts it to a pandas DataFrame."""
    try:
        # Read in the csv file.
        # Currently, if there is a bad line it will warn the user.
        df = pd.read_csv(file, header=None, encoding="ISO-8859-1", on_bad_lines="warn")

        # Convert the dataframe to a string object for the sniffer.
        strIO = io.StringIO()
        df.to_csv(strIO)

        # Determine if the dataframe has column names. If it doesn't, generate column names.
        header = csv.Sniffer().has_header(strIO.getvalue())
        if not header:
            df = gen_headers(df)
        else:
            col = df.iloc[0]
            df = df.set_axis(col.fillna(0), axis="columns")
            df.drop(index=0, axis=0, inplace=True)
            # If the first column of the csv is an index, set the index.
            if df.columns.values[0] == 0:
                df.set_index(0, inplace=True)
                df.index.name = None
        if not check_numeric_df(df):
            return "CSV file contains non numeric values. Please submit a csv file that only contains numeric values for the model."
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
            elif name.filename.__contains__("__MACOSX") or name.filename.__contains__(
                ".DS_Store"
            ):
                continue
            elif name.filename.endswith(".csv"):
                names.append(name.filename)
            else:
                return (
                    "There are files in "
                    + str(file.filename)
                    + " that are not .csv files. Please try again with only .csv files."
                )

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
                        return (
                            "The csv files within "
                            + file.filename
                            + """ do not have the same column names/number of columns.
                                Please resubmit with .csvs that have matching columns."""
                        )
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
    json = df.copy().rename(columns={df.columns[0]: "x", df.columns[-1]: "y"})
    return json


def get_graph_labels(df):
    cols = df.columns.to_list()
    return [cols[0], cols[-1]]


def display_table(df):
    tables = df.to_html()
    titles = df.columns.tolist()
    return tables, titles


"""Gather/Validate form information."""


def validate_hyperparameter(val):
    if val == "None":
        return None
    item, e = err.text_input_parse(val)
    if item is Exception:
        return Exception
    else:
        return item


def logistic_hyperparams(request):
    """penalty='l2', *, dual=False, tol=0.0001, C=1.0, fit_intercept=True,
    intercept_scaling=1, class_weight=None, random_state=None, solver='lbfgs', max_iter=100, multi_class='auto',
    verbose=0, warm_start=False, n_jobs=None, l1_ratio=None"""
    # try:
    val = []
    val.append(request.form["penalty"])
    val.append(request.form["dual"])
    val.append(validate_hyperparameter(request.form["tol"]))
    val.append(validate_hyperparameter(request.form["C"]))
    val.append(request.form["fit_intercept"])
    val.append(validate_hyperparameter(request.form["intercept_scaling"]))
    val.append(validate_hyperparameter(request.form["class_weight"]))
    val.append(validate_hyperparameter(request.form["random_state"]))
    val.append(request.form["solver"])
    val.append(validate_hyperparameter(request.form["max_iter"]))
    val.append(request.form["multi_class"])
    val.append(validate_hyperparameter(request.form["verbose"]))
    val.append(request.form["warm_start"])
    val.append(validate_hyperparameter(request.form["n_jobs"]))
    val.append(validate_hyperparameter(request.form["l1_ratio"]))
    # except Exception:
    #     return Exception
    return val


def get_hyperparams(request):
    try:
        val = []
        val.append(request.form["loss_strength"])
        val.append(request.form["penalty"])
        val.append(validate_hyperparameter(request.form["alpha"]))
        val.append(validate_hyperparameter(request.form["l1_ratio"]))
        val.append(request.form["fit_intercept"])
        val.append(validate_hyperparameter(request.form["max_iter"]))
        val.append(validate_hyperparameter(request.form["tol"]))
        val.append(request.form["shuffle"])
        val.append(validate_hyperparameter(request.form["verbose"]))
        val.append(validate_hyperparameter(request.form["epsilon"]))
        val.append(validate_hyperparameter(request.form["rand_state"]))
        val.append(request.form["learning_rate"])
        val.append(validate_hyperparameter(request.form["eta0"]))
        val.append(validate_hyperparameter(request.form["power_t"]))
        val.append(request.form["early_stopping"])
        val.append(validate_hyperparameter(request.form["validation_fraction"]))
        val.append(validate_hyperparameter(request.form["n_iter_no_change"]))
        val.append(request.form["warm_start"])
        val.append(request.form["average"])
        if snapshot.model_type == "poly":
            val.append(validate_hyperparameter(request.form["degree"]))
    except Exception:
        return Exception
    return val


def validate_file(request, page):
    if "file" not in request.files:
        return render_template(
            page,
            tab=0,
            filename=request.files["file"].filename,
            error="No file attached in request. Please submit a file with a valid extension (csv or zip).",
        )

    if request.files["file"].filename == "":
        return render_template(
            page,
            tab=0,
            filename=request.files["file"].filename,
            error="No file submitted. Please submit a file with a valid extension (csv or zip).",
        )
    return True


"""Forms"""


def upload_form(request, page):
    test = validate_file(request, page)
    if test is True:
        f = request.files["file"]
        type = err.allowed_file(f.filename)
        if type:
            # If the uploaded file is a zip, send it to zip_unpack.
            if type == "zip":
                result = zip_unpack(f)

            # Else, the uploaded file must be a csv file, and should go to csv_upload
            else:
                result = csv_upload(f)

            # If the upload functions return a string, an error was found and should be returned to the user.
            if isinstance(result, str):
                return render_template(
                    page, tab=0, filename=request.files["file"].filename, error=result
                )

            # Else, save the snapshot.
            else:
                snapshot.og_data = result
                snapshot.filename = secure_filename(f.filename)

            # Return the output to the user.
            return render_template(
                page,
                tab=0,
                file_upload=True,
                filename=request.files["file"].filename,
                og_df=snapshot.og_data.to_html(),
                column_names=snapshot.og_data.columns.tolist(),
            )

        # In case something goes wrong, we ensure to render the template with a warning message.
        else:
            return render_template(
                page,
                tab=0,
                filename=request.files["file"].filename,
                error="Please submit a file with a valid extension (csv or zip).",
            )

    # In case something goes wrong, we ensure to render the template with a warning message.
    else:
        return render_template(
            page,
            tab=0,
            filename=request.files["file"].filename,
            error="Please submit a file with a valid extension (csv or zip).",
        )


def select_columns_form(request, page):
    Y = request.form["Y"]
    X = request.form.getlist("X")
    if Y in X:
        return render_template(
            page,
            tab=0,
            file_upload=True,
            filename=snapshot.filename,
            og_df=snapshot.og_data.to_html(),
            column_names=snapshot.og_data.columns.tolist(),
            error="Please select different columns for X and Y.",
        )

    # Select the columns
    snapshot.select_columns(X, Y)
    df = get_graph_data(snapshot.data)
    return render_template(
        page,
        tab=0,
        columns_selected=True,
        form_complete=True,
        file_upload=True,
        filename=snapshot.filename,
        name="Selected Columns",
        data=df.to_json(orient="records"),
        data_columns=get_graph_labels(snapshot.data),
        user_input=True,
        og_df=snapshot.og_data.to_html(),
        column_names=snapshot.og_data.columns.tolist(),
    )


def scaling_form(request, page):
    snapshot.clean_data(snapshot.data)
    x, y = snapshot.create_x_y_split(snapshot.data)
    snapshot.x, snapshot.y = Model.scaling(x, y, request.form["scale"])

    # Create a dataframe with x and y to display the information in a table for the user.
    snapshot.data = snapshot.merge_x_y(snapshot.x, snapshot.y)
    return render_template(
        page,
        tab=1,
        user_input=True,
        scaling=True,
        tables=[snapshot.data.to_html(classes="data")],
        titles=snapshot.data.columns.tolist(),
        og_df=snapshot.og_data.to_html(),
    )


def test_train_form(request, page):
    train, e = err.text_input_parse(request.form["training"])
    test, e = err.text_input_parse(request.form["testing"])

    # If the user submitted a non-integer/float value, return an error.
    if train is Exception:
        return render_template(
            page,
            tab=2,
            user_input=True,
            traintest=False,
            error=e,
            og_df=snapshot.og_data.to_html(),
        )
    if test is Exception:
        return render_template(
            page,
            tab=2,
            user_input=True,
            traintest=False,
            error=e,
            og_df=snapshot.og_data.to_html(),
        )

    # Run the testing/training split based on if the model is linear or poly
    x_train, x_test, y_train, y_test, msg = Model.test_train_split(
        snapshot.x, snapshot.y, test, train
    )

    if x_train is None:
        return render_template(
            page,
            tab=2,
            user_input=True,
            traintest=False,
            error=msg,
            og_df=snapshot.og_data.to_html(),
        )

    # TODO: Review sorting method.
    x_test, y_test = snapshot.sort_x(x_test, y_test)
    snapshot.set_prediction_values(x_train, x_test, y_train, y_test)
    train_df = snapshot.merge_x_y(x_train, y_train)
    test_df = snapshot.merge_x_y(x_test, y_test)

    # If an error is found while trying to split the data, display the error.
    if train_df is None or test_df is None:
        return render_template(
            page,
            tab=2,
            user_input=True,
            traintest=False,
            error=msg,
            og_df=snapshot.og_data.to_html(),
        )

    # Otherwise, get the json graph data and return the information needed for chartJS.
    test_df = get_graph_data(test_df)
    train_df = get_graph_data(train_df)

    return render_template(
        page,
        tab=2,
        user_input=True,
        traintest=True,
        tr=train,
        te=test,
        og_df=snapshot.og_data.to_html(),
        test_name="Test Values",
        training_name="Train Values",
        test_data=test_df.to_json(orient="records"),
        training_data=train_df.to_json(orient="records"),
        data_columns=get_graph_labels(snapshot.data),
        column_names=snapshot.data.columns.tolist(),
        error=msg,
    )


def hyperparameter_form(request, page):
    if snapshot.model_type == "poly":
        val = get_hyperparams(request)
        if val is Exception:
            return render_template(
                page,
                tab=3,
                og_df=snapshot.og_data.to_html(),
                error="Please input proper integer/float values for the given hyperparameters.",
            )
        snapshot.model = poly.initialize(val)

    if snapshot.model_type == "logistic":
        val = logistic_hyperparams(request)
        if val is Exception:
            return render_template(
                page,
                tab=3,
                og_df=snapshot.og_data.to_html(),
                error="Please input proper integer/float values for the given hyperparameters.",
            )
        snapshot.model = logistic.initialize(val)

    elif snapshot.model_type == "linear":
        val = get_hyperparams(request)
        if val is Exception:
            return render_template(
                page,
                tab=3,
                og_df=snapshot.og_data.to_html(),
                error="Please input proper integer/float values for the given hyperparameters.",
            )
        snapshot.model = lr.initialize(val)

    elif snapshot.model_type == "svm":
        snapshot.model = svm.initalize(val)

    return render_template(
        page, tab=3, user_input=True, hyper=True, og_df=snapshot.og_data.to_html()
    )


# TODO: Finish confusion matrix code.
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ConfusionMatrixDisplay.html
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
def run_model_matrix(page):
    def plot_confusion_matrix(
        cm, classes, normalize=False, title="Confusion matrix", cmap=plt.cm.Blues
    ):
        if normalize:
            cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

        plt.imshow(cm, interpolation="nearest", cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = ".2f" if normalize else "d"
        thresh = cm.max() / 2.0
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(
                j,
                i,
                format(cm[i, j], fmt),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )

        plt.tight_layout()
        plt.ylabel("True label")
        plt.xlabel("Predicted label")

    if snapshot.model_type == "logistic":
        ml_model = logistic.fit_model(
            snapshot.model, snapshot.x_train, snapshot.y_train
        )
        if isinstance(ml_model, str):
            return render_template(
                page, tab=3, og_df=snapshot.og_data.to_html(), hyper_error=ml_model
            )
        y_pred = logistic.predict_model(ml_model, snapshot.x_test)
        results = logistic.evaluate(snapshot.y_test, y_pred)

    if snapshot.model_type == "svm":
        ml_model = svm.fit_model(snapshot.model, snapshot.x_train, snapshot.y_train)
        if isinstance(ml_model, str):
            return render_template(
                page, tab=3, og_df=snapshot.og_data.to_html(), hyper_error=ml_model
            )
        y_pred = svm.predict_model(ml_model, snapshot.x_test)
        results = svm.evaluate(snapshot.y_test, y_pred)

        cm_labels = ["first", "second"]

        cm = confusion_matrix(snapshot.y_test, y_pred)

        plot_confusion_matrix(cm, cm_labels)

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode()

        return render_template(
            page,
            tab=4,
            user_input=True,
            start=True,
            name="eval",
            eval_table=list(results.values()),
            # data=data.to_json(orient="records"),
            # pred=pred.to_json(orient="records"),
            data_columns=get_graph_labels(snapshot.data),
            og_df=snapshot.og_data.to_html(),
            eval=results,
            graphic=graphic,
        )

    if snapshot.model_type == "neural":
        ml_model = neural.fit_model(snapshot.model, snapshot.x_train, snapshot.y_train)

        if isinstance(ml_model, str):
            return render_template(
                page, tab=3, og_df=snapshot.og_data.to_html(), hyper_error=ml_model
            )

        y_pred = neural.predict_model(ml_model, snapshot.x_test)

        results = neural.evaluate(snapshot.y_test, y_pred)

        cm_labels = ["first", "second"]

        cm = confusion_matrix(snapshot.y_test, y_pred)

        plot_confusion_matrix(cm, cm_labels)

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode()

        return render_template(
            page,
            tab=4,
            og_df=snapshot.og_data.to_html(),
            eval_table=list(results.values()),
            graphic=graphic,
        )

    return render_template(page, tab=4)


def run_model_form(page):
    if snapshot.model_type == "logistic":
        return run_model_matrix(page)
    if snapshot.model_type == "svm":
        return run_model_matrix(page)
    if snapshot.model_type == "neural":
        return run_model_matrix(page)
    else:
        if snapshot.model_type == "poly":
            ml_model = poly.fit_model(
                snapshot.model, snapshot.x_train, snapshot.y_train
            )
            # If fit returned an error, print the error and redirect to hyperparameters
            if isinstance(ml_model, str):
                return render_template(
                    page, tab=3, og_df=snapshot.og_data.to_html(), hyper_error=ml_model
                )
            # Predict and evaluate the model
            # TODO: Review sorting method. Commented code is original code.
            x_test_sorted = sorted(snapshot.x_test, key=lambda x: x[0])
            y_pred = poly.predict_model(ml_model, x_test_sorted)
            # y_pred = poly.predict_model(ml_model, snapshot.x_test)
            results = poly.evaluate(snapshot.y_test, y_pred)

        elif snapshot.model_type == "linear":
            ml_model = lr.fit_model(snapshot.model, snapshot.x_train, snapshot.y_train)
            # If fit returned an error, print the error and redirect to hyperparameters
            if isinstance(ml_model, str):
                return render_template(
                    page, tab=3, og_df=snapshot.og_data.to_html(), hyper_error=ml_model
                )
            # Predict and evaluate the model
            # TODO: Review sorting method. Commented code is original code.
            x_test_sorted = sorted(snapshot.x_test, key=lambda x: x[0])
            y_pred = lr.predict_model(ml_model, x_test_sorted)
            # y_pred = lr.predict_model(ml_model, snapshot.x_test)
            results = lr.evaluate(snapshot.y_test, y_pred)

        # Get graph data for the prediction graph
        df = snapshot.merge_x_y(snapshot.x_test, snapshot.y_test)
        data = get_graph_data(df)
        # TODO: Review sorting method. Commented code is original code.
        prediction = snapshot.merge_x_y(x_test_sorted, y_pred)
        # # prediction = snapshot.merge_x_y(snapshot.x_test, y_pred)
        pred = get_graph_data(prediction)

        return render_template(
            page,
            tab=4,
            user_input=True,
            start=True,
            name="eval",
            eval_table=list(results.values()),
            data=data.to_json(orient="records"),
            pred=pred.to_json(orient="records"),
            data_columns=get_graph_labels(snapshot.data),
            og_df=snapshot.og_data.to_html(),
            eval=results,
        )


@app.route("/")
def index():
    """Renders the home page of the website, the first page that a user will land on when visiting the website."""
    return render_template("index.html")


@app.route("/about")
def about():
    """Renders the about page of the website, which contains information about the project and the team."""
    return render_template("about.html")


@app.route("/linear", methods=["POST", "GET"])
def linear_form():
    """Renders the machine learning form for the linear regression model. This is done by pressing the button on the navigation bar."""
    snapshot.model_type = "linear"
    page = "linear.html"
    if request.method == "POST":
        # If step 1 of the ml_form has been completed, return new information
        if "upload_file" in request.form:
            return upload_form(request, page)

        # If the user selects columns, display output.
        if "select_xy" in request.form:
            return select_columns_form(request, page)

        # If the user submits the scaling form, clean the data and perform data scaling.
        if "scaling" in request.form:
            return scaling_form(request, page)

        # If the user submits the testing/training form
        if "tt" in request.form:
            return test_train_form(request, page)

        if "hyperparams" in request.form:
            return hyperparameter_form(request, page)

        if "run" in request.form:
            return run_model_form(page)

    return render_template("linear.html", tab=0, user_input=False)


@app.route("/poly", methods=["POST", "GET"])
def poly_form():
    """Renders the machine learning form for the polynomial regression model. This is done by pressing the button on the navigation bar."""
    snapshot.model_type = "poly"
    page = "poly.html"
    if request.method == "POST":
        # If step 1 of the ml_form has been completed, return new information
        if "upload_file" in request.form:
            return upload_form(request, page)

        # If the user selects columns, display output.
        if "select_xy" in request.form:
            return select_columns_form(request, page)

        # If the user submits the scaling form, clean the data and perform data scaling.
        if "scaling" in request.form:
            return scaling_form(request, page)

        # If the user submits the testing/training form
        if "tt" in request.form:
            return test_train_form(request, page)

        if "hyperparams" in request.form:
            return hyperparameter_form(request, page)

        if "run" in request.form:
            return run_model_form(page)

    return render_template(page, tab=0, user_input=False)


@app.route("/logistic", methods=["POST", "GET"])
def logistic_form():
    """Renders the machine learning form for the logisitc regression model. This is done by pressing the button on the navigation bar."""
    snapshot.model_type = "logistic"
    page = "logistic.html"
    if request.method == "POST":
        # If step 1 of the ml_form has been completed, return new information
        if "upload_file" in request.form:
            return upload_form(request, page)

        # If the user selects columns, display output.
        if "select_xy" in request.form:
            return select_columns_form(request, page)

        # If the user submits the scaling form, clean the data and perform data scaling.
        if "scaling" in request.form:
            return scaling_form(request, page)

        # If the user submits the testing/training form
        if "tt" in request.form:
            return test_train_form(request, page)

        if "hyperparams" in request.form:
            return hyperparameter_form(request, page)

        if "run" in request.form:
            return run_model_form(page)

    return render_template("logistic.html", tab=0, user_input=False)


@app.route("/svm", methods=["POST", "GET"])
def svm_form():
    snapshot.model_type = "svm"
    page = "svm.html"
    if request.method == "POST":
        # If step 1 of the ml_form has been completed, return new information
        if "upload_file" in request.form:
            return upload_form(request, page)

        # If the user selects columns, display output.
        if "select_xy" in request.form:
            return select_columns_form(request, page)

        # If the user submits the scaling form, clean the data and perform data scaling.
        if "scaling" in request.form:
            return scaling_form(request, page)

        # If the user submits the testing/training form
        if "tt" in request.form:
            return test_train_form(request, page)

        if "hyperparams" in request.form:
            return hyperparameter_form(request, page)

        if "run" in request.form:
            return run_model_form(page)

    return render_template("svm.html", tab=0, user_input=False)


@app.route("/neural", methods=["POST", "GET"])
def neural_form():
    """Renders the machine learning form for the neural network model. This is done by pressing the button on the navigation bar."""
    snapshot.model_type = "neural"
    page = "neural.html"
    if request.method == "POST":
        if "upload_file" in request.form:
            return upload_form(request, page)

        if "select_xy" in request.form:
            return select_columns_form(request, page)

        if "scaling" in request.form:
            return scaling_form(request, page)

        if "tt" in request.form:
            return test_train_form(request, page)

        if "hyperparams" in request.form:
            return hyperparameter_form(request, page)

        if "run" in request.form:
            return run_model_form(page)

    return render_template("neural.html", tab=0, user_input=False)


@app.errorhandler(413)
def file_too_large(e):
    return "File too large", 413


if __name__ == "__main__":
    app.run(debug=True)
