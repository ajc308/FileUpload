import io
import config
import csv
import uuid
from flask import Flask, request

from database import get_connection, get_table_columns, truncate_table

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def import_file_to_database(file, database, table, truncate, ignore_fields):
    if truncate:
        truncate_table(database, table)

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)

    file_upload_id = uuid.uuid1()

    file_fieldnames = csv_input.fieldnames
    file_fieldnames_count = len(csv_input.fieldnames)
    table_columns = get_table_columns(database, table)

    if ignore_fields:
        file_fieldnames = list(set(file_fieldnames).intersection(set(table_columns)))
        file_fieldnames_count = len(file_fieldnames)
    else:
        invalid_columns = list(set(file_fieldnames).difference(set(table_columns)))
        if invalid_columns:
            raise ValueError('Invalid columns: {}  Table has columns: {}'.format(invalid_columns, table_columns))

    query_columns = ', '.join(map(str, file_fieldnames)) + ', FileUploadID'

    insert_query = 'INSERT INTO {table} ({columns}) VALUES '.format(table=table, columns=query_columns)
    value_subs = '(' + ', '.join(map(str, ['%s'] * (file_fieldnames_count + 1))) + ')'
    query_values = [[row[file_fieldnames[i]] for i in range(0, file_fieldnames_count)] for row in csv_input]
    for values in query_values:
        values.append(str(file_upload_id))
    query_values = [tuple(values) for values in query_values]

    conn = get_connection(database)
    cursor = conn.cursor()

    try:
        cursor.executemany(insert_query + value_subs, query_values)
    except Exception as e:
        raise ValueError((e, insert_query + value_subs, query_values))

    conn.commit()

    cursor.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = ''
    if request.method == 'POST':
        file = request.files['file']
        table = request.form['table']
        database = request.form['database']
        truncate_table = True if 'truncate_table' in request.form.keys() else False
        ignore_fields = True if 'ignore_fields' in request.form.keys() else False

        if file.filename == '':
            message = 'No selected file'

        if not allowed_file(file.filename):
            message = 'Invalid file type, must be .csv'

        if not table:
            message = 'Please enter a table name'

        if not database:
            message = 'Please enter a database name'

        if file and allowed_file(file.filename) and table and database:
            try:
                import_file_to_database(file, database, table, truncate_table, ignore_fields)
                message = '<script>parent.location.href=parent.location.href</script>'
            except Exception as e:
                message = e

    return """
    <!doctype html>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <title>Upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <div class="container">
        <div class="row">
          <div class="col-md-1">
            <div class="input-group">
              <label for="database">Database Name:&nbsp;</label>
              <input name="database" value="{DEFAULT_DATABASE}">
              <br><br>
              <label for="table">Target Table Name:&nbsp;</label>
              <input name="table" value="{DEFAULT_TABLE}">
              <br><br>
              <input type="file" name="file">
              <br>
              <input type="checkbox" name="truncate_table"> Truncate target table?<br>
              <input type="checkbox" name="ignore_fields"> Ignore non-matching fields?<br>
              <br>
              <input type="submit" value="Upload" class="btn btn-primary">
          </div>
        </div>
      </div>
    </form>
    <br>
    <div>{message}</div>
    """.format(
        message=message,
        DEFAULT_DATABASE=config.DEFAULT_DATABASE,
        DEFAULT_TABLE=config.DEFAULT_TABLE
    )


if __name__ == "__main__":
    app.run()
