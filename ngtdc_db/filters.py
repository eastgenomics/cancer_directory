import django_filters
from django import forms
from .models import (
    GenomicTestNov20,
    ClinicalIndicationNov20,
    GenomicTestJul21,
    ClinicalIndicationJul21,
)


class Jul21MainFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Jul21MainFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 94px',})
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        help_text = '(Test code e.g. M1.2)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 82px',})
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        help_text = '(Test name e.g. KRAS hotspot)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 77px',})
        )

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets (Essential)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 15px',})
        )

    targets_desirable = django_filters.CharFilter(
        field_name='targets_desirable__target',
        label='Targets (Desirable)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 11px',})
        )

    tt_code = django_filters.CharFilter(
        field_name='tt_id__tt_code',
        label='TT Code',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 96px',})
        )

    # ci_code__cancer_id = django_filters.ChoiceFilter(
    #     field_name='ci_code__cancer_id',
    #     label='Cancer Type',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # scope_id = django_filters.ChoiceFilter(
    #     field_name='scope_id',
    #     label='Test Scope',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # tech_id = django_filters.ChoiceFilter(
    #     field_name='tech_id',
    #     label='Technology',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # inhouse_id = django_filters.ChoiceFilter(
    #     field_name='inhouse_id',
    #     label='In-House Test',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # provided_id = django_filters.ChoiceFilter(
    #     field_name='provided_id',
    #     label='Currently Provided',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )

    class Meta:
        model = GenomicTestJul21

        fields = [
            'ci_code__cancer_id',
            'scope_id',
            'tech_id',
            'inhouse_id',
            'provided_id',
        ]

        exclude = [
            'cc_id',
            'specialist_id',
            'eligibility',
            'family_id',
            'citt_id',
            'tt_id'
        ]


class Jul21CIFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Jul21CIFilter, self).__init__(*args, **kwargs)
        self.filters['cancer_id'].label = 'Cancer Type'

    ci_code = django_filters.CharFilter(
        field_name='ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 38px',}),
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 32px',})
        )

    class Meta:
        model = ClinicalIndicationJul21
        fields = [
            'cancer_id',
            ]



class Nov20MainFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Nov20MainFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 94px',})
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        help_text = '(Test code e.g. M1.2)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 82px',})
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        help_text = '(Test name e.g. KRAS hotspot)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 77px',})
        )

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets (Essential)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 15px',})
        )

    # ci_code__cancer_id = django_filters.ChoiceFilter(
    #     field_name='ci_code__cancer_id',
    #     label='Cancer Type',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # scope_id = django_filters.ChoiceFilter(
    #     field_name='scope_id',
    #     label='Test Scope',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # tech_id = django_filters.ChoiceFilter(
    #     field_name='tech_id',
    #     label='Technology',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # inhouse_id = django_filters.ChoiceFilter(
    #     field_name='inhouse_id',
    #     label='In-House Test',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )
    
    # provided_id = django_filters.ChoiceFilter(
    #     field_name='provided_id',
    #     label='Currently Provided',
    #     widget=forms.Select(attrs={'style': 'max-width: 10vw; margin-left: 100px',})
    #     )

    class Meta:
        model = GenomicTestNov20

        fields = [
            'ci_code__cancer_id',
            'scope_id',
            'tech_id',
            'inhouse_id',
            'provided_id',
        ]

        exclude = [
            'eligibility',
        ]


class Nov20CIFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Nov20CIFilter, self).__init__(*args, **kwargs)
        self.filters['cancer_id'].label = 'Cancer Type'

    ci_code = django_filters.CharFilter(
        field_name='ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 38px',}),
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'max-width: 10vw; margin-left: 32px',})
        )

    class Meta:
        model = ClinicalIndicationNov20
        fields = [
            'cancer_id',
            ]
