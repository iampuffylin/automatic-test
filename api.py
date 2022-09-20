from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import pathlib
import config
import requests
import csv
import json
import threading
import time

slaves = config.slaves
results = []

path = pathlib.Path(__file__).parent.resolve()
app = Flask(__name__)
CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')
api = Api(app)

@app.route('/header', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
def header():
    resp = make_response('', 200)
    resp.headers['Access-Control-Allow-Headers'] = 'content-type, token'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, PATCH, DELETE'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    resp.headers['Token'] = 'yes'
    return resp

class GetConfig(Resource):
    def get(self):
        jobj = { "slaves": config.slaves, "ssh_all": config.ssh_all, "user_profile_pages": config.user_profile_pages }
        res = {"statusCode": 200,
               "message": jobj}
        return res

class LogData(Resource):
    def post(self):
        time_cost = request.json['time_cost']
        doc_name = 'api_csv'
        with open(os.path.join(path, 'test_log/', doc_name + '.csv'), 'a') as f:
            f.write(time_cost + '\n')
        return time_cost

class CallSlaves(Resource):
    def get(self): #async
        results.clear()
        t_list = []
        for s in slaves:
            t_list.append(threading.Thread(target=callExecuteTest, args=(s,)))
        for t in t_list:
            t.start()
        for t in t_list:
            t.join()
        res = {"statusCode": 200, "message": results}
        return res

    # def get(self):   # sync 
    #     res = []
    #     for s in slaves:
    #         json = requests.get('http://' + s + ':5000/ExecuteTest').json()
    #         res.append(json['message'].replace('[', '').replace(']', '').replace('\n', ''))
    #     res = {"statusCode": 200,
    #            "message": str(res)}
    #     return res

def callExecuteTest(slave):
    # print(slave)
    json = requests.get('http://' + slave + ':5000/ExecuteTest').json()
    results.append(json['message'].replace('[', '').replace(']', '').replace('\n', ''))

class ExecuteTest(Resource):
    def get(self):
        out = os.popen('python3 ~/irene/motom.py').read()
        # os.system('python3 ~/irene/motom.py')
        res = {"statusCode": 200,
               "message": out}
        return res

class CrontabTest(Resource):
    def get(self):
        res = {"statusCode": 200,
               "message": "Crontab Success"}
        return res

class UpdateSlavesCode(Resource):
    def post(self):
        for s in config.slaves:
            requests.post('http://' + s + ':5000/UpdateCode',
                files = {'file': request.files['file'] },
                data = { 'filename' : request.files['file'].filename },
                timeout = 8)
            time.sleep(5)
        res = {"statusCode": 200,
               "message": "UpdateSlavesCode Success"}
        return res

class UpdateCode(Resource):
    def post(self):
        try:
            with open(os.path.join(path, request.form['filename']), 'wb') as binary_file:
                binary_file.write(request.files['file'].read())
            res = {"statusCode": 200,
                "message": "UpdateCode Success"}
            return res
        except Exception as e:
            return str(e)

class GetAverageCost(Resource):
    def get(self):
        doc_name = 'api_csv'
        with open(os.path.join(path, 'test_log/', doc_name + '.csv'), newline='') as csvfile:
            rows = csv.reader(csvfile)
            avglist = list()
            for row in rows:
                total = 0
                for r in row:
                    total = total + float(r)
                avg = total / len(row)
                avglist.append(avg)
            totalAvg = 0
            for a in avglist:
                totalAvg = totalAvg + float(a)
        res = {"statusCode": 200,
               "message": "Average of visit every User Profile page cost: " + str(totalAvg / len(avglist)) + " seconds"}
        return res

api.add_resource(GetConfig, '/GetConfig')
api.add_resource(LogData, '/LogData')
api.add_resource(CallSlaves, '/CallSlaves')
api.add_resource(ExecuteTest, '/ExecuteTest')
api.add_resource(CrontabTest, '/CrontabTest')
api.add_resource(UpdateSlavesCode, '/UpdateSlavesCode')
api.add_resource(UpdateCode, '/UpdateCode')
api.add_resource(GetAverageCost, '/GetAverageCost')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #a