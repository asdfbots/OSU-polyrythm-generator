def osu_parser(path:str):
    """
    Parses an .osu beatmap file and extracts hit object timestamps.

    Args:
        path(str): Path to the .osu file.

    Returns:
        tuple[list[int], list[str], list[str]]: List of hit object times, hit objects and timepoints.
    """

    hitobject = False
    hitobjects_list = []
    timepoint = False
    timepoints_list = []
    beatmap_path = path
    with open(beatmap_path, "r") as beatmap_file:
        for line in beatmap_file:
            if line == "[TimingPoints]\n":
                timepoint = True
                continue
            if line == "\n":
                timepoint = False
            if timepoint == True:
                timepoints_list.append(line)
            if line == "[HitObjects]\n":
                print("hitobject founded")
                hitobject = True
                continue
            if hitobject == True:
                hitobjects_list.append(line)

    # print(hitobjects_list[1])
    # print("split")
    time_list = []
    point_list = []
    for i in hitobjects_list:
        # print(f"in proccess hit_obj{hitobj_list}")
        hitobject_parts = i.split(',')
        time = hitobject_parts[2]
        time = int(time)
        hit_obj = (True, int(time), None)
        time_list.append(hit_obj)
    for i in timepoints_list:
        timepoint_parts = i.split(',')
        time = timepoint_parts[0]
        bpm = int(60000/int(timepoint_parts[1]))
        time = int(time)
        point_obj = (False, time, bpm if bpm >0 else None)
        time_list.append(point_obj)
        point_list.append(i)
        time_list.sort(key=lambda x: (x[1], x[0]))
    # print(time_list)
    return({"time_list": time_list, "hit_obj":hitobjects_list, "timepoint_list":point_list})

def chunker(time_step:int, time_list:list):
    '''
        Splits list in to chunks.
        Args:
            time_step(int): Step and size of chunk
            time_list(list): take list of nums and splits by time_step
        Returns:
            list[list[int]] list of chunks, each include times in range of one time_step
        Example:
            >>> chunking(200,[(True, 100), (True, 200), (False, 400), (True, 600), (False, 700), (True, 800)])
            [[(True, 100), (True, 200)], [(False, 400], [(True, 600), False, 700)], [(True, 800)]]
    '''
    times = time_list
    # print(times)
    time_range = time_step
    step = time_range
    temp = []
    chunk_list = []
    chunk_bpm = 0
    for is_obj, time, bpm in times:
        if is_obj == False and bpm != None:
            chunk_bpm = bpm
        if time <= time_range:

            # print(f"i = {i}")
            # print(f"range = {time_range}")
            temp.append((is_obj, time, bpm))
            if times[-1] == time:
                chunk_list.append([chunk_bpm, temp])
        else:
            if temp:
                chunk_list.append([chunk_bpm, temp])
            while time > time_range:
                time_range += step
            temp=[(is_obj, time, bpm)]

            if times[-1] == time:
                chunk_list.append([chunk_bpm, temp])

    return(chunk_list)


def hitobject_time_replace(time:int, hitobject:str):
    '''
    Replacing original time on different
    Args:
        time(int): new time value
        hitobject(str): hitobject that will be changed
    Returns:
        str: updated hitobject string
    Example:
        >>> hitobject_time_replace(100, '256,53,0,5,0,0:0:0:0:')
        "256,53,100,5,0,0:0:0:0:"
    '''
    hitonbject_split = hitobject.split(',')
    hitonbject_split[2] = str(time)
    # print(hitonbject_split)
    return(','.join(hitonbject_split))

def timepoint_time_replace(time, bpm, timepoint):
    '''
    Replacing original time on different
    Args:
        time(int): new time value
        bpm(int): new bpm
        timepoint(str): timepoint that will be changed
    Returns:
        str: updated timepoint string
    Example:
        >>> hitobject_time_replace(100, None, '1387,-100,4,2,0,80,0,0')
        "100,-100,4,2,0,80,0,0"
    '''
    timepoint_parts = timepoint.split(',')
    timepoint_parts[0] = str(time)
    if bpm != None:
        bpm = 60000/bpm
        timepoint_parts[1] = str(bpm)
    return(','.join(timepoint_parts))



# print(hitobject_time_replace(100, '256,53,0,5,0,0:0:0:0:'))
# print(chunking(20000, osu_parser("Megurine Luka - LukaLuka Night Fever (samipale) [MoNky's BeaT].osu")))


