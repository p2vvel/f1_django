def group_elements(data, index_key=lambda x: x[0], value_key=lambda x: x[1]):
    '''
    Grupuje elementy w pary (index, [wartosci odpowiadajace danemu indeksowi])
    '''
    indexes = set([index_key(k) for k in data])
    result = {k: [] for k in indexes}
    for k in data:
        result[index_key(k)].append(value_key(k))
    return list(result.items())


def fill_empty_races(races: list, races_count: int) -> list:
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
        return fill


def get_country_code(country_name):
    codes = {
        'Argentina': 'ar',
        'Australia': 'au',
        'Austria': 'at',
        'Azerbaijan': 'az',
        'Bahrain': 'bh',
        'Belgium': 'be',
        'Brazil': 'br',
        'Canada': 'ca',
        'China': 'cn',
        'France': 'fr',
        'Germany': 'de',
        'Hungary': 'hu',
        'India': 'in',
        'Italy': 'it',
        'Japan': 'jp',
        'Korea': 'kr',
        'Malaysia': 'my',
        'Mexico': 'mx',
        'Monaco': 'mc',
        'Morocco': 'ma',
        'Netherlands': 'nl',
        'Portugal': 'pt',
        'Russia': 'ru',
        'Saudi Arabia': 'sa',
        'Singapore': 'sg',
        'South Africa': 'za',
        'Spain': 'es',
        'Sweden': 'se',
        'Switzerland': 'ch',
        'Turkey': 'tr',
        'UAE': 'ae',
        'UK': 'gb',
        'USA': 'us',
        'Vietnam': 'vn'
    }

    return codes[country_name]