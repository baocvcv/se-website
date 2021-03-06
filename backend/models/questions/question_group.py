'''code for QuestionGroup'''
from django.db import models
from polymorphic.models import PolymorphicModel

from backend.models.knowledge_node import KnowledgeNode
from backend.models.question_bank import QuestionBank


class QuestionGroup(PolymorphicModel):
    '''Model of QuestionGroup
    each Question has a ForeignKey to a QuestionGroup
    A QuestionGroup records the change history of one qustion
    Attributes:
        group_id: the identity of a QuestionGroup
        current_version: the latest version of this list of questions
    '''
    current_version = models.DateTimeField()
    parents_node = models.ManyToManyField(KnowledgeNode)
    belong_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
