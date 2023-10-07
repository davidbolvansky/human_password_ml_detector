import random
import argparse
import string

def generate_random_password():
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

    # Randomly decide which character sets to include
    character_sets = [
        char_type for char_type in [lowercase, uppercase, digits, punctuation]
        if random.choice([True, False])
    ]

    # Handle case where no sets are selected
    if not character_sets:
        character_sets = [lowercase, uppercase, digits]

    # Combine selected character sets and generate password
    characters = ''.join(character_sets)
    password_length = random.randint(8, 16)  # You can set your own length range
    password = ''.join(random.choice(characters) for i in range(password_length))
    return password

def main(output_file, num_passwords):
    with open(output_file, 'w') as file:
        for _ in range(num_passwords):
            password = generate_random_password()
            file.write(password + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate random passwords and write to a file.')
    parser.add_argument('output_file', type=str, help='Path to the output file')
    parser.add_argument('--num-passwords', type=int, default=100, help='Number of passwords to generate (default: 100)')
    args = parser.parse_args()
    main(args.output_file, args.num_passwords)

