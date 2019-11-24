from constants import GRADE_LEVELS, STATE_ABBREVS, STATE_NAMES

def grade_level_string(grLvlCode):
    for lvl in GRADE_LEVELS:
        code, string = lvl
        if grLvlCode == code:
            return string
    return None

def state_abbrev_to_name(abbrev):
    return STATE_NAMES[STATE_ABBREVS.index(abbrev)]


