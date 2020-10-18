from flask import Flask
from flask import request, jsonify
from db_service import get_db_connection, insert_into_table, retrive_all, retrive_from_table_by_id
import json

app = Flask(__name__)


@app.route('/')
def slash():
    db_connection = get_db_connection()
    if db_connection is not None:
        db_connection.close()
    return "hi its working"


@app.route('/hello_world')
def hello_world():
    return "hello_world"


@app.route('/user/<id>',methods=['GET'])
def get_user(id):
    record = retrive_from_table_by_id("select * from users where user_id = "+id)
    user_obj = {'id':record[0],'first_name': record[1], 'last_name': record[2]}
    return jsonify(user_obj)

@app.route('/user/<id>/images',methods = ['GET'])
def get_all_users(id):
    records = retrive_all("select * from user_images where user_id = "+id)
    images = []
    for row in records:
        images.append(row[2])
    return jsonify(images)

# @app.route('/user/<id>/image',methods=['POST'])
# def create_user():
#     req_data = request.get_json()
#
#     insert_query = """insert into users(name,doj) values (%s,%s)"""
#
#     insert_into_table(insert_query,req_data)
#     return jsonify(req_data)

if __name__ == '__main__':
    port = int(8080)
    app.run(debug=True, port= port, host='0.0.0.0')

    # parser = optparse.OptionParser(usage="python3 api.py -p ")
    # parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    # (args, _) = parser.parse_args()
    # if args.port == None:
    #     print "Missing required argument: -p/--port"
    # app.run(host='0.0.0.0', port=int(args.port), debug=False)




