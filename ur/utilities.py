def max_index(_list):
    """
    Returns the index of the maximum element in the list
    :param _list: the list
    :return: The index of the maximum element in the list
    """

    best_index = 0
    best_value = _list[0]

    for i, val in enumerate(_list):
        if val > best_value:
            best_value = val
            best_index = i

    return best_index
