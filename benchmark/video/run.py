"""
[file]          run.py
[description]   
"""
#
##
import json
import time
import torch
from sklearn.model_selection import train_test_split

from model import *
from preset import preset
from load_data import load_data_y, VideoDataset


#
##
def main_0(var_pretrain = True):
    #
    ##
    print(preset)
    #
    ##
    data_pd_y = load_data_y(preset["path"]["data_y"],
                            var_environment = preset["data"]["environment"], 
                            var_num_users = preset["data"]["num_users"])
    #
    data_train_pd_y, data_test_pd_y = train_test_split(data_pd_y, 
                                                       test_size = 0.2, 
                                                       shuffle = True, 
                                                       random_state = 39)
    #
    data_train_set = VideoDataset(preset["path"]["data_pre_x"], data_train_pd_y, preset["task"])
    data_test_set = VideoDataset(preset["path"]["data_pre_x"], data_test_pd_y, preset["task"])
    #
    ##
    if var_pretrain:
        #
        result, var_weight = run_resnet(data_train_set, 
                                        data_test_set,
                                        var_repeat = preset["nn"]["repeat"])
        #
        result["data"] = preset["data"]
        result["nn"] = preset["nn"]
        #
        print(result)
        #
        var_file = open(preset["path"]["save_result"], 'w')
        json.dump(result, var_file, indent = 4)
        #
        torch.save(var_weight, preset["path"]["save_model"])
    #
    ##
    else:
        #
        result, _ = run_resnet(data_train_set, 
                               data_test_set,
                               var_repeat = preset["nn"]["repeat"],
                               var_weight = preset["path"]["save_model"])
        #
        result["data"] = preset["data"]
        result["nn"] = preset["nn"]
        #
        print(result)
        #
        var_file = open(preset["path"]["save_result"], 'w')
        json.dump(result, var_file, indent = 4)


if __name__ == "__main__":
    #
    ##
    # main_0()
    #
    preset["task"] = "identity"
    preset["nn"]["repeat"] = 1
    preset["nn"]["epoch"] = 10
    preset["data"]["environment"] = ["meeting_room"]
    preset["path"]["save_result"] = "result_identity_resnet_meeting_pre.json"
    preset["path"]["save_model"] = "model_identity_resnet_meeting.pt"
    main_0(var_pretrain = True)
    #
    preset["nn"]["repeat"] = 10
    preset["nn"]["epoch"] = 1
    preset["path"]["save_result"] = "result_identity_resnet_meeting.json"
    main_0(var_pretrain = False)


    #
    preset["task"] = "identity"
    preset["nn"]["repeat"] = 1
    preset["nn"]["epoch"] = 10
    preset["data"]["environment"] = ["empty_room"]
    preset["path"]["save_result"] = "result_identity_resnet_empty_pre.json"
    preset["path"]["save_model"] = "model_identity_resnet_empty.pt"
    main_0(var_pretrain = True)
    #
    preset["nn"]["repeat"] = 10
    preset["nn"]["epoch"] = 1
    preset["path"]["save_result"] = "result_identity_resnet_empty.json"
    main_0(var_pretrain = False)

