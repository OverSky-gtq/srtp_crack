import os
import threading

from flask import Flask, request, send_file
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource

from imageRegistration import multi_image_stitching
from maskrcnnresult import main as Crack

app = Flask(__name__)
CORS(app)
api = Api(app)


def delete_files(folder_path):
    try:
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print('deleted'+ folder_path)
        return True
    except Exception as e:
        print("Error deleting files:", e)
        return False


@app.route('/', methods=["GET"])
def index():
    return "Welcome to API v1, try /hello."


class Registration(Resource):
    img_src = './IR_src'
    output_path = './IR_result/result.jpg'

    def get(self):
        return send_file(self.output_path)


    def post(self):
        img_src = self.img_src
        output_path = self.output_path
        file = request.files['file']
        filepath = os.path.join(img_src, file.filename)
        file.save(filepath)
        multi_image_stitching(path=img_src, output_path=output_path)
        delete_files(img_src)
        return "success"


class CrackID(Resource):
    img_src = './pic'
    output_path = './results'

    def get(self):
        key = request.args.get('key')
        if not key:
            return "error"
        path = self.output_path + '/images'
        return send_file(path + '/' + key)

    def post(self):
        img_src = self.img_src
        output_path = self.output_path
        file = request.files['file']
        filepath = os.path.join(img_src, file.filename)
        file.save(filepath)
        delete_files(os.path.join(output_path, 'images'))
        Crack(dir_path='./')
        thread1 = threading.Thread(target=delete_files,args=(img_src,))
        thread1.start()
        thread2 = threading.Thread(target=delete_files,args=('./crackpic',))
        thread2.start()
        return send_file(os.path.join(output_path, 'json/mask_data.json'))


api.add_resource(Registration, '/imgRegistration')
api.add_resource(CrackID, '/CrackID')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8010)
