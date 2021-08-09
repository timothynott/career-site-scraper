import re
from itemloaders.processors import TakeFirst

JOB_LEVELS_PATTERNS = {
    'ENTRY': 'entry',
    'JUNIOR': r'jun(ior)?',
    'MID': r'mid(dle)?',
    'SENIOR': 'senior',
}
JOB_TYPES_PATTERNS = {
    'FULL_TIME': r'full[_ -]?time',
    'PART_TIME': r'part[_ -]?time',
    'CONTRACT': 'contract',
    'INTERN': 'intern',
}
SHIFTS_PATTERNS = {
    'FIRST': r'(1-?st|first)',
    'SECOND': r'(2-?nd|second)',
    'THIRD': r'(3-?rd|third)',
}

def search_patterns(patterns, values):
    for value in values:
        for key, pattern in patterns.items():
            if re.search(rf'\b{pattern}\b', value, re.I):
                yield key

def job_level_proc(values):
    for value in search_patterns(JOB_LEVELS_PATTERNS, values):
        return value

def job_type_proc(values):
    for value in search_patterns(JOB_TYPES_PATTERNS, values):
        return value

def shifts_proc(values):
    return list(search_patterns(SHIFTS_PATTERNS, values))

def wage_proc(values):
    for value in values:
        try:
            wage = float(value)
            if wage > 0:
                return wage
        except ValueError:
            continue

def description_proc(values):
    return re.sub(
        r'\s+',
        ' ',
        ' '.join(filter(None, values)).replace('\n', ' ')
    )
