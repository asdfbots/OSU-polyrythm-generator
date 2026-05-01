from bpm_changer import bpm_change
from parser import osu_parser, chunker, hitobject_time_replace

osu_map = osu_parser("Memeoz - aim training (Memeoz) [100 BPM Spinning Jump 1].osu")

pattern = chunker(1000, osu_map['time_list'])
print(pattern)
print("bpm changing")
print("bpm changing")
print("bpm changing")
print("bpm changing")
hit_object_list = osu_map['hit_obj']
# print(hit_object_list)
new_pattern = bpm_change(pattern)

print(new_pattern)
new_hitobjects = []
for count, chunk in enumerate(new_pattern):

    for is_obj, note in chunk:
        if is_obj == True:
            new_hitobjects.append(hitobject_time_replace(note, hit_object_list[count]))
    
with open("objects.txt", "w") as file:
    new_hitobjects = ''.join(new_hitobjects)
    file.write(new_hitobjects)
            
