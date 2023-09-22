from flask import Flask, render_template, request, url_for, redirect, flash
import pandas as pd
from matplotlib.figure import Figure
import base64
from io import BytesIO


# Limits allowed file extensions to csv
ALLOWED_EXTENSIONS = {'csv'}

# Name of the module initializing / running the program
app = Flask(__name__)


def allowed_file(filename):
    """Method to ensure that the user supplied a file with the correct extension."""
    # https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def display_graph(df):
    """Method that will generate and display a graph to the html page."""
    fig = Figure()
    ax = fig.subplots()
    ax.plot(df)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return data


@app.route("/", methods=['POST','GET'])
def index():
    """ Displays the index page at url '/' """
    if request.method == 'POST':

        # If the POST request does not return the file, redirect. 
        if 'file' not in request.files:
            return render_template(
                    'index.html',
                    file_upload=False,
                    error="No file submitted. Please submit a file with the proper extension (csv).",
            )
        
        # Retrieve the file from the POST request.
        file = request.files['file']
        
        # If there is no submitted file, it will return an empty string.
        if file.filename == '':
            return render_template(
                    'index.html',
                    file_upload=False,
                    error="No file submitted. Please submit a file with the proper extension (csv).",
            )
        
        if file:
            if allowed_file(file.filename):
                df = pd.read_csv(request.files.get('file'))
                #df.plot()
                line_graph = display_graph(df)
                return render_template(
                        'index.html',
                        file_upload=True,
                        file_name=file.filename,
                        tables = [df.to_html()],
                        titles = [''],
                        img1 = line_graph
                )
            
            else:
                return render_template(
                        'index.html',
                        file_upload=False,
                        error="File extension is not correct. Please submit a file with the proper extension (csv).",
                )
        else:
            return render_template(
                    'index.html',
                    file_upload=False,
                    error= "File object is null."
            )

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)