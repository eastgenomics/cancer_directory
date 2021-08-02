import django_tables2 as tables

from .models import (
    GenomicTestNov20,
    ClinicalIndicationNov20,
    GenomicTestJul21,
    ClinicalIndicationJul21,
    )


class Jul21MainTable(tables.Table):
    test_code = tables.LinkColumn(
        'jul21_test_detail',
        kwargs={"test_code": tables.A("test_code")},
        )
    
    ci_code = tables.LinkColumn(
        'jul21_ci_detail',
        kwargs={"ci_code": tables.A("ci_code__ci_code")},
        )

    class Meta:
        model = GenomicTestJul21
        fields = [
            'ci_code__cancer_id__cancer_type',
            'ci_code',
            'test_code',
            'test_name',
            'targets_essential',
            'targets_desirable',
            'scope_id__test_scope',
            'tech_id__technology',
            'provided_id__provided',
            'inhouse_id__inhouse',
            'tt_id__tt_code',
            ]


class Jul21CITable(tables.Table):
    ci_code = tables.LinkColumn(
        'jul21_ci_detail',
        kwargs={"ci_code": tables.A("ci_code")},
        )

    class Meta:
        model = ClinicalIndicationJul21
        fields = [
            'cancer_id',
            'ci_code',
            'ci_name',
            ]


class Jul21CIDetailTable(tables.Table):
    test_code = tables.LinkColumn(
        'jul21_test_detail',
        kwargs={"test_code": tables.A("test_code")},
        )

    class Meta:
        model = GenomicTestJul21
        fields = [
            'test_code',
            'test_name',
            'cc_id__commissioning',
            'eligibility',
            'targets_essential',
            'targets_desirable',
            ]


class Nov20MainTable(tables.Table):
    test_code = tables.LinkColumn(
        'nov20_test_detail',
        kwargs={"test_code": tables.A("test_code")},
        )

    ci_code = tables.LinkColumn(
        'nov20_ci_detail',
        kwargs={"ci_code": tables.A("ci_code__ci_code")},
        )

    class Meta:
        model = GenomicTestNov20
        fields = [
            'ci_code__cancer_id__cancer_type',
            'ci_code',
            'test_code',
            'test_name',
            'targets_essential',
            'scope_id__test_scope',
            'tech_id__technology',
            'inhouse_id__inhouse',
            'provided_id__provided',
            ]


class Nov20CITable(tables.Table):
    ci_code = tables.LinkColumn(
        'nov20_ci_detail',
        kwargs={"ci_code": tables.A("ci_code")},
        )

    class Meta:
        model = ClinicalIndicationNov20
        fields = [
            'cancer_id',
            'ci_code',
            'ci_name',
            ]


class Nov20CIDetailTable(tables.Table):
    test_code = tables.LinkColumn(
        'nov20_test_detail',
        kwargs={"test_code": tables.A("test_code")},
        )

    class Meta:
        model = GenomicTestNov20
        fields = [
            'test_code',
            'test_name',
            'eligibility',
            'targets_essential',
            ]
