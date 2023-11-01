def allowed_file(filename):
    """Method to ensure that the user supplied a file with the correct extension."""
    allowed_extensions = {'csv', 'zip'}
    type = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and type in allowed_extensions:
        return type
    # https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
    return False

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
    except Exception as e:
        return Exception, e