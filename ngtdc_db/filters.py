import django_filters
from .models import GenomicTest


class GenomicTestFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(GenomicTestFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',
        lookup_expr='icontains',
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        lookup_expr='icontains',
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        lookup_expr='icontains',
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        lookup_expr='icontains',
        )

    targets = django_filters.CharFilter(
        field_name='targets__target',
        label='Targets',
        lookup_expr='icontains',
        distinct = True,
        )


    class Meta:
        model = GenomicTest
        fields = ['ci_code__cancer_id', 'scope_id', 'tech_id']
        
