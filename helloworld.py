
from flask import Flask, request, make_response,jsonify
import uuid
import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(
    dbname="project",
    user="melo",
    password="qaz129946858",
    host="postgres-service",
    port="5432"
)

@app.route('/', methods=['POST'])
def hello_world():
    app.logger.warning(request.data)
    # Respond with another event (optional)
    response = make_response({
        "msg": "Hi from helloworld-python app!"
    })
    response.headers["Ce-Id"] = str(uuid.uuid4())
    response.headers["Ce-specversion"] = "0.3"
    response.headers["Ce-Source"] = "knative/eventing/samples/hello-world"
    response.headers["Ce-Type"] = "dev.knative.samples.hifromknative"
    try:
        data = request.get_json()
        cursor = conn.cursor()
        cmd = data['cmd']
        #id = data['id']
        # name = data['name']
        # price = data['price']
        # print(id,name,price)
        if cmd == "POST":
           cursor.execute('INSERT INTO obj (id, name, price) VALUES (%s, %s, %s);',(data['id'],data['name'],data['price']))
           conn.commit()
           return response
        elif cmd == "PUT":
             cursor.execute('UPDATE obj SET name = %s, price = %s WHERE id = %s;',
                   (data['name'], data['price'], data['id']))
             conn.commit()
             return response
        elif cmd == "DELETE":
             cursor.execute('DELETE FROM obj WHERE id = %s;', (data['id']))
             conn.commit()
             return response
    except Exception as e:
        conn.rollback()
        return response
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
