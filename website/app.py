from flask import Flask, render_template, request
import pandas as pd


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
                           tab=0)


if __name__ == "__main__":
    app.run(debug=True)