# Parse MedMention data and save it with HPO code
# Preparation: 
# Clone MedMention repo:
#   git clone https://github.com/chanzuckerberg/MedMentions.git
# Unzip the following file and copy it to the same location as this file
#   MedMentions/full/data/corpus_pubtator.txt.gz

import csv

def save_MedMention_hpo(dataFile,hpoMapFile):
    umls2hpoMap = get_umls_2_hpo_map(hpoMapFile)
    dataset_hpo = []
    with open(dataFile) as dataFileObj:
        item_hpo = dict.fromkeys(['id','title','abstract','startIdx','endIdx','text','hpo_id'])
        startIdx = []
        endIdx = []
        text = []
        hpo_id = []
        for line in dataFileObj:
            if '|t|' in line:
                if item_hpo['id']:
                    item_hpo['startIdx'] = startIdx
                    item_hpo['endIdx'] = endIdx
                    item_hpo['text'] = text
                    item_hpo['hpo_id'] = hpo_id
                    dataset_hpo.append(item_hpo)
                # Initialize for a new entry
                item_hpo = dict.fromkeys(['id','title','abstract','startIdx','endIdx','text','hpo_id'])
                startIdx = []
                endIdx = []
                text = []
                hpo_id = []
                strList = line.split('|t|')
                item_hpo['id'] = strList[0]
                item_hpo['title'] = strList[1]
            elif '|a|' in line:
                strList = line.split('|a|')
                item_hpo['abstract'] = strList[1]
            elif line in ['\n', '\r\n']:
                continue
            else:
                strList = line.split('\t')
                umls_code = strList[5].rstrip()
                if umls_code in umls2hpoMap:
                    hpo_code = umls2hpoMap[umls_code]
                    startIdx.append(strList[1])
                    endIdx.append(strList[2])
                    text.append(strList[3])
                    hpo_id.append(hpo_code)
        item_hpo['startIdx'] = startIdx
        item_hpo['endIdx'] = endIdx
        item_hpo['text'] = text
        item_hpo['hpo_id'] = hpo_id
        dataset_hpo.append(item_hpo)
    save_data_csv(dataset_hpo,'MedMentions_data_hpo.csv')

def get_umls_2_hpo_map(hpo2umlsMapFile):
    umls2hpoMap = dict()
    with open(hpo2umlsMapFile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[1] != 'NA':
                    if row[1] in umls2hpoMap:
                        umls2hpoMap[row[1]].append(row[0])
                    else:
                        umls2hpoMap[row[1]] = [row[0]]
                line_count += 1
    return umls2hpoMap

def save_data_csv(dataset_hpo,filename):
    with open(filename, mode = 'w') as result_file:
        file_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ['ID','Text','Symptom','HPO_code','Start Index','End Index']
        file_writer.writerow(header)
        for item in dataset_hpo:
            result = []
            result.append(item['id'])
            result.append(item['title'] + item['abstract'])
            result.append(item['text'])
            result.append(item['hpo_id'])
            result.append(item['startIdx'])
            result.append(item['endIdx'])
            file_writer.writerow(result)

def main():
    save_MedMention_hpo('corpus_pubtator.txt','hpo_umls_map.csv')

if __name__ == "__main__":
    main()