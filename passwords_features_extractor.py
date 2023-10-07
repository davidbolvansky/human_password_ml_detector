from password_features import extract_features, features
import argparse
import csv

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
