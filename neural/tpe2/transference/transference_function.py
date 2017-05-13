from abc import ABCMeta, abstractmethod


class TransferenceFunction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def apply(self, value):
        raise NotImplementedError("Extend this class")

    @abstractmethod
    def apply_derived(self, value):
        raise NotImplementedError("Extend this class")

    @abstractmethod
    def to_json(self):
        raise NotImplementedError("Extend this class")
