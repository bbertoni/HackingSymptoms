import logging
import azure.functions as func
import json
import requests
import pandas as pd
from ..SharedCode.utils import *
from ..SharedCode import config


def run(raw_data):

    raw_data = json.loads(raw_data)

    # get results from Text Analytics for Health API
    logging.info('Getting results from Text Analytics for Health API')
    textanalytics_url=config.text_analytics_endpoint 
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }
    payload = {"documents":[{"language":"en", 
                             "id":"1",
                             "text":raw_data['data']}]}
    response = requests.request("POST", textanalytics_url, headers=headers, json = payload)
    logging.info('TA4H status: {}'.format(response.status_code))
    logging.info(response.json())
    output_dict = {}
    output_dict['status'] = response.status_code
    output_dict['result'] = []
    output_dict['message'] = None
    output_dict["exception"] = None

    if "errors" in response.json():
        if response.status_code == 200 and response.json()["errors"] == []:
            # get HPO code concept names
            df = pd.read_csv('./hpo_term_names.txt',sep='\t',header=None)
            df.columns = ['HPO_code','concept']

            # parse Text Analytics for Health API results
            logging.info('Parsing Text Analytics for Health API results')
            result = extract_HPO_codes(response.json()["documents"],df)
            output_dict['result'] = result
            output_dict['message'] = None
            output_dict["exception"] = None
        else:
            output_dict["exception"] = response.json()["errors"]
            output_dict["message"] = "Azure Text Analytics for Health API errors listed in 'exception' field"
    else:
        if response.status_code == 200:
            # get HPO code concept names
            df = pd.read_csv('./hpo_term_names.txt',sep='\t',header=None)
            df.columns = ['HPO_code','concept']

            # parse Text Analytics for Health API results
            logging.info('Parsing Text Analytics for Health API results')
            result = extract_HPO_codes(response.json()["documents"],df)
            output_dict['result'] = result
            output_dict['message'] = None
            output_dict["exception"] = None

        elif "error" in response.json():
            output_dict["exception"] = response.json()["error"]
            output_dict["message"] = "Azure Text Analytics for Health API errors listed in 'exception' field"

        else:
            output_dict["message"] = "Azure Text Analytics for Health API errors listed in 'exception' field"


    output_json = json.dumps(output_dict)

    return output_json



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    raw_data = req.get_body()
    if not raw_data:
        try:
            logging.info('Getting json')
            req_body = json.dumps({})
            req_body = req.get_json()
        except ValueError:
            logging.info('Incorrect input format')
            output_dict = {}
            output_dict['status'] = 406
            output_dict['result'] = []
            output_dict['message'] = 'Error calling run function in __init__.py'
            output_dict["exception"] = str('Please reformat input as JSON: {"data": "sample text HERE"}')
            output_json = json.dumps(output_dict)   
            return func.HttpResponse(output_json, headers={"Content-Type": "application/json"})
        else:
            logging.info('Getting raw data')
            raw_data = req_body.get('raw_data')

    if raw_data:
        logging.info('Calling run function')
        try:
            output_json = run(raw_data)
        except Exception as e:
            logging.info('Error calling run function')           
            output_dict = {}
            output_dict['status'] = 500
            output_dict['result'] = []
            output_dict['message'] = 'Error calling run function in __init__.py'
            output_dict["exception"] = str(e)
            output_json = json.dumps(output_dict)     
            return func.HttpResponse(output_json, headers={"Content-Type": "application/json"})
        return func.HttpResponse(output_json, headers={"Content-Type": "application/json"})
    else:
        logging.info('ERROR')
        output_dict = {}
        output_dict['status'] = 500
        output_dict['result'] = []
        output_dict["exception"] = "ERROR"
        output_json = json.dumps(output_dict)     
        return func.HttpResponse(output_json, headers={"Content-Type": "application/json"})
