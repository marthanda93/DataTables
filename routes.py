from flask import Flask, render_template, request, jsonify
import pyodbc, pdb, json
from urllib.parse import unquote
from itertools import groupby

app = Flask(__name__)

# --------------------------------//DB connection || START
server = 'mssql'
database = 'Navin'
username = 'SA'
password= 'setSt1234'
driver= '{ODBC Driver 17 for SQL Server}'
db_cnx = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password+';autocommit=False')
cursor = db_cnx.cursor()
cursor.fast_executemany = True
sql_query = "select name, age, address, phone, email from Navin.dbo.Persons"
# --------------------------------//DB connection || END

def keyfunc(s):
    return [int(''.join(g)) if k else ''.join(g) for k, g in groupby('\0'+s, str.isdigit)]

@app.route('/')
def index():
    return render_template('server_table.html', title='Server-Driven Table')

@app.route('/api/data', methods=['POST'])
def data():
    cursor.execute(sql_query)
    table_data = cursor.fetchall()
    table_data = [dict(zip(('name', 'age', 'address', 'phone', 'email'), val)) for val in table_data]

    record_count = len(table_data)
    search_column = ['name', 'age', 'email']

    # search filter
    args = json.loads(request.values.get("args"))

    search = args['search']['value']
    if search:
        table_data = [item for item in table_data for val in [v for k,v in item.items() if k in search_column] if str(search).lower() in str(val).lower()]
    total_filtered = len(table_data)

    # sorting
    i = 0
    while True:
        col_index = args['order'][i]['column'] if i < len(args['order']) else None
        if col_index is None:
            break

        col_name = args['columns'][col_index]['data']
        if col_name not in search_column:
            col_name = 'name'

        if  col_name == 'age':
            if args['order'][i]['dir'] == 'desc':
                table_data = sorted(table_data, key=lambda k: int(k[col_name]), reverse=True)
            else:
                table_data = sorted(table_data, key=lambda k: int(k[col_name]))
        else:
            if args['order'][i]['dir'] == 'desc':
                table_data = sorted(table_data, key=lambda k: k[col_name], reverse=True)
            else:
                table_data = sorted(table_data, key=lambda k: k[col_name])
        i += 1

    # pagination
    draw = int(args['draw'])
    start = int(args['start'])
    length = int(args['length'])

    query = table_data[start:start + length]

    res = {
        'data': query,
        'recordsFiltered': total_filtered,
        'recordsTotal': record_count,
        'draw': draw,
    }

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
