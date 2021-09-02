import pydmps
import pydmps.dmp_discrete

import json 
import numpy as np

import os

def get_weights_of_dmps( json_filepaths, json_key ):

    """
    - reads the json files from the data set 
    - reads specific keys to get joint position
      though we recorded joint velocities as well
      but pyDMP uses central differences to get 
      velocities and acceleration. 

    * returns -> dmp weights 
    """

    dmps = []
    for json_path in json_filepaths:

        data = ""
        with open(json_path, 'r') as read_file:
            data = json.load(read_file)
        if data != "":

            positions = np.array( data[json_key] )  
            # remove gripper positions
            positions = positions[:, : 7].T 

            n_dmps = positions.shape[0]
            n_bfs = 100
            gain_multiplier = 100
            y0 = positions[:, 0] # trajectory start point
            goal = positions[:, -1] # trajectory end point

            dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps= n_dmps, n_bfs=n_bfs, ay=np.ones(n_dmps) * gain_multiplier)
            dmp.imitate_path(y_des=positions, plot=False)
            
            dmps.append( dmp )



def get_trajectories_of_dmps( weigths ):

    """
    - pass in the weights of 7 DMPS (for each joint) 
      it will create DMPs 
    """



if __name__ == '__main__':


    data_folder_path = ""
    files = os.listdir(data_folder_path)
    files = [os.path.join(data_folder_path, f) for f in files if '.json' in f]

    get_weights_of_dmps(files, 'joint_positions')