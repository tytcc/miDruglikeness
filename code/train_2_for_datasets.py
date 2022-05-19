import os
import sys
import numpy as np
import pandas as pd
import torch

import pandas as pd
import numpy as np
import torch

# np.random.seed(33)
torch.manual_seed(3)
torch.cuda.manual_seed(3)


from chemprop.data import MoleculeDataset

from model_GNN_2 import train_GNN
from rdkit import Chem

import warnings
warnings.filterwarnings('ignore')

from time import clock
import pandas as pd

def rm_dup_smi(wdi, zinc):
    '''
    wdi:  negative
    zinc: positive
    '''
    smi_wdi = [Chem.MolToSmiles(x, isomericSmiles=False) for x in wdi.mols()]
    smi_zinc = [Chem.MolToSmiles(x, isomericSmiles=False) for x in zinc.mols()]
    idx = []
    for i in range(len(smi_wdi)):
        if smi_wdi[i] not in smi_zinc:
            idx.append(i)
    temp=np.array(wdi)[idx]
    return MoleculeDataset(temp)

def rm_du(data):
    smi=[Chem.MolToSmiles(x,isomericSmiles=False) for x in data.mols()]
    hash=dict()
    add_idx=[]
    for i,x in enumerate(smi):
        if x not in hash.keys():
            hash[x]=i
            add_idx.append(i)
    temp = np.array(data)[add_idx]
    return MoleculeDataset(temp)


