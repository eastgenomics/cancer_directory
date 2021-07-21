import django_tables2 as tables
from .models import GenomicTestNov20, GenomicTestJul21


class Jul21_Table(tables.Table):
    test_code = tables.LinkColumn(
        'jul21_detail',
        kwargs={"test_code": tables.A("test_code")},
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
            'inhouse_id__inhouse',
            'provided_id__provided',
            'tt_id__tt_code',
            ]


class Nov20_Table(tables.Table):
    test_code = tables.LinkColumn(
        'nov20_detail',
        kwargs={"test_code": tables.A("test_code")},
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
