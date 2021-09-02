def group_elements(data, index_key=lambda x: x[0], value_key=lambda x: x[1]):
    '''
    Grupuje elementy w pary (index, [wartosci odpowiadajace danemu indeksowi])
    '''
    indexes = set([index_key(k) for k in data])
    result = {k: [] for k in indexes}
    for k in data:
        result[index_key(k)].append(value_key(k))
    return list(result.items())

def fill_empty_races(races:list, races_count: int) -> list:
    '''
    W przypadku tabeli z wyscigami mialem problem z wyswietlaniem kierowcow, 
    ktorzy nie brali udzialu we wszystkiuch wyscigach sezonu(tabela sie rozjezdzala)
    Ta funkcja dodaje None do listy wyscigow kierwocy i przy okazji wszystko ustawia w dobrej
    kolejnosci, dzieki czemu przenosze prawie cala logike rysowania tej tabeli z 
    szablonu do widoku
    '''
    if len(races) == races_count:
        return races
    else:
        fill = [None] * (races_count - len(races))
        for race in races:
            fill.insert(race.race.round - 1, race)
        print(fill)
        return fill