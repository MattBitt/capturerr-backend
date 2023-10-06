from faker import Faker

fake = Faker()


def create_fake_foo() -> dict[str, str]:
    name = fake.sentence(nb_words=10, variable_nb_words=True)
    return {
        "name": name,
    }
