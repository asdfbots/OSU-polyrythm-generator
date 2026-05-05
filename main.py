from bpm_changer import bpm_change
from parser import osu_parser, chunker, hitobject_time_replace, timepoint_time_replace

osu_map = osu_parser("Megurine Luka - LukaLuka Night Fever (samipale) [MoNky's BeaT].osu")

pattern = chunker(1000, osu_map['time_list'])
print(pattern)
print("bpm changing")
print("bpm changing")
print("bpm changing")
print("bpm changing")
hit_object_list = osu_map['hit_obj']
timepoint_list = osu_map['timepoint_list']
# print(hit_object_list)
new_pattern = bpm_change(pattern)

# print(new_pattern)
new_hitobjects = []
new_time_points = []
timepoint_counter = 0
for count, chunk in enumerate(new_pattern):
    for is_obj, time in chunk:
        if is_obj == True:
            new_hitobjects.append(hitobject_time_replace(time, hit_object_list[count]))
        if is_obj == False:

            print(timepoint_list[timepoint_counter])
            new_time_points.append(timepoint_time_replace(time, timepoint_list[timepoint_counter]))
            timepoint_counter += 1
with open("objects.txt", "w") as file:
    new_hitobjects = ''.join(new_hitobjects)
    file.write(new_hitobjects)
        
with open("timepoints.txt", "w") as file:
    new_time_points = ''.join(new_time_points)
    file.write(new_time_points)
        