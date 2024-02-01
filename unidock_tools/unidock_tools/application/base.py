from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    @abstractmethod
    def check_dependencies(self) -> bool:
        """ Check ligand type by file path """
        pass
