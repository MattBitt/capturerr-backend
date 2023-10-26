# """Illustrates a mixin which provides a generic association
# via a individually generated association tables for each parent class.
# The associated objects themselves are persisted in a single table
# shared among all parents.

# This configuration has the advantage that all Address
# rows are in one table, so that the definition of "Address"
# can be maintained in one place.   The association table
# contains the foreign key to Address so that Address
# has no dependency on the system.


# """
# from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine
# from sqlalchemy.ext.declarative import as_declarative, declared_attr
# from sqlalchemy.orm import Session, relationship


# @as_declarative()
# class Base:
#     """Base class which provides automated table name
#     and surrogate primary key column.

#     """

#     @declared_attr
#     def __tablename__(cls):
#         return cls.__name__.lower()

#     id = Column(Integer, primary_key=True, unique=True)


# class Address(Base):
#     """The Address class.

#     This represents all address records in a
#     single table.

#     """

#     street = Column(String)
#     city = Column(String)
#     zip = Column(String)

#     def __repr__(self):
#         return "%s(street=%r, city=%r, zip=%r)" % (
#             self.__class__.__name__,
#             self.street,
#             self.city,
#             self.zip,
#         )


# class HasAddresses:
#     """HasAddresses mixin, creates a new address_association
#     table for each parent.

#     """

#     @declared_attr
#     def addresses(cls):
#         address_association = Table(
#             "%s_addresses" % cls.__tablename__,
#             cls.metadata,
#             Column("address_id", ForeignKey("address.id"), primary_key=True),
#             Column(
#                 "%s_id" % cls.__tablename__,
#                 ForeignKey("%s.id" % cls.__tablename__),
#                 primary_key=True,
#             ),
#         )
#         return relationship(Address, secondary=address_association)


# class Customer(HasAddresses, Base):
#     name = Column(String)


# class Supplier(HasAddresses, Base):
#     company_name = Column(String)


# engine = create_engine("sqlite:///sandbox.db", echo=False)
# Base.metadata.create_all(engine)


# add1 = Address(street="123 anywhere street", city="New York", zip="10110")
# add2 = Address(street="40 main street", city="San Francisco", zip="95732")
# add3 = Address(street="12 high street", city="Boston", zip="23456")
# add4 = Address(street="123 low street", city="New Orleans", zip="70003")

# c1 = Customer(name="customer 1", addresses=[add1, add3])
# c2 = Customer(name="customer 2", addresses=[add2])
# s1 = Supplier(
#     company_name="Ace Hammers",
#     addresses=[add4],
# )
# session = Session(engine)

# session.add_all([c1, c2, s1])

# session.commit()

# customers = session.query(Customer).all()
# customers[0].addresses.append(add2)
# session.add(customers[0])
# session.commit()

# for customer in session.query(Customer):
#     print(f"CUSTOMER: {customer.name}")
#     for address in customer.addresses:
#         print(address)
