# Parse MedMention data and save it with its original UMLS code
# Preparation: 
# Clone MedMention repo:
#   git clone https://github.com/chanzuckerberg/MedMentions.git
# Unzip the following file and copy it to the same location as this file
#   MedMentions/full/data/corpus_pubtator.txt.gz

import csv



def save_MedMention_original(dataFile):
    dataset = []
    with open(dataFile) as dataFileObj:
        item = dict.fromkeys(['id','title','abstract','startIdx','endIdx','text','semType_id','umls_id'])
        startIdx = []
        endIdx = []
        text = []
        semType_id = []
        umls_id = []
        for line in dataFileObj:
            if '|t|' in line:
                if item['id']:
                    item['startIdx'] = startIdx
                    item['endIdx'] = endIdx
                    item['text'] = text
                    item['semType_id'] = semType_id
                    item['umls_id'] = umls_id
                    dataset.append(item)
                # Initialize for a new entry
                item = dict.fromkeys(['id','title','abstract','startIdx','endIdx','text','semType_id','umls_id'])
                startIdx = []
                endIdx = []
                text = []
                semType_id = []
                umls_id = []
                strList = line.split('|t|')
                item['id'] = strList[0]
                item['title'] = strList[1]
            elif '|a|' in line:
                strList = line.split('|a|')
                item['abstract'] = strList[1]
            elif line in ['\n', '\r\n']:
                continue
            else:
                strList = line.split('\t')
                startIdx.append(strList[1])
                endIdx.append(strList[2])
                text.append(strList[3])
                semType_id.append(strList[4])
                umls_code = strList[5].rstrip()
                umls_id.append(umls_code)
        item['startIdx'] = startIdx
        item['endIdx'] = endIdx
        item['text'] = text
        item['semType_id'] = semType_id
        item['umls_id'] = umls_id
        dataset.append(item)
    save_data_csv(dataset, 'MedMentions_data_original.csv')

# Save original MedMentions data with UMLS code
def save_data_csv(dataset,filename):
    with open(filename, mode = 'w') as result_file:
        file_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ['ID','Text','Symptom','UMLS_code','SemanticTypeID','Start Index','End Index']
        file_writer.writerow(header)
        for item in dataset:
            result = []
            result.append(item['id'])
            result.append(item['title'] + item['abstract'])
            result.append(item['text'])
            result.append(item['umls_id'])
            result.append(item['semType_id'])
            result.append(item['startIdx'])
            result.append(item['endIdx'])
            file_writer.writerow(result)

def main():
    save_MedMention_original('corpus_pubtator.txt')

if __name__ == "__main__":
    main()