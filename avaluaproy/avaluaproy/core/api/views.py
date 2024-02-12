from rest_framework import viewsets, mixins, filters, views
from core.api.serializers import *
from core.models import Modulo, ResAprendizaje
from rest_framework.exceptions import ValidationError
from .pagination import LargeResultsSetPagination, StandardResultsSetPagination, ShortResultsSetPagination
from rest_framework import serializers, response, status
from rest_framework.decorators import api_view
#UD10.3.b
from core.mixins import deleteMixin_api
#UD11.1.b
from rest_framework.permissions import IsAuthenticated

#UD10.3.a

class ModuloListViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Listado de modulos del curso
    """
    #UD11.1.b
    permission_classes = [IsAuthenticated]

    serializer_class = ModuloListSerializer
    pagination_class = None
    ordering = 'codigo'
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['codigo', 'nombre']
    search_fields = ['codigo', 'nombre']
    queryset = Modulo.objects.all()

#UD10.3.b  
class ModuloDetailViewSet(deleteMixin_api,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    
    """
    Si tiene id en la url permite modificar y borrar un modulo, si no la tiene permite crearlo
    """
    #UD11.1.b
    permission_classes = [IsAuthenticated]
    
    serializer_class = ModuloDetailSerializer
    queryset = Modulo.objects.all()

###############################################


class RAListViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Listado de RAs del curso
    """
    #UD11.1.b
    permission_classes = [IsAuthenticated]
    
    serializer_class = RAListSerializer
    pagination_class = StandardResultsSetPagination
    ordering = 'codigo'
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['codigo']
    search_fields = ['codigo', 'descripcion']
    
    def get_queryset(self):
        modulo = self.request.query_params.get('modulo')
        if modulo:
            return ResAprendizaje.objects.filter(modulo=modulo)
        
        return ResAprendizaje.objects.all()

#UD10.3.b
class RADetailViewSet(deleteMixin_api,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    Si tiene id en la url permite modificar y borrar un resultado de aprendizaje, si no la tiene permite crearlo
    """    
    #UD11.1.b
    permission_classes = [IsAuthenticated]
    
    serializer_class = RADetailSerializer
    queryset = ResAprendizaje.objects.all()

###############################################
    
class CEListViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Listado de CEs del curso
    """
    #UD11.1.b
    permission_classes = [IsAuthenticated]
    
    serializer_class = CEListSerializer
    pagination_class = StandardResultsSetPagination
    ordering = 'codigo'
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    filter_fields = ['resultado_aprendizaje_modulo', 'resultado_aprendizaje']
    ordering_fields = ['codigo', 'descripcion']
    search_fields = ['codigo', 'descripcion',
                    'resultado_aprendizaje_codigo',
                    'resultado_aprendizaje_descripcion',
                    'resultado_aprendizaje__modulo_nombre']
    
    def get_queryset(self):
        modulo = self.request.query_params.get('modulo')
        ra = self.request.query_params.get('res_ap')
        todos = CritEvaluacion.objects.all()
        if modulo:
            todos = todos.filter(resultado_aprendizaje__modulo=modulo)
        if ra:
            todos = todos.filter(resultado_aprendizaje=ra)
        

        return todos
    
#UD10.3.b
class CEDetailViewSet(deleteMixin_api,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    Si tiene id en la url permite modificar y borrar un criterio de evaluacion, si no la tiene permite crearlo
    """  
    #UD11.1.b
    permission_classes = [IsAuthenticated]
    
    serializer_class = CEDetailSerializer
    queryset = ResAprendizaje.objects.all()

###############################################