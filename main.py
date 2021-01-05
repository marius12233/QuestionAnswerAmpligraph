from main_run import *
from flask import Flask
from flask import Response
from flask import request
from flask_cors import CORS


URL_CHAT_END_POINT='http://localhost:5000'

app = Flask(__name__)
CORS(app)

model = restore_model('./best_model.pkl')

def give_response(data={},response_code=200,response_message='OK',result=None):
    

    response_data={'response_code':response_code,
              'response_message': response_message,
              'result':data}

    print(response_data)
    json_string = json.dumps(response_data, ensure_ascii=False)

    response = Response(json_string, content_type="application/json; charset=utf-8")
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET')

    return response

@app.route('/analyze_canti',methods=['GET'])
def choose_canti():
    required_params_keys = ['start', 'stop']
    required_params={}

    for key in required_params_keys:
        required_params[key]=str(request.args.get(key))
    start=int(required_params['start'])
    stop=int(required_params['stop'])
    load_and_extract_Canti(start, stop)
    print("Done")
    return give_response({"data":"Done"})

@app.route('/train',methods=['GET'])
def train():
    global model
    train_model()
    model = restore_model('./best_model.pkl')
    return give_response({"data":"Done"})

@app.route('/query',methods=['GET'])
def make_query():
    required_params_keys = ['q']
    required_params={}

    for key in required_params_keys:
        required_params[key]=str(request.args.get(key))
    question = required_params['q']
    query(question)
    print("Question analysis completed...")
    print(os.listdir())
    try:
        r=predict_link(model)
    except:
        return give_response(data={"data":"you make an erroneous question"},response_code=500,response_message='OK')
    
    return give_response({"data":r})

@app.route('/upload',methods=['POST'])
#@cross_origin()
def upload():
    file=request.files["file"]
    filename = file.filename
    file.save("Text/"+filename)
    load_and_extract_File()
    return give_response({"data":"Done"})


if __name__ == '__main__':
    app.run(port=5001)

