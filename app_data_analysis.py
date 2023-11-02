import numpy as np
import pandas as pd
import json
from collections import defaultdict
import os
import json
import statsmodels.stats.multitest as multi
from datetime import timedelta

ids = [11, 13, 14, 15, 19, 20, 22, 23, 24, 26, 29, 30, 
       101, 102, 103, 104, 105, 106, 108, 110, 114, 115, 118]

# How I read the data in folder Used to verify no duplicate problems etc - output in folder Summary
# clean_data = {str(i) : defaultdict(list) for i in ids}
# for path in os.listdir('/home/ydemetri/SR_logs/ActionLogs'):
#     data = {}
#     if '.json' in path:
#         with open("ActionLogs/" + path) as json_file:
#             data = json.load(json_file)
#         if int(data['user_id']) in ids:
#             clean_data[data['user_id']]['dates'].append(data['date'])
#         for key in data.keys():
#             if int(data['user_id']) in ids and 'Problem' in key:
#                 for sub_key in data[key].keys():
#                     if sub_key in ['problem_id', 'time_began', 'time_completed', 'check_answer_frequency']:
#                         clean_data[data['user_id']][sub_key].append(data[key][sub_key])

# clean_data = {k: v for k, v in clean_data.items() if v!=defaultdict(list)}

# data_df = pd.DataFrame.from_dict(clean_data, orient='index')
# for row in data_df.index:
#     user_df = data_df.loc[row]
#     user_df.to_csv('/home/ydemetri/SR_logs/{}_data.csv'.format(row))

paths = os.listdir('C:\\Users\\Yiannos\\Documents\\VR_stuff\\Analysis\\copy\\ActionLogs')
sorted_paths = []
for path in paths:
    data = {}
    if '.json' in path:
        with open("ActionLogs\\" + path) as json_file:
            data = json.load(json_file)
        sorted_paths.append((int(data['user_id']), path))

sorted_paths.sort()

time_data = {i : [] for i in range(1,116)}
answer_check_data = {i : [] for i in range(1,116)}
time_on_feedback = {i : [] for i in range(1,116)}

for path in sorted_paths:
    data = {}
    if '.json' in path[1]:
        with open("ActionLogs\\" + path[1]) as json_file:
            data = json.load(json_file)
        for prob in range(1,116):
            if "Problem {}".format(prob) in data.keys():
                start = data["Problem {}".format(prob)]['time_began'].split(':')
                end = data["Problem {}".format(prob)]['time_completed'].split(':')
                t1 = timedelta(hours=int(start[0]), minutes=int(start[1]), seconds=int(start[2]))
                t2 = timedelta(hours=int(end[0]), minutes=int(end[1]), seconds=int(end[2]))
                time_diff = t2 - t1
                time_data[prob].append(time_diff.total_seconds())
                num_checked = data["Problem {}".format(prob)]['check_answer_frequency']
                answer_check_data[prob].append(num_checked)
                if num_checked > 1:
                    total_time = 0
                    for i in range(num_checked - 1):
                        check_answer_list = data["Problem {}".format(prob)]['check_answer_timestamps']
                        try_again_list = data["Problem {}".format(prob)]['try_again_timestamps']
                        if len(check_answer_list) - 1 == len(try_again_list):
                            s = check_answer_list[i].split(':')
                            e = try_again_list[i].split(':')
                            ts = timedelta(hours=int(s[0]), minutes=int(s[1]), seconds=int(s[2]))
                            te = timedelta(hours=int(e[0]), minutes=int(e[1]), seconds=int(e[2]))
                            time_d = te - ts
                            total_time += time_d.total_seconds()
                    time_on_feedback[prob].append(total_time)
                else:
                    time_on_feedback[prob].append(np.nan)
            else:
                time_data[prob].append(np.nan)
                answer_check_data[prob].append(np.nan)

time_df = pd.DataFrame.from_dict(time_data, orient='index')
answer_check_df = pd.DataFrame.from_dict(answer_check_data, orient='index')
time_on_feedback = pd.DataFrame.from_dict(time_on_feedback, orient='index')

time_df.columns = ids
answer_check_df.columns = ids
time_on_feedback.columns = ids
time_df.index = range(1,116)
answer_check_df.index = range(1,116)
time_on_feedback.index = range(1,116)
time_df = time_df.drop(index=[38,41,42,81,83]) # drop problems that had a bug


time_df.to_csv('time.csv', index=False)
answer_check_df.to_csv('answer_check.csv', index=False)
time_on_feedback.to_csv('time_on_feedback.csv', index=False)


