import logging
import azure.functions as func
import json
import requests
import pandas as pd
from ..SharedCode.utils import *


def run(raw_data):

    raw_data = json.loads(raw_data)

    # get results from Text Analytics for Health API
    logging.info('Getting results from Text Analytics for Health API')
    textanalytics_url="https://ta4h-app-service.azurewebsites.net/text/analytics/v3.0-preview.1/domains/health"
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }
    payload = {"documents":[{"language":"en", 
                             "id":"1",
                             "text":raw_data['data']}]}
    response = requests.request("POST", textanalytics_url, headers=headers, json = payload)
    
    output_dict = {}
    output_dict['status'] = response.status_code
    output_dict['result'] = []
    output_dict['message'] = None
    output_dict["exception"] = None

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
    else:
        output_dict["exception"] = "Azure Text Analytics for Health API call failed"

    output_json = json.dumps(output_dict)

    return output_json



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    raw_data = req.get_body()
    if not raw_data:
        try:
            logging.info('Getting json')
            req_body = req.get_json()
        except ValueError:
            logging.info('Incorrect input format')
            pass
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
     #       output_dict['status'] = response.status_code
            output_dict['result'] = []
            output_dict['message'] = None
            output_dict["exception"] = 'Error: {}'.format(e)  
            output_json = json.dumps(output_dict)          
        return func.HttpResponse(output_json, headers={"Content-Type": "application/json"})
    else:
        logging.info('ERROR')
        return func.HttpResponse(
                "Please reformat input as JSON",
                status_code = 400
                )
