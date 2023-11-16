import random
import string

def generate_categorical_data(num_samples):
    return [''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10))) for _ in range(num_samples)]
