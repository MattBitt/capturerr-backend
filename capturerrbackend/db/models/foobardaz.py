# from sqlalchemy import (
#     Column,
#     DateTime,
#     ForeignKey,
#     Integer,
#     String,
#     Table,
#     create_engine,
#     func,
# )
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import backref, relationship


# engine = create_engine("sqlite:///many_to_many.db")
# Base = declarative_base()


# if __name__ == "__main__":
#     Base.metadata.create_all(engine)

#     g1 = Bar(title="Super Mario Bros.", genre="Platformer", platform="NES", price=20)
#     g2 = Bar(title="Super Mario Bros. 2", genre="Platformer", platform="NES", price=25)
#     g3 = Bar(title="Super Mario Bros. 3", genre="Platformer", platform="NES", price=30)
#     u1 = Foo(name="Mario")
#     u2 = Foo(name="Luigi")
#     r1 = Daz(score=9, comment="Great bar!")
#     r2 = Daz(score=8, comment="Fun bar!")

#     g1.foos = [u1, u2]
#     g2.foos = [u2]
#     g1.dazs = [r1]
#     u1.bars.append(g3)
#     session = get_db_session()
#     session.add_all([g1, g2, g3, u1, u2, r1, r2])
#     session.commit()

#     print(u1.bars)
#     print(g1.dazs)
