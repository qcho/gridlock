from abc import ABCMeta, abstractmethod


class TransferenceFunction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def apply(self, value):
        raise NotImplementedError("Extend this class")

    @abstractmethod
    def apply_inverse(self, value):
        raise NotImplementedError("Extend this class")