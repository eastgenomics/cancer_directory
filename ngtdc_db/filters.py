import django_filters
from django import forms
from .models import (
    CancerTypeNov20,
    ClinicalIndicationNov20,
    ScopeNov20,
    TechnologyNov20,
    CurrentlyProvidedNov20,
    InHouseTestNov20,
    GenomicTestNov20,

    CancerTypeJul21,
    ClinicalIndicationJul21,
    ScopeJul21,
    TechnologyJul21,
    CurrentlyProvidedJul21,
    InHouseTestJul21,
    GenomicTestJul21,
)


class Jul21MainFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Jul21MainFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    ci_code__cancer_id = django_filters.ChoiceFilter(
        field_name='ci_code__cancer_id',
        label='Cancer Type',

        choices = [
            (CancerTypeJul21.objects.get(pk=x).cancer_id, CancerTypeJul21.objects.get(pk=x).cancer_type) for x in CancerTypeJul21.objects.all().values_list('cancer_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 59px',}
            )
        )

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 95px',}
            )
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 89px',}
            )
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        help_text = '(Test code e.g. M1.2)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 78px',}
            )
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        help_text = '(Test name e.g. KRAS hotspot)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 73px',}
            )
        )

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets (Essential)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 15px',}
            )
        )

    targets_desirable = django_filters.CharFilter(
        field_name='targets_desirable__target',
        label='Targets (Desirable)',
        help_text = '(Optional test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 11px',}
            )
        )

    scope_id = django_filters.ChoiceFilter(
        field_name='scope_id',
        label='Test Scope',

        choices = [
            (ScopeJul21.objects.get(pk=x).scope_id, ScopeJul21.objects.get(pk=x).test_scope) for x in ScopeJul21.objects.all().values_list('scope_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 70px',}
            )
        )
    
    tech_id = django_filters.ChoiceFilter(
        field_name='tech_id',
        label='Technology',

        choices = [
            (TechnologyJul21.objects.get(pk=x).tech_id, TechnologyJul21.objects.get(pk=x).technology) for x in TechnologyJul21.objects.all().values_list('tech_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 65px',}
            )
        )

    provided_id = django_filters.ChoiceFilter(
        field_name='provided_id',
        label='Currently Provided',

        choices = [
            (CurrentlyProvidedJul21.objects.get(pk=x).provided_id, CurrentlyProvidedJul21.objects.get(pk=x).provided) for x in CurrentlyProvidedJul21.objects.all().values_list('provided_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 10px',}
            )
        )

    inhouse_id = django_filters.ChoiceFilter(
        field_name='inhouse_id',
        label='In-House Test',

        choices = [
            (InHouseTestJul21.objects.get(pk=x).inhouse_id, InHouseTestJul21.objects.get(pk=x).inhouse) for x in InHouseTestJul21.objects.all().values_list('inhouse_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 48px',}
            )
        )

    tt_code = django_filters.CharFilter(
        field_name='tt_id__tt_code',
        label='TT Code',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 91px',}
            )
        )

    class Meta:
        model = GenomicTestJul21

        fields = [
            'ci_code__cancer_id',
            'ci_code',
            'ci_name',
            'test_code',
            'test_name',
            'targets_essential',
            'targets_desirable',
            'scope_id',
            'tech_id',
            'provided_id',
            'inhouse_id',
            'tt_code',
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

    cancer_id = django_filters.ChoiceFilter(
        field_name='cancer_id__cancer_id',
        label='Cancer Type',

        choices = [
            (CancerTypeJul21.objects.get(pk=x).cancer_id, CancerTypeJul21.objects.get(pk=x).cancer_type) for x in CancerTypeJul21.objects.all().values_list('cancer_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 0px',}
            )
        )

    ci_code = django_filters.CharFilter(
        field_name='ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',

        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 36px',}
            ),
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',

        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 30px',}
            )
        )

    class Meta:
        model = ClinicalIndicationJul21
        exclude = []


class Nov20MainFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Nov20MainFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    ci_code__cancer_id = django_filters.ChoiceFilter(
        field_name='ci_code__cancer_id',
        label='Cancer Type',

        choices = [
            (CancerTypeNov20.objects.get(pk=x).cancer_id, CancerTypeNov20.objects.get(pk=x).cancer_type) for x in CancerTypeNov20.objects.all().values_list('cancer_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 59px',}
            )
        )

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'width: 10vw; margin-left: 95px',})
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'width: 10vw; margin-left: 89px',})
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        help_text = '(Test code e.g. M1.2)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'width: 10vw; margin-left: 78px',})
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        help_text = '(Test name e.g. KRAS hotspot)',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'style': 'width: 10vw; margin-left: 73px',})
        )

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets (Essential)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(attrs={'style': 'width: 10vw; margin-left: 15px',})
        )

    scope_id = django_filters.ChoiceFilter(
        field_name='scope_id',
        label='Test Scope',

        choices = [
            (ScopeNov20.objects.get(pk=x).scope_id, ScopeNov20.objects.get(pk=x).test_scope) for x in ScopeNov20.objects.all().values_list('scope_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 70px',}
            )
        )
    
    tech_id = django_filters.ChoiceFilter(
        field_name='tech_id',
        label='Technology',

        choices = [
            (TechnologyNov20.objects.get(pk=x).tech_id, TechnologyNov20.objects.get(pk=x).technology) for x in TechnologyNov20.objects.all().values_list('tech_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 65px',}
            )
        )

    provided_id = django_filters.ChoiceFilter(
        field_name='provided_id',
        label='Currently Provided',

        choices = [
            (CurrentlyProvidedNov20.objects.get(pk=x).provided_id, CurrentlyProvidedNov20.objects.get(pk=x).provided) for x in CurrentlyProvidedNov20.objects.all().values_list('provided_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 10px',}
            )
        )

    inhouse_id = django_filters.ChoiceFilter(
        field_name='inhouse_id',
        label='In-House Test',

        choices = [
            (InHouseTestNov20.objects.get(pk=x).inhouse_id, InHouseTestNov20.objects.get(pk=x).inhouse) for x in InHouseTestNov20.objects.all().values_list('inhouse_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 48px',}
            )
        )

    class Meta:
        model = GenomicTestNov20

        fields = [
            'ci_code__cancer_id',
            'ci_code',
            'ci_name',
            'test_code',
            'test_name',
            'targets_essential',
            'scope_id',
            'tech_id',
            'provided_id',
            'inhouse_id',
        ]

        exclude = [
            'eligibility',
        ]


class Nov20CIFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(Nov20CIFilter, self).__init__(*args, **kwargs)
        self.filters['cancer_id'].label = 'Cancer Type'

    cancer_id = django_filters.ChoiceFilter(
        field_name='cancer_id__cancer_id',
        label='Cancer Type',

        choices = [
            (CancerTypeNov20.objects.get(pk=x).cancer_id, CancerTypeNov20.objects.get(pk=x).cancer_type) for x in CancerTypeNov20.objects.all().values_list('cancer_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 0px',}
            )
        )

    ci_code = django_filters.CharFilter(
        field_name='ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',

        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 36px',}
            ),
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',

        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 30px',}
            )
        )

    class Meta:
        model = ClinicalIndicationNov20
        exclude = []
