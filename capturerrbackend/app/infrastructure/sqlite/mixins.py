# class HasTags:
#     """HasTags mixin, creates a new tag_association
#     table for each parent.

#     """

#     @declared_attr
#     def tags(cls):
#         tag_association = Table(
#             "%s_tags" % cls.__tablename__,
#             cls.metadata,
#             Column("tag_id", ForeignKey("tag.id"), primary_key=True),
#             Column(
#                 "%s_id" % cls.__tablename__,
#                 ForeignKey("%s.id" % cls.__tablename__),
#                 primary_key=True,
#             ),
#         )
#         return relationship(TagDTO, secondary=tag_association)
