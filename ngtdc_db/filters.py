import django_filters
from .models import GenomicTest


class GenomicTestFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(GenomicTestFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_type'].label = 'Cancer Type'

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code', 
        lookup_expr='icontains', 
        label='CI Code',
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name', 
        lookup_expr='icontains', 
        label='CI Name',
        )

    test_code = django_filters.CharFilter(
        field_name='test_code', 
        lookup_expr='icontains', 
        label='Test Code',
        )

    test_name = django_filters.CharFilter(
        field_name='test_name', 
        lookup_expr='icontains', 
        label='Test Name',
        )

    targets = django_filters.CharFilter(
        field_name='targets', 
        lookup_expr='icontains', 
        label='Targets',
        )


    class Meta:
        model = GenomicTest
        fields = ['ci_code__cancer_type', 'test_scope', 'technology']
