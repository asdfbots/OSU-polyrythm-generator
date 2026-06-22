from bpm_changer import bpm_change
from parser import (osu_parser, chunker,
                     hitobject_time_replace,
                     timepoint_time_replace,
                     timepoints_create,
                     merge_timepoints)

osu_map = osu_parser("metronome - 7 (Arkinght) [987].osu")
step = 2000
pattern = chunker(step, osu_map['time_list'])
print("bpm changing")
hit_object_list = osu_map['hit_obj']
timepoint_list = osu_map['timepoint_list']
# print(hit_object_list)
new_pattern = bpm_change(pattern, [0.5, 1], 2000)
# print(f'new pattern {len(new_pattern)}')
# print(f'hitobject {len(hit_object_list)}')

# print(new_pattern)
new_hitobjects = []
new_time_points = []
created_timepoints = []
timepoint_counter = 0
obj_couter = 0
print(len)
for count, chunk in enumerate(new_pattern):
    chunk_bpm, events = chunk
    created_timepoints.append(timepoints_create(events[1][1], chunk_bpm))
    for (is_obj, time, bpm) in events:
        if is_obj == True:
            # print(len(new_pattern))
            # print(len(hit_object_list))
            if len(hit_object_list) > obj_couter:
                new_hitobjects.append(hitobject_time_replace(time, hit_object_list[obj_couter]))
                obj_couter+=1
        if is_obj == False:
            new_time_points.append(timepoint_time_replace(time, bpm, timepoint_list[timepoint_counter]))
            timepoint_counter += 1

with open("objects.txt", "w") as file:
    txt_new_hitobjects = ''.join(new_hitobjects)
    file.write(txt_new_hitobjects)
        
with open("timepoints.txt", "w") as file:
    txt_new_time_points = ''.join(new_time_points)
    file.write(txt_new_time_points)
with open("new_points.txt", 'w') as file:
    timepoints_bpm_changer =  ''.join(created_timepoints)
    file.write(timepoints_bpm_changer)
with open("all_tp.txt", "w") as file:
    file.write(merge_timepoints(new_time_points, created_timepoints))