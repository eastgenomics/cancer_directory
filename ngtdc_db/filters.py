import django_filters
from django import forms

from .models import (
    CancerType,
    ClinicalIndication,
    TestScope,
    Technology,
    GenomicTest,
    )


class V1MainFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(V1MainFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    # Create a filter for the cancer_type field
    ci_code__cancer_id = django_filters.ChoiceFilter(

        # Specify which field of the table is being filtered
        # In this case field is from another table, so define the path via keys
        field_name='ci_code__cancer_id',

        # Specify the human-readable name for the filter
        label='Cancer Type',

        # Define the possible values the field can be filtered on
        choices = [
            (CancerType.objects.get(pk=x).cancer_id,
            CancerType.objects.get(pk=x).cancer_type) for x in \
                CancerType.objects.all().\
                    values_list('cancer_id', flat=True).distinct()
            ],

        # Format the appearance of the filter box
        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 72px',}
            )
        )

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',

        # Provide help text to display next to the filter box
        help_text = '(Clinical indication code e.g. M1)',

        # Specify the filter type as a case-insensitive text search
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 108px',}
            )
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 102px',}
            )
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        help_text = '(Test code e.g. M1.2)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 91px',}
            )
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        help_text = '(Test name e.g. KRAS hotspot)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 86px',}
            )
        )

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets (Essential)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',

        # Specify that no duplicate records are returned
        distinct = True,
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 28px',}
            )
        )

    scope_id = django_filters.ChoiceFilter(
        field_name='scope_id',
        label='Test Scope',

        choices = [
            (TestScope.objects.get(pk=x).scope_id,
            TestScope.objects.get(pk=x).test_scope) for x in \
                TestScope.objects.all().\
                    values_list('scope_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 83px',}
            )
        )
    
    tech_id = django_filters.ChoiceFilter(
        field_name='tech_id',
        label='Technology',

        choices = [
            (Technology.objects.get(pk=x).tech_id,
            Technology.objects.get(pk=x).technology) for x in \
                Technology.objects.all().\
                    values_list('tech_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 78px',}
            )
        )

    currently_provided = django_filters.ChoiceFilter(
        field_name='currently_provided',
        label='Currently Provided',

        choices = [
            (x, x) for x in GenomicTest.objects.all().values_list(
                'currently_provided',
                flat=True,
                ).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 23px',}
            )
        )

    inhouse_id = django_filters.ChoiceFilter(
        field_name='inhouse_technology',
        label='In-House Technology',

        choices = [
            (x, x) for x in GenomicTest.objects.all().values_list(
                'inhouse_technology',
                flat=True,
                ).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw;',}
            )
        )

    class Meta:
        model = GenomicTest

        fields = [
            'ci_code__cancer_id',
            'ci_code',
            'ci_name',
            'test_code',
            'test_name',
            'targets_essential',
            'scope_id',
            'tech_id',
            'currently_provided',
            'inhouse_technology',
            ]

        exclude = [
            'currently_provided',
            'inhouse_technology',
            'eligibility',
            ]


class V2MainFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(V2MainFilter, self).__init__(*args, **kwargs)
        self.filters['ci_code__cancer_id'].label = 'Cancer Type'

    ci_code__cancer_id = django_filters.ChoiceFilter(
        field_name='ci_code__cancer_id',
        label='Cancer Type',

        choices = [
            (CancerType.objects.get(pk=x).cancer_id,
            CancerType.objects.get(pk=x).cancer_type) for x in \
                CancerType.objects.all().\
                    values_list('cancer_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 72px',}
            )
        )

    ci_code = django_filters.CharFilter(
        field_name='ci_code__ci_code',
        label='CI Code',
        help_text = '(Clinical indication code e.g. M1)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 108px',}
            )
        )

    ci_name = django_filters.CharFilter(
        field_name='ci_code__ci_name',
        label='CI Name',
        help_text = '(Clinical indication name e.g. Colorectal carcinoma)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 102px',}
            )
        )

    test_code = django_filters.CharFilter(
        field_name='test_code',
        label='Test Code',
        help_text = '(Test code e.g. M1.2)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 91px',}
            )
        )

    test_name = django_filters.CharFilter(
        field_name='test_name',
        label='Test Name',
        help_text = '(Test name e.g. KRAS hotspot)',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 86px',}
            )
        )

    targets_essential = django_filters.CharFilter(
        field_name='targets_essential__target',
        label='Targets (Essential)',
        help_text = '(Test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 28px',}
            )
        )

    targets_desirable = django_filters.CharFilter(
        field_name='targets_desirable__target',
        label='Targets (Desirable)',
        help_text = '(Optional test targets e.g. KRAS)',
        lookup_expr='icontains',
        distinct = True,
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 24px',}
            )
        )

    scope_id = django_filters.ChoiceFilter(
        field_name='scope_id',
        label='Test Scope',

        choices = [
            (TestScope.objects.get(pk=x).scope_id,
            TestScope.objects.get(pk=x).test_scope) for x in \
                TestScope.objects.all().\
                    values_list('scope_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 83px',}
            )
        )
    
    tech_id = django_filters.ChoiceFilter(
        field_name='tech_id',
        label='Technology',

        choices = [
            (Technology.objects.get(pk=x).tech_id,
            Technology.objects.get(pk=x).technology) for x in \
                Technology.objects.all().\
                    values_list('tech_id', flat=True).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 78px',}
            )
        )

    provided_id = django_filters.ChoiceFilter(
        field_name='currently_provided',
        label='Currently Provided',

        choices = [
            (x, x) for x in GenomicTest.objects.all().values_list(
                'currently_provided',
                flat=True,
                ).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw; margin-left: 23px',}
            )
        )

    inhouse_id = django_filters.ChoiceFilter(
        field_name='inhouse_technology',
        label='In-House Technology',

        choices = [
            (x, x) for x in GenomicTest.objects.all().values_list(
                'inhouse_technology',
                flat=True,
                ).distinct()
            ],

        widget=forms.Select(
            attrs={'style': 'width: 10vw;'}
            )
        )

    tt_code = django_filters.CharFilter(
        field_name='tt_code',
        label='TT Code',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={'style': 'width: 10vw; margin-left: 104px',}
            )
        )

    class Meta:
        model = GenomicTest

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
            'currently_provided',
            'inhouse_technology',
            'tt_code',
            ]

        exclude = [
            'cc_id',
            'specialist_id',
            'eligibility',
            'family_id',
            'citt_id',
            'currently_provided',
            'inhouse_technology',
            ]


class V1CIFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(V1CIFilter, self).__init__(*args, **kwargs)
        self.filters['cancer_id'].label = 'Cancer Type'

    cancer_id = django_filters.ChoiceFilter(
        field_name='cancer_id__cancer_id',
        label='Cancer Type',

        choices = [
            (CancerType.objects.get(pk=x).cancer_id,
            CancerType.objects.get(pk=x).cancer_type) for x in \
                CancerType.objects.all().\
                    values_list('cancer_id', flat=True).distinct()
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
        model = ClinicalIndication
        exclude = []


class V2CIFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(V2CIFilter, self).__init__(*args, **kwargs)
        self.filters['cancer_id'].label = 'Cancer Type'

    cancer_id = django_filters.ChoiceFilter(
        field_name='cancer_id__cancer_id',
        label='Cancer Type',

        choices = [
            (CancerType.objects.get(pk=x).cancer_id,
            CancerType.objects.get(pk=x).cancer_type) for x in \
                CancerType.objects.all().\
                    values_list('cancer_id', flat=True).distinct()
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
        model = ClinicalIndication
        exclude = []
