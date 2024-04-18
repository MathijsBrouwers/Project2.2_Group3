#This class is only to provide the abstract class meant to serve as the base for all the implemented evaluators

from abc import ABC, abstractmethod

class Evaluator(ABC):

    @abstractmethod
    def minScore(self):
        pass

    @abstractmethod
    def maxScore(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass