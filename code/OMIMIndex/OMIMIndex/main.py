import json

from pronto import Ontology

def extract_omim(ontology):
    dic = {}
    for id in ontology:
        term = ontology[id]
        omim = try_get_omim(term)
        if omim:
            dic[omim] = {
                    'mondo': id,
                    'name': term.name[0].upper() + term.name[1:],
                    'source': f'https://omim.org/entry/{omim[5:]}'
                }
    return dic

def try_get_omim(term):
    for xref in term.xrefs:
        if xref.id.startswith('OMIM:'):
            return xref.id
    return None

def main():
    mondo = Ontology('mondo.obo')
    dic = extract_omim(mondo)
    with open('omim_index.json', 'w') as fp:
        json.dump(dic, fp, indent=2)

if __name__ == "__main__":
    main()
