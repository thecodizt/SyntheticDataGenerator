from faker import Faker

def generate_categorical_data(num_samples, categories):
    fake = Faker()
    return [fake.random_element(categories) for _ in range(num_samples)]