def split_train_GNN_predict(args,logger,path_save,n):
    seed=34
    # results_all_list=[[],[],[],[],[],[],[],[],[],[]]
    results_all_list=[[],[],[],[],[]]
    for i in range(5):
        args.fold=i
        # i=args.fold
        path_save_new=path_save+'/fold_'+str(i)+'/'
        print(path_save_new)
        try:
            os.mkdir(path_save_new)
        except FileExistsError:
            pass

        # for chemprop
        if args.data_path:
            # Get data
            # debug('Loading data')
            args.task_names = args.target_columns or get_task_names(args.data_path)
            # data = get_data(path=args.data_path, features_path=args.features_path,args=args)
            # args.num_tasks = data.num_tasks()
            # args.features_size = data.features_size()
            # debug(f'Number of tasks = {args.num_tasks}')

            # Split data
            # debug(f'Splitting data with seed {args.seed}')
            if args.separate_test_path:
                # test_data = get_data(path=args.separate_test_path, args=args,
                #                      features_path=args.separate_test_features_path,target_columns=['label_world','label_intrials','label_invivo'])
                test_data = get_data(path=args.separate_test_path, args=args,
                                     features_path=args.separate_test_features_path,target_columns=['label'],smiles_column='smiles')
                args.num_tasks = test_data.num_tasks()
                args.features_size = test_data.features_size()
            if args.separate_val_path:
                val_data = get_data(path=args.separate_val_path, args=args, features_path=args.separate_val_features_path)

            if args.separate_val_path and args.separate_test_path:
                train_data = data
            # elif args.separate_val_path:
            #     train_data, _, test_data = split_data(data=data, split_type=args.split_type, sizes=(0.8, 0.0, 0.2),
            #                                           seed=args.seed+i, args=args)
            # elif args.separate_test_path:
            #     train_data, val_data, _ = split_data(data=data, split_type=args.split_type, sizes=(0.8, 0.2, 0.0),
            #                                          seed=seed+i, args=args)
            # else:
            #     train_data, val_data, test_data = split_data(data=data, split_type=args.split_type, sizes=args.split_sizes,
            #                                                  seed=seed+i, args=args)

            metric_list=['auc','mcc','gmeans','f1','accuracy','prc-auc']
            # metric_list = ['precision','recall']
            # metric_list = ['auc']

            # val_data remove duplicate
            ## remove duplicate with train data
            # val_data_rm=rm_dup_smi(val_data,train_data)
            # test_data_rm=rm_dup_smi(test_data,train_data)
            ## remove iso with myself
            # val_data_rm = rm_du(val_data_rm)
            # test_data_rm = rm_du(test_data_rm)
            
            # ## debug
            # print(len(test_data))

            # metric_list=['prc-auc']
            len_metric=len(metric_list)
            results = [[] for x in range(len_metric)]
            train_results=[[] for x in range(len_metric)]
            val_results=[[] for x in range(len_metric)]
            for round in range(1):
                args.round=round
                net = train_GNN(args)
                # temperature = joblib.load(os.path.join(args.save_dir, f'fold_{args.fold}',f'round_{args.round}','temperature'))
                temperature=[1]
                # temperature 计算

                for iteration in range(30,31):
                    # test_preds=net.predict_GNN_last_tem(test_data,iteration,temperature[iteration],args,logger)
                    # print(len(test_data))
                    # print(np.array(test_preds).shape)
                    test_preds = net.predict_GNN_last(test_data, iteration, args,logger)
                    # test_preds = net.predict_GNN_last(test_data_rm, iteration, args,logger)
                    # # temperature scaling
                    # test_preds_tem,test_preds,temps = net.predict_GNN_last_tem(test_data,val_data, iteration, temperature, args,logger)

                    # print(len(test_preds))
                    # print(test_preds[0])

                    # me = net.evaluate_GNN(test_preds, test_data, args, logger, metric_list)
                    # me = net.evaluate_GNN(test_preds, test_data_rm, args, logger, metric_list)

                    # train_preds = net.predict_GNN_last(train_data, iteration, args,logger)
                    # train_me = net.evaluate_GNN(train_preds, train_data, args, logger, metric_list)

                    # val_preds = net.predict_GNN_last(val_data_rm, iteration, args,logger)
                    # val_me = net.evaluate_GNN(val_preds, val_data_rm, args, logger, metric_list)

                    # val_preds = net.predict_GNN_last(val_data, iteration, args,logger)
                    # val_me = net.evaluate_GNN(val_preds, val_data, args, logger, metric_list)

                    # test_preds_tem,test_preds=np.array(test_preds_tem)[:,0],np.array(test_preds)[:,0]
                    # hard_test_preds,hard_test_preds_tem=copy.deepcopy(test_preds),copy.deepcopy(test_preds_tem)
                    # hard_test_preds[test_preds < 0.5]=0
                    # hard_test_preds[test_preds >= 0.5]=1
                    # hard_test_preds_tem[test_preds_tem < 0.5]=0
                    # hard_test_preds_tem[test_preds_tem >= 0.5]=1
                    #
                    # ece,acc_hist,conf_hist=get_log(test_preds,test_data.targets(),hard_test_preds)
                    # tem_ece,tem_acc_hist,tem_conf_hist=get_log(test_preds_tem,test_data.targets(),hard_test_preds_tem)

                    # try:
                    #     os.mkdir(path_save_new+str(round))
                    # except FileExistsError:
                    #     pass
                    # for mm in range(len_metric):
                    #     results[mm].append(me[metric_list[mm]])
                    #     # train_results.append(train_me[metric])
                    #     # val_results[mm].append(val_me[metric_list[mm]])


                    
            # for mm in range(len_metric):
            #     metric = metric_list[mm]
            #     if metric=='accuracy':
            #         metric='acc'
                # joblib.dump(results[mm],path_save_new+str(round)+'/'+metric)
                # joblib.dump(train_results, path_save_new + str(round) + '/' +'train_'+ metric)
                # joblib.dump(val_results[mm], path_save_new + str(round) + '/' + 'val_rm_'+metric)
                # joblib.dump(val_results[mm], path_save_new + str(round) + '/' + 'val_'+metric)
        # results_all[i]=test_preds
        # results_all_list[i]=test_preds_tem

        results_all_list[i]=test_preds

        # print(np.array(results_all).shape)
        # print(path_save_new+str(round)+'/'+metric)
    for model_idx in range(1):
        #
        results_all=np.array(results_all_list)[:,:,model_idx].transpose()

        data = pd.DataFrame(results_all.mean(axis=1),columns=['average'])
        data['smiles']=test_data.smiles()
        
        data.to_csv(args.outputfile,index=False)


    return results_all_list





# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# args = sys.argv
# print(args)
# args.pop(0)

from args import TrainArgs
from chemprop.data.utils import get_class_sizes, get_data, get_task_names, split_data
from chemprop.utils import create_logger
vari = {}
fold = False
regression = False
trained = False

args = TrainArgs().parse_args()
logger = create_logger(name='train', save_dir=args.save_dir, quiet=args.quiet)


path_save = args.s



# start training from here
if logger is not None:
    debug, info = logger.debug, logger.info
else:
    debug = info = print
info('Command line')
info(f'python {" ".join(sys.argv)}')

file_path = path_save
try:
    os.mkdir(file_path)
except FileExistsError:
    pass
# os.chdir(file_path)


m=30
results=split_train_GNN_predict(args,logger,path_save,m)
