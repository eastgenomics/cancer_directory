import django_filters
from django import forms
from .models import GenomicTest


class GenomicTestFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(GenomicTestFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        help_text = '(Test code e.g. M1.2)',
        lookup_expr='icontains',
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        help_text = '(Test name e.g. KRAS hotspot)',
        lookup_expr='icontains',
        )

    targets = django_filters.CharFilter(
        field_name='targets__target',
        label='Targets',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        )


    class Meta:
        model = GenomicTest
        fields = [
            'ci_code__cancer_id',
            'scope_id',
            'tech_id',
            'inhouse_id',
            'provided_id',
            ]
