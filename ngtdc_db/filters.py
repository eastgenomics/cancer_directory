import django_filters
from django import forms
from .models import GenomicTestNov20, GenomicTestJul21


class Jul21_Filter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Jul21_Filter, self).__init__(*args, **kwargs)
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

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets (Essential)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        )

    targets_desirable = django_filters.CharFilter(
        field_name='targets_desirable__target',
        label='Targets (Desirable)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        )

    tt_code = django_filters.CharFilter(
        field_name='tt_id__tt_code',
        label='TT Code',
        lookup_expr='icontains',
        )


    class Meta:
        model = GenomicTestJul21
        fields = [
            'ci_code__cancer_id',
            'scope_id',
            'tech_id',
            'inhouse_id',
            'provided_id',
            ]


class Nov20_Filter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Nov20_Filter, self).__init__(*args, **kwargs)
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

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        )

    class Meta:
        model = GenomicTestNov20
        fields = [
            'ci_code__cancer_id',
            'scope_id',
            'tech_id',
            'inhouse_id',
            'provided_id',
            ]
