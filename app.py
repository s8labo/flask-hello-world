from flask import Flask, request
import os
import requests
import random
import cloudmersive_barcode_api_client
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def hello_world():
    return 'Test!'

# setup cloudmersive apis
API_KEY = '17d27b8b-e23d-42bd-92f0-69235984761f'
config_barcode = cloudmersive_barcode_api_client.Configuration()
config_barcode.api_key['Apikey'] = API_KEY
api_instance_barcode = cloudmersive_barcode_api_client.BarcodeScanApi(cloudmersive_barcode_api_client.ApiClient(config_barcode))

@app.route("/pzn", methods=["POST"])
def call_cloudmersive_barcode_api():

    try:
        # get image_url
        json_dict = request.json
        image_url = json_dict.get("image_url")

        # load image_data
        res = requests.get(image_url)
        image_data = res.content

        # write to tmp file
        random_int = random.randint(0,1000000)
        tmp_file_path = f"/tmp/file{random_int}"
        with open(tmp_file_path, "wb") as temp_file:
            temp_file.write(image_data)

        # call API
        api_response = api_instance_barcode.barcode_scan_image(tmp_file_path)

    # process result
   #
        res = api_response.raw_text
        pzn = res.replace("-", "")
    except Exception as e:
        # Handle exceptions
        app.logger.error(f"An error occurred: {e}")
        return "Internal Server Error", 500
    return pzn
