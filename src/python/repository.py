from abc import ABC, abstractmethod

class Repository[T](ABC):

    @abstractmethod
    def get(self, id) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, id, **kwargs: object) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id) -> None:
        raise NotImplementedError
