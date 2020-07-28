objects = []
with (open("text_analytics_responses.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break

data = objects[0]['documents']
parsed_output = pd.DataFrame(columns=['file','offset_list','length_list','text_list','score_list','isNegated_list','HPO_codes'])

for item in data:
    df_temp = pd.DataFrame(columns=['file','offset_list','length_list','text_list','score_list','isNegated_list','HPO_codes'])
    df_temp.loc[0,'file'] = item['id']
    cur_data = item['entities']
    offset = []
    length = []
    text = [] # HPO_symptoms
    type_name = []
    score = []
    isNegated = []
    hpo_code_list = []
    cur_result = []
    for it in cur_data:
        if 'links' in it:
            ds = it['links']
            codes = [entry['id'] for entry in ds if entry['dataSource']=='HPO']
            hpo_codes = [ab.replace('HP:', '') for ab in codes]
            if hpo_codes:
                offset.append(it['offset'])
                length.append(it['length'])
                text.append(it['text'])
                score.append(it['score'])
                isNegated.append(str(it['isNegated']))
                hpo_code_list = hpo_code_list + hpo_codes
    df_temp.loc[0,'offset_list'] = offset
    df_temp.loc[0,'length_list'] = length
    df_temp.loc[0,'text_list'] = text
    df_temp.loc[0,'score_list'] = score
    df_temp.loc[0,'isNegated_list'] = isNegated
    df_temp.loc[0,'HPO_codes'] = hpo_code_list
    parsed_output = parsed_output.append(df_temp, ignore_index=True)

parsed_output.to_csv('TAforHealth_results.csv', index=False)