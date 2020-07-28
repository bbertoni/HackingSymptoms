import wikipediaapi
import pandas as pd
import requests
import json
import multiprocessing
import os
from functools import partial

OMIM_PAGE_STRING = "List_of_OMIM_disorder_codes"
API_STRING = "https://f29bio-dev.northeurope.cloudapp.azure.com/api/BioEntity/disease/phenotypes/en/tree/omim:"
API_HEADERS = headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                         "Accept-Encoding":"gzip, deflate",
                         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1",
                         "Connection":"close", "Upgrade-Insecure-Requests":"1"}

wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)
wiki_page = wiki_wiki.page(OMIM_PAGE_STRING)

def call_and_insert(row):
    try:
        url = API_STRING + row["OMIM ID"]
        key = "omim:" + row["OMIM ID"]
        html_content = requests.get(url, headers=API_HEADERS).text
        result = json.loads(html_content)
        symptoms = result[key]['phenotypes']
        extra_key = ""
        for key in symptoms.keys():
            if key.find("MONDO")==0:
                extra_key = key
        if extra_key in symptoms: del symptoms[extra_key]
        row["SYMPTOMS"] = json.dumps(symptoms)
    finally:
        return row

if __name__ == "__main__":
    lines = wiki_page.text.split("\n")
    lines = lines[2:len(lines)-3]
    df = pd.DataFrame(columns=["OMIM ID", "Disease", "Protein Associated"])
    rows = []
    for line in lines:
        row = line.split(";")
        new_row = {"OMIM ID": row[1][1:], "Disease": row[0], "Protein Associated": row[2][1:]}
        #df = df.append(new_row, ignore_index=True)
        #row = call_and_insert(new_row)
        rows.append(new_row)

    workers = max(os.cpu_count()-1,1)
    manager = multiprocessing.Manager()
    listManager = manager.list()
    pool = multiprocessing.Pool(workers)
    try:
        df_rows = pool.map(call_and_insert, rows)
        pool.close()
        pool.join()
    finally:
        for row in df_rows:
            df = df.append(row, ignore_index=True)
        df.to_csv("omim_with_symptoms.csv", encoding='utf-8', index=False)
