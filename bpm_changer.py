from random import uniform
def bpm_change(pattern_list):
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
    last_start_time = pattern_list[0][1][0][1]
    last_end_time = pattern_list[0][1][0][1]
    for chunk_count, [chunk_bpm, pattern] in enumerate(pattern_list):

        rnd = round(uniform(0.7, 1.5), 1)
        start_time = pattern[0][1]
        end_time = pattern[-1][1]
        gap = start_time-last_end_time
        start_new = last_start_time+(gap*rnd)
        pattern_list[chunk_count][0] = int(chunk_bpm*rnd)
        for i, (is_obj, time, bpm) in enumerate(pattern):
            diff = time - start_time
            # print(f"diff= {diff}")

            pattern[i] = is_obj, int((start_new+(diff*rnd))), bpm*rnd if bpm != None else None
        last_start_time = pattern[-1][1]
        last_end_time = end_time
    return(pattern_list)
    # print([[round(i, 2) for i in p] for p in pattern_list])

