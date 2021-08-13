def group_elements(data, index_key=lambda x: x[0], value_key=lambda x: x[1]):
    '''
    Grupuje elementy w pary (index, [wartosci odpowiadajace danemu indeksowi])
    '''
    indexes = set([index_key(k) for k in data])
    result = {k: [] for k in indexes}
    for k in data:
        result[index_key(k)].append(value_key(k))
    return list(result.items())