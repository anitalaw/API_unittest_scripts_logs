from flask import Flask, request, make_response, jsonify, abort
from datetime import datetime

app = Flask(__name__)


items = [
    {
        'id': 1,
        'name': 'laptop',
        'value': 1000
    },
    {
        'id': 2,
        'name': 'chair',
        'value': 300,
    },
    {
        'id': 3,
        'name': 'book',
        'value': 20,
    },
]


@app.errorhandler(400)
def error(error):
    return make_response( jsonify({"error": "Error"}), 400 )

@app.route('/', methods=['GET'])
def index():
    return 'HOMEPAGE'


@app.route('/dates', methods=['GET'])
def get_date():
    """Get Dates"""
    request_data = request.get_json(silent=True)

    try:
        if request_data is None or type(request_data["full"]) is bool and request_data["full"]==False:
            date_object = datetime.now()
            result_false = {
                "day": date_object.strftime("%d"),
                "month": date_object.strftime("%m"),
                "year": date_object.strftime("%Y"),
            }
            return jsonify(result_false)

        elif type(request_data["full"]) is bool and request_data["full"]==True:
            
            date_object = datetime.now()
            
            result_true = {
                "day": date_object.strftime("%d"),
                "month": date_object.strftime("%B"),
                "year": date_object.strftime("%Y"),
                "weekday": date_object.strftime("%A")
                }
            return jsonify(result_true)
        elif "full" in request_data and type(request_data["full"]) is not bool:
            abort(400)
        
    except KeyError:
        abort(400)


@app.route('/items', methods=['POST'])
def new_post():
    """ Creates a new item in the items db """

    response_obj = request.get_json()

    if not request.json or 'name' not in request.json or 'value' not in request.json:
        abort(400)

    if type(response_obj['value']) is not int:
        abort(400)

    new_item={
        'id': items[-1].get('id')+1,
        'name': response_obj['name'],
        'value': response_obj['value']
    }
        
    items.append(new_item)
    return jsonify({"new_item": new_item}), 201
    

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """ Modifies the item_id to the request """

    item = list(filter(lambda item: item['id'] == item_id, items))
    if len(item) == 0:
        abort(400)
    if not request.json:
        abort(400)

    name = request.json.get('name', item[0]['name'])
    value = request.json.get('value', item[0]['value'])

    if type(value) is not int:
        abort(400)
    
    item[0]['name'] = name
    item[0]['value'] = value

    return jsonify({'updated_item':item[0]}), 200


if __name__=='__main__':
    app.run(debug=False)