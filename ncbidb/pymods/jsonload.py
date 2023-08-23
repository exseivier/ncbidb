

#
#   PYTHON MODULE JSONLOAD.PY
#   AUTHOR JAVIER MONTALVO-ARREDONDO
#   VERSION 0.0.1
#   CONTACT buitrejma@gmail.com
#   UNIVERSIDAD AUTONOMA AGRARIA ANTONIO NARRO
#   CALZADA ANTONIO NARRO 1923
#   BUENAVISTA SALTILLO COAHUILA.
#


import json
import pandas as pd

def load_json_lines(filename):
    """
        Loads jsonl files into an empty dictionary
    """

    with open(filename, 'r') as FHIN:
        jsondata = FHIN.readlines()

    data = {}

    [data.update({eval(jsondata[x])['accession'] : eval(jsondata[x].strip())}) \
            for x in range(len(jsondata))]

    return data

def load_json(filename):
    """
        Loads json files into a dictionary.
    """

    with open(filename, 'r') as FHIN:
        data = json.load(FHIN)
    
    data['assemblies'].pop(0)
    data = data['assemblies']
    dictionary = {}
    _ = [dictionary.update({data[x]['accession'] : data[x]['files']}) \
            for x in range(len(data))]
        
    return dictionary

def load_df(dic_json = None, dic_json_lines = None):
    """
        Populates a panda's dataframe with data from json and jsonl files.
    """
    assert dic_json != None \
            and dic_json_lines != None, \
            f'Both dictionaries must be not None'

    assert all([item in list(dic_json.keys()) \
            for item in list(dic_json_lines.keys())]), \
            f'Keys from {dic_json} are not equal to keys from {dic_json_lines}'

    oname = []
    txid = []
    filepath = []
    strain = []
    filetype = []

    for key in dic_json_lines.keys():
        oname.append(dic_json_lines[key]['organism']['organismName'])
        txid.append(dic_json_lines[key]['organism']['taxId'])
        if 'infraspecificNames' in dic_json_lines[key]['organism'].keys():
            strain.append(dic_json_lines[key]['organism']['infraspecificNames']['strain'])
        else:
            strain.append('NULL')

        filepath.append('/'.join(dic_json[key][0]['filePath'].split('/')[:-1]))
        filetype.append(dic_json[key][0]['fileType'])

    list_of_tuples = list(zip(oname, strain, txid, filepath, filetype))
    table = pd.DataFrame(list_of_tuples, \
            columns = ['OrganismName', 'Strain', 'TaxId', 'FilePath', 'FileType'])

    return table
    

