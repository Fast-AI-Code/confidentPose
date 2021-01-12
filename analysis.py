import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx

def rot_90(l):
    return [-l[1],-l[0]]

rel = [
    ['leftElbow', 'leftWrist'],
    ['leftShoulder', 'leftElbow'],
    ['leftShoulder', 'rightShoulder'],
    ['leftEar', 'rightEar'],
    ['leftEye', 'rightEye'],
    ['nose', 'rightEye'],
    ['leftEye', 'nose'],
    ['rightElbow', 'rightWrist'],
    ['rightShoulder', 'rightElbow'],
    ['leftHip', 'leftKnee'],
    ['leftKnee', 'leftAnkle'],
    ['rightHip', 'rightKnee'],
    ['rightKnee', 'rightAnkle'],
]

files = os.listdir("./ouput_stream/")

# Read files and make them into a dataframe
def initialize():
    temp_frames = [pd.read_csv("./ouput_stream/"+i, names = [f"{i}_x", f"{i}_y"]) for i in files]
    concat_file = pd.DataFrame()
    # concatenate values for each point
    for i in temp_frames:
        concat_file = pd.concat([concat_file, i],axis = 1)
    dict_vals = {}
    for i,f in enumerate(files):
        ind = 2*i
        dict_vals[f] = concat_file.iloc[:,ind:ind+2]
    return dict_vals

# General math operation
def perform_x(dict_vals, fname = 'mean'):
    avg_lis = []
    for i in files:
        op_dict = {'mean': dict_vals[i].mean().values, 'min': dict_vals[i].min().values, 'max': dict_vals[i].max().values}
        calc = op_dict[fname]
        avg_lis.append(tuple(calc)) # change this if needed
    df2 = pd.DataFrame(avg_lis,index = [x.split(".")[0] for x in files]); df2=df2.reset_index();df2
    dict_vals = df2.set_index('index').T.to_dict('list');dict_vals
    G = nx.Graph()
    for i in dict_vals:
        G.add_node(i, pos = tuple(rot_90(dict_vals[i])))
    G.add_edges_from(rel)
    plt.figure(figsize=(6,12))
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=0)
    plt.savefig(f"./graph_gen-{fname}.png")

dict_vals = initialize()
perform_x(dict_vals, 'mean')
perform_x(dict_vals, 'max')
perform_x(dict_vals, 'min')
