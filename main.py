from bpm_changer import bpm_change
from parser import osu_parser, chunker, hitobject_time_replace, timepoint_time_replace

osu_map = osu_parser("Megurine Luka - LukaLuka Night Fever (samipale) [MoNky's BeaT].osu")

pattern = chunker(1000, osu_map['time_list'])
print("bpm changing")
hit_object_list = osu_map['hit_obj']
timepoint_list = osu_map['timepoint_list']
# print(hit_object_list)
new_pattern = bpm_change(pattern)
# print(f'new pattern {len(new_pattern)}')
# print(f'hitobject {len(hit_object_list)}')

# print(new_pattern)
new_hitobjects = []
new_time_points = []
timepoint_counter = 0
for count, chunk in enumerate(new_pattern):
    chunk_bpm, events = chunk
    print(chunk_bpm)
    for (is_obj, time, bpm) in events:
        if is_obj == True:
            # print(len(new_pattern))
            # print(len(hit_object_list))
            new_hitobjects.append(hitobject_time_replace(time, hit_object_list[count]))
        if is_obj == False:
            new_time_points.append(timepoint_time_replace(time, bpm, timepoint_list[timepoint_counter]))
            timepoint_counter += 1
with open("objects.txt", "w") as file:
    new_hitobjects = ''.join(new_hitobjects)
    file.write(new_hitobjects)
        
with open("timepoints.txt", "w") as file:
    new_time_points = ''.join(new_time_points)
    file.write(new_time_points)
        