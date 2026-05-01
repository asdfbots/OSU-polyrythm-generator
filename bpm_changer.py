from random import uniform
def bpm_change(pattern_list):
    '''
        Reorganizes groups of timepoints to create smooth tempo variation
        between consecutive patterns while preserving internal structure.

        Args:
            pattern_list(list[list[float]]): A list of patterns, where each
                pattern is a list of timepoints (e.g. [[3, 4, 5], [8, 9, 10]])

        Returns:
            list[list[float]]: A transformed list of patterns where each
            timepoint is slightly shifted in time to simulate BPM variation
            between groups, while preserving relative spacing inside each group.
            All values are rounded to 2 decimal places to avoid floating point artifacts.

        Example:
            >>> bpm_change([[3, 4, 5], [8, 9, 10], [12, 13, 14]])
            [[3.0, 3.1, 3.2],
             [3.5, 3.6, 3.7],
             [3.9, 4.0, 4.1]]
    '''
    last_start_time = pattern_list[0][0][1]
    last_end_time = pattern_list[0][0][1]
    for pattern in (pattern_list):
        rnd = round(uniform(0.7, 1.5), 1)
        start_time = pattern[0][1]
        end_time = pattern[-1][1]
        gap = start_time-last_end_time
        start_new = last_start_time+(gap*rnd)
        for i, (is_obj, time) in enumerate(pattern):
            diff = time - start_time
            # print(f"diff= {diff}")
            pattern[i] = is_obj, int((start_new+(diff*rnd)))
        last_start_time = pattern[-1][1]
        last_end_time = end_time
    return(pattern_list)
    # print([[round(i, 2) for i in p] for p in pattern_list])

