from random import choice
def bpm_change(pattern_list, temp_list, step):
    '''
        Reorganizes groups of timepoints to create smooth tempo variation
        between consecutive patterns while preserving internal structure.

        Args:
            pattern_list(list[list[tuple(boolean, int)]]): A list of patterns, where each
                pattern is a list of timepoints (e.g. [[(True, 3), (False, 4), (True, 5)], [(False, 8), (False, 9), (True, 10)]])

        Returns:
            list[list[Tuple(Boolean, Tuple)]]: A transformed list of patterns where each
            timepoint is slightly shifted in time to simulate BPM variation
            between groups, while preserving relative spacing inside each group.
            All values are rounded to 2 decimal places to avoid floating point artifacts.

        Example:
            >>> bpm_change([[(True, 3), (False, 4), (True, 5)], [(False, 8), (True, 9), (False, 10)], [(True, 12), (False, 13), (True, 14)]])
            [[(True, 3), (False, 3), (True, 4)],
             [(False, 5), (True, 5), (False, 6)],
             [(True, 6), (False, 7), (True, 7)]]
    '''
    rnd_list = []
    current_uscaled = 0
    current_chaged = 0
    rnd = 1
    for chunk_count, [chunk_bpm, pattern] in enumerate(pattern_list):
        if chunk_bpm == -10:
            if rnd != 0:
                rnd_list.append(1/rnd)
            current_uscaled += step
            current_chaged += step*rnd
        rnd = choice(temp_list)
        rnd_list.append(1/rnd)
        pattern_list[chunk_count][0]=int(chunk_bpm*rnd)
        for i, (is_obj, time, bpm) in enumerate(pattern):
            diff = time-current_uscaled
            # print(f"diff= {diff}")
            new_time = int(current_chaged + (diff * rnd))
            pattern[i] = is_obj, new_time, bpm*rnd if bpm != None else None

        current_uscaled += step
        current_chaged += (step * rnd)
    print(rnd_list)
    return(pattern_list)
    # print([[round(i, 2) for i in p] for p in pattern_list])