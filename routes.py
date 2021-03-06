from flask import Flask, render_template, request, jsonify
import pyodbc, pdb, json
from urllib.parse import unquote

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
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Tiger Home Page')

@app.route('/server_table')
def server_table():
    return render_template('server_table.html', title='Server-Driven Table')

@app.route('/server_tree_table')
def server_tree_table():
    return render_template('server_tree_table.html', title='Server-Driven Table')

@app.route('/api/data', methods=['POST'])
def data():
    cursor.execute(sql_query)
    table_data = cursor.fetchall()
    table_data = [dict(zip(('name', 'age', 'address', 'phone', 'email'), val)) for val in table_data]

    record_count = len(table_data)
    search_column = ['name', 'age', 'email']

    # search filter
    args = json.loads(request.values.get("args"))
    print(args)

    search = args['search']['value']
    if search:
        table_data = [item for item in table_data for val in [v for k,v in item.items() if k in search_column] if str(search).lower() in str(val).lower()]
    total_filtered = len(table_data)

    print("-----------------", request.values.get("url").split('/')[-1])

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

@app.route('/api/tree_data', methods=['POST'])
def tree_data():
    res = [{
            "ID": 1,
            "CompanyName": "Super Mart of the West",
            "Address": "702 SW 8th Street",
            "City": "Bentonville",
            "State": "Arkansas",
            "Zipcode": 72716,
            "Phone": "(800) 555-2797",
            "Fax": "(800) 555-2171",
            "Website": "http://www.nowebsitesupermart.com"
        }, {
            "ID": 2,
            "CompanyName": "K&S Music",
            "Address": "1000 Nicllet Mall",
            "City": "Minneapolis",
            "State": "Minnesota",
            "Zipcode": 55403,
            "Phone": "(612) 304-6073",
            "Fax": "(612) 304-6074",
            "Website": "http://www.nowebsitemusic.com"
        }, {
            "ID": 3,
            "CompanyName": "Tom's Club",
            "Address": "999 Lake Drive",
            "City": "Issaquah",
            "State": "Washington",
            "Zipcode": 98027,
            "Phone": "(800) 955-2292",
            "Fax": "(800) 955-2293",
            "Website": "http://www.nowebsitetomsclub.com"
        }, {
            "ID": 4,
            "CompanyName": "E-Mart",
            "Address": "3333 Beverly Rd",
            "City": "Hoffman Estates",
            "State": "Illinois",
            "Zipcode": 60179,
            "Phone": "(847) 286-2500",
            "Fax": "(847) 286-2501",
            "Website": "http://www.nowebsiteemart.com"
        }, {
            "ID": 5,
            "CompanyName": "Walters",
            "Address": "200 Wilmot Rd",
            "City": "Deerfield",
            "State": "Illinois",
            "Zipcode": 60015,
            "Phone": "(847) 940-2500",
            "Fax": "(847) 940-2501",
            "Website": "http://www.nowebsitewalters.com"
        }, {
            "ID": 6,
            "CompanyName": "StereoShack",
            "Address": "400 Commerce S",
            "City": "Fort Worth",
            "State": "Texas",
            "Zipcode": 76102,
            "Phone": "(817) 820-0741",
            "Fax": "(817) 820-0742",
            "Website": "http://www.nowebsiteshack.com"
        }, {
            "ID": 7,
            "CompanyName": "Circuit Town",
            "Address": "2200 Kensington Court",
            "City": "Oak Brook",
            "State": "Illinois",
            "Zipcode": 60523,
            "Phone": "(800) 955-2929",
            "Fax": "(800) 955-9392",
            "Website": "http://www.nowebsitecircuittown.com"
        }, {
            "ID": 8,
            "CompanyName": "Premier Buy",
            "Address": "7601 Penn Avenue South",
            "City": "Richfield",
            "State": "Minnesota",
            "Zipcode": 55423,
            "Phone": "(612) 291-1000",
            "Fax": "(612) 291-2001",
            "Website": "http://www.nowebsitepremierbuy.com"
        }, {
            "ID": 9,
            "CompanyName": "ElectrixMax",
            "Address": "263 Shuman Blvd",
            "City": "Naperville",
            "State": "Illinois",
            "Zipcode": 60563,
            "Phone": "(630) 438-7800",
            "Fax": "(630) 438-7801",
            "Website": "http://www.nowebsiteelectrixmax.com"
        }, {
            "ID": 10,
            "CompanyName": "Video Emporium",
            "Address": "1201 Elm Street",
            "City": "Dallas",
            "State": "Texas",
            "Zipcode": 75270,
            "Phone": "(214) 854-3000",
            "Fax": "(214) 854-3001",
            "Website": "http://www.nowebsitevideoemporium.com"
        }, {
            "ID": 11,
            "CompanyName": "Screen Shop",
            "Address": "1000 Lowes Blvd",
            "City": "Mooresville",
            "State": "North Carolina",
            "Zipcode": 28117,
            "Phone": "(800) 445-6937",
            "Fax": "(800) 445-6938",
            "Website": "http://www.nowebsitescreenshop.com"
        }, {
            "ID": 12,
            "CompanyName": "Braeburn",
            "Address": "1 Infinite Loop",
            "City": "Cupertino",
            "State": "California",
            "Zipcode": 95014,
            "Phone": "(408) 996-1010",
            "Fax": "(408) 996-1012",
            "Website": "http://www.nowebsitebraeburn.com"
        }, {
            "ID": 13,
            "CompanyName": "PriceCo",
            "Address": "30 Hunter Lane",
            "City": "Camp Hill",
            "State": "Pennsylvania",
            "Zipcode": 17011,
            "Phone": "(717) 761-2633",
            "Fax": "(717) 761-2334",
            "Website": "http://www.nowebsitepriceco.com"
        }, {
            "ID": 14,
            "CompanyName": "Ultimate Gadget",
            "Address": "1557 Watson Blvd",
            "City": "Warner Robbins",
            "State": "Georgia",
            "Zipcode": 31093,
            "Phone": "(995) 623-6785",
            "Fax": "(995) 623-6786",
            "Website": "http://www.nowebsiteultimategadget.com"
        }, {
            "ID": 15,
            "CompanyName": "Electronics Depot",
            "Address": "2455 Paces Ferry Road NW",
            "City": "Atlanta",
            "State": "Georgia",
            "Zipcode": 30339,
            "Phone": "(800) 595-3232",
            "Fax": "(800) 595-3231",
            "Website": "http://www.nowebsitedepot.com"
        }, {
            "ID": 16,
            "CompanyName": "EZ Stop",
            "Address": "618 Michillinda Ave.",
            "City": "Arcadia",
            "State": "California",
            "Zipcode": 91007,
            "Phone": "(626) 265-8632",
            "Fax": "(626) 265-8633",
            "Website": "http://www.nowebsiteezstop.com"
        }, {
            "ID": 17,
            "CompanyName": "Clicker",
            "Address": "1100 W. Artesia Blvd.",
            "City": "Compton",
            "State": "California",
            "Zipcode": 90220,
            "Phone": "(310) 884-9000",
            "Fax": "(310) 884-9001",
            "Website": "http://www.nowebsiteclicker.com"
        }, {
            "ID": 18,
            "CompanyName": "Store of America",
            "Address": "2401 Utah Ave. South",
            "City": "Seattle",
            "State": "Washington",
            "Zipcode": 98134,
            "Phone": "(206) 447-1575",
            "Fax": "(206) 447-1576",
            "Website": "http://www.nowebsiteamerica.com"
        }, {
            "ID": 19,
            "CompanyName": "Zone Toys",
            "Address": "1945 S Cienega Boulevard",
            "City": "Los Angeles",
            "State": "California",
            "Zipcode": 90034,
            "Phone": "(310) 237-5642",
            "Fax": "(310) 237-5643",
            "Website": "http://www.nowebsitezonetoys.com"
        }, {
            "ID": 20,
            "CompanyName": "ACME",
            "Address": "2525 E El Segundo Blvd",
            "City": "El Segundo",
            "State": "California",
            "Zipcode": 90245,
            "Phone": "(310) 536-0611",
            "Fax": "(310) 536-0612",
            "Website": "http://www.nowebsiteacme.com"
    }]

    return jsonify(res)

@app.errorhandler(404)
def handle_exception(err):
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]

    app.logger.error("{}: {}".format(err.description, response["message"]))

    return render_template('error.html', the_title='Tiger Home Page', error=response['error'], error_code=err.code)
    # return jsonify(response), err.code

@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for any other server error"""
    app.logger.error(f"Unknown Exception: {str(err)}")
    app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    response = {"error": "Sorry, that error is on us, please contact support if this wasn't an accident"}
    return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)
