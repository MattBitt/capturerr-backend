import abc


# somewhere in the domain layer
class Listing:
    ...


class ListingId:
    ...


class ListingRepository(metaclass=abc.ABCMeta):
    """An interface to listing repository"""

    @abc.abstractmethod
    def add(self, entity: Listing) -> None:
        """Adds new entity to a repository"""
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: Listing) -> None:
        """Removes existing entity from a repository"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, id: ListingId) -> Listing:
        """Retrieves entity by its identity"""
        raise NotImplementedError()

    def __getitem__(self, index: ListingId) -> Listing:
        return self.get_by_id(index)
