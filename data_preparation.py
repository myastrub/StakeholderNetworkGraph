from multiprocessing import connection
import pandas as pd
import numpy as np
import os
import constants as c

RIT_TABLE_FILE = os.path.join('datasets', 'RIT_STK.xls')
SVC_FILE = os.path.join('datasets', 'SVC-to-CAP.xls')
URL_IMAGE = os.path.join('assets', 'stk.png')



def generate_data_for_graph(dataset):
    elements = list(set(dataset[c.SOURCE_STK].unique()).union(
        dataset[c.TARGET_STK].unique()
    ))
    conn_frame = dataset[[c.SOURCE_STK, c.TARGET_STK]].drop_duplicates()
    connections = conn_frame.to_dict(orient='records')
    nodes = [{
        'data': {
            'id': item,
            'label': item,
            'url': URL_IMAGE
            }
    } for item in elements]
    edges = [{
        'data': {'source': item[c.SOURCE_STK], 'target': item[c.TARGET_STK]}
    }
    for item in connections
    ]
    return nodes + edges


def get_capabilities(dataset, level=2):
    if level == 2:
        return sorted(list(dataset[c.L2_CAP].unique()))
    elif level == 1:
        return sorted(list(dataset[c.L1_CAP].unique()))
    else:
        return sorted(list(dataset[c.L3_CAP].unique()))


rit_frame = pd.read_excel(RIT_TABLE_FILE)
svc_to_cap_frame = pd.read_excel(SVC_FILE)

# preparation of Resource Interaction Table
services_frame = rit_frame[rit_frame[c.INTERACTION_TYPE].eq('Service')]
services_frame = services_frame[[c.SVC, c.SOURCE_STK, c.TARGET_STK]]
services_frame = services_frame.dropna(subset=[c.SOURCE_STK, c.TARGET_STK])
services_frame = services_frame.drop_duplicates()

# preparation of SVC to Capability dataset
svc_to_cap_frame = svc_to_cap_frame[svc_to_cap_frame[c.OWNER].eq('Service')]
svc_to_cap_frame = svc_to_cap_frame.dropna()

# merge of the dataset
services_dataset = svc_to_cap_frame.merge(
    services_frame, left_on=c.SVC, right_on=c.SVC, how='inner'
)

generate_data_for_graph(services_dataset)