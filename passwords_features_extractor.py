import csv
import string
import argparse
import re

def has_sequential_chars(password):
    """Check if password has sequential characters."""
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    for i in range(len(alphabets)-2):
        if alphabets[i:i+3] in password.lower():
            return True
        if digits[i:i+3] in password:
            return True
    return False

def has_repeated_patterns(password):
    """Check if password has repeated patterns."""
    for i in range(1, len(password)//2 + 1):
        pattern = re.compile(r'(.{%d})\1' % i)
        if pattern.search(password):
            return True
    return False

def char_diversity(password):
    """Calculate character diversity."""
    unique_chars = set(password)
    return len(unique_chars) / len(password) if password else 0

def contains_leetspeak(password):
    """Check if the password uses leetspeak."""
    leetspeak_mapping = {'4': 'a', '3': 'e', '0': 'o', '$': 's', '7': 't'}
    for k, v in leetspeak_mapping.items():
        password = password.replace(k, v)
    return password != password

def calculate_entropy(password):
    """Calculate the entropy of the password."""
    from collections import Counter
    import math
    if not password:
        return 0
    probability = [freq / len(password) for freq in Counter(password).values()]
    entropy = -sum(p * math.log2(p) for p in probability)
    return entropy

def contains_keyboard_patterns(password):
    """Check for patterns that are common on a keyboard."""
    keyboard_rows = [
        '1234567890',
        'qwertyuiop',
        'asdfghjkl',
        'zxcvbnm'
    ]

    def generate_patterns(rows):
        patterns = set()
        # Adding horizontal patterns
        for row in rows:
            for length in range(2, len(row) + 1):
                for i in range(len(row) - length + 1):
                    patterns.add(row[i:i + length])
                    patterns.add(row[i:i + length][::-1])  # reversed

        # Adding vertical patterns (considering QWERTY layout)
        for col in range(10):  # max number of columns in standard QWERTY keyboard
            column_pattern = ''.join([row[col] for row in rows if col < len(row)])
            for length in range(2, len(column_pattern) + 1):
                for i in range(len(column_pattern) - length + 1):
                    patterns.add(column_pattern[i:i + length])
                    patterns.add(column_pattern[i:i + length][::-1])  # reversed
        
        return patterns

    keyboard_patterns = generate_patterns(keyboard_rows)
    lower_password = password.lower()
    return any(pattern in lower_password for pattern in keyboard_patterns)

def starts_with_capital(password):
    """Check if the password starts with a capital letter."""
    return password[0].isupper() if password else False

def is_camel_case(password):
    """Check if the password is in camel case."""
    return re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', password) is not None

def has_uppercase_lowercase_alternation(password):
    """Check for alternating capitalization starting with uppercase."""
    return all(x.isupper() for x in password[::2]) and all(x.islower() for x in password[1::2])

def has_lowercase_uppercase_alternation(password):
    """Check for alternating capitalization starting with lowercase."""
    return all(x.islower() for x in password[::2]) and all(x.isupper() for x in password[1::2])

class Feature:
    def __init__(self, name, func):
        self.name = name
        #self.key = key
        self.func = func

# Defining the features
features = [
    Feature('length', len),
    Feature('num_uppercase', lambda password: sum(1 for char in password if char.isupper())),
    Feature('num_lowercase', lambda password: sum(1 for char in password if char.islower())),
    Feature('num_digits', lambda password: sum(1 for char in password if char.isdigit())),
    Feature('num_special', lambda password: sum(1 for char in password if char in string.punctuation)),
    Feature('starts_with_digit', lambda password: password[0].isdigit() if password else False),
    Feature('ends_with_digit', lambda password: password[-1].isdigit() if password else False),
    Feature('starts_with_special', lambda password: password[0] in string.punctuation if password else False),
    Feature('ends_with_special', lambda password: password[-1] in string.punctuation if password else False),
    Feature('has_sequential_chars', has_sequential_chars),
    Feature('has_repeated_patterns', has_repeated_patterns),
    Feature('char_diversity', char_diversity),
    Feature('contains_leetspeak', contains_leetspeak),
    Feature('calculate_entropy',  calculate_entropy),
    Feature('contains_keyboard_patterns', contains_keyboard_patterns),
    Feature('starts_with_capital', starts_with_capital),
    Feature('is_camel_case', is_camel_case),
    Feature('has_uppercase_lowercase_alternation', has_uppercase_lowercase_alternation),
    Feature('has_lowercase_uppercase_alternation', has_lowercase_uppercase_alternation),
]

def extract_features(password):
    feature_values = {}
    for feature in features:
        feature_values[feature.name] = feature.func(password)
    return feature_values

def write_features_to_csv(args, passwords):
    with open(args.output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = [feature.name for feature in features]
        header.append('human_created')
        writer.writerow(header)
        for password in passwords:
            feature_values = extract_features(password)
            feature_values['human_created'] = args.human_created
            writer.writerow(feature_values.values())

def main(args):
    passwords = []
    with open(args.input_file, 'r', encoding='latin-1') as file:
        for line in file:
            passwords.append(line.strip())
    write_features_to_csv(args, passwords)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract features from a list of passwords.')
    parser.add_argument('input_file', type=str, help='Path to the file containing the passwords')
    parser.add_argument('output_file', type=str, help='CSV file to write the features to')
    parser.add_argument('--human-created', action='store_true', default=False, help='Add a column indicating the passwords are human-created (default: False)')
    args = parser.parse_args()
    main(args)
