from faker import Faker

fake = Faker()


def create_fake_daz() -> dict[str, str]:
    comment = fake.sentence(nb_words=10, variable_nb_words=True)
    return {
        "comment": comment,
    }
