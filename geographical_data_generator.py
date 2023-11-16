from faker import Faker

def generate_geographical_data(num_samples):
    fake = Faker()
    fake.add_provider("faker.providers.address")
    return [(fake.latitude(), fake.longitude()) for _ in range(num_samples)]
