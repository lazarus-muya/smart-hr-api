from logging import getLogger
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from src.account.serializers import (WorkPlace, 
                                     WorkplaceSerializer, 
                                     Bank, BankSerializer, 
                                     EmployeeGrade, 
                                     EmployeeGradeSerializer, 
                                     Department, 
                                     DepartmentSerializer)

from src.account.staff import Staff
from src.administration.serializers import QuestionSerializer, Question


logger = getLogger(__name__)

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    allowed_methods = ['GET', 'PUT', 'POST', 'DELETE', 'PATCH']


class StaffListRetrieveMixin(CreateListRetrieveViewSet):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        obj = serializer.data
        print(obj)
        if obj['department'] is not None:
            _department = Department.objects.get(pk=obj['department'])
            obj['department'] = DepartmentSerializer(_department).data
        if obj['workplace'] is not None:
            _workplace = WorkPlace.objects.get(pk=obj['workplace'])
            obj['workplace'] = WorkplaceSerializer(_workplace).data
        if obj['grade'] is not None:
            _grade = EmployeeGrade.objects.get(pk=obj['grade'])
            obj['grade'] = EmployeeGradeSerializer(_grade).data
        if obj['bank'] is not None:
            _bank = Bank.objects.get(pk=obj['bank'])
            obj['bank'] = BankSerializer(_bank).data
        return Response(obj)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        _serializer = serializer.data
        for obj in _serializer:
            if obj['department'] is not None:
                _department = Department.objects.get(pk=obj['department'])
                obj['department'] = DepartmentSerializer(_department).data
            if obj['workplace'] is not None:
                _workplace = WorkPlace.objects.get(pk=obj['workplace'])
                obj['workplace'] = WorkplaceSerializer(_workplace).data
            if obj['grade'] is not None:
                _grade = EmployeeGrade.objects.get(pk=obj['grade'])
                obj['grade'] = EmployeeGradeSerializer(_grade).data
            if obj['bank'] is not None:
                _bank = Bank.objects.get(pk=obj['bank'])
                obj['bank'] = BankSerializer(_bank).data
        return Response(_serializer)


class SurveyCreateListRetrieveViewSet(CreateListRetrieveViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        _question = Question.objects.get(pk=serializer.data['question'])
        _questionSerializer = QuestionSerializer(_question)
        _serializer = serializer.data
        _serializer["question"] = _questionSerializer.data
        return Response(_serializer)
