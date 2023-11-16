from faker import Faker

def generate_numeric_data(num_samples, min_value, max_value, mean, std_deviation):
    fake = Faker()
    fake.add_provider("faker.providers.person")
    return [fake.random_int(min_value, max_value) for _ in range(num_samples)]
