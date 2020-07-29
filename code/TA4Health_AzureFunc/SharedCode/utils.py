def extract_HPO_codes(data, df):

    result = []
    for item in data:
        cur_data = item['entities']
        for it in cur_data:
            info = {}
            if 'links' in it:
                ds = it['links']
                hpo_codes = [entry['id'] for entry in ds if entry['dataSource']=='HPO']
                if hpo_codes:
                    start = it['offset'] # need to double check this (index 0)
                    end = start + it['length']
                    info['characters'] = [str(start), str(end)]
                    info['text'] = it['text']
                    try:
                        concept = df.loc[df['HPO_code']==hpo_codes[0],'concept'].values[0]
                    except:
                        concept = 'unable to map HPO code to concept, may need to update hpo_term_names.txt'
                    info['concept'] = concept
                    info['id'] = hpo_codes[0]
                    info['probability'] = it['score']
                    info['isNegated'] = it['isNegated']
                    result.append(info)    

    return result
