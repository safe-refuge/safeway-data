from typing import Set


CATEGORIES: Set[str] = {
    'Clothes',
    'Accommodation',
    'Medical',
    'Border Crossing',
    'Pharmacy',
    'Finance',
    'Information',
    'Mental help',
    'Transport',
    'Food',
    'Electronics',
    'Children',
    'Social help',
    'Any help',
    'Disability support',
    'Pets',
    'Water',
    'Jobs',
    'Education',
    'LGBTQ+'
}

DEFAULT_CATEGORY: str = 'Any help'


if __name__ == '__main__':
    for category in CATEGORIES:
        print(f' - {category}')
