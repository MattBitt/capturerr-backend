from faker import Faker

fake = Faker()


def create_fake_bar() -> dict[str, str]:
    title = fake.sentence(nb_words=10, variable_nb_words=True)
    return {
        "title": title,
    }
