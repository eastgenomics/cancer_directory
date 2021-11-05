import django_tables2 as tables

from .models import (
    GenomicTest,
    ClinicalIndication,
    )


class V1MainTable(tables.Table):
    # Define the test_code field as linking to the test_detail template
    test_code = tables.LinkColumn(
        'v1_test_detail',
        kwargs={"test_id": tables.A("test_id")},
        )

    # Define the ci_code field as linking to the ci_detail template
    ci_code = tables.LinkColumn(
        'v1_ci_detail',
        kwargs={"ci_code": tables.A("ci_code__ci_code")},
        )

    class Meta:
        model = GenomicTest
        fields = [
            'ci_code__cancer_id__cancer_type',
            'ci_code',
            'test_code',
            'test_name',
            'targets_essential',
            'scope_id__test_scope',
            'tech_id__technology',
            'currently_provided',
            'inhouse_technology',
            ]


class V2MainTable(tables.Table):
    # Define the test_code field as linking to the test_detail template
    test_code = tables.LinkColumn(
        'v2_test_detail',
        kwargs={"test_id": tables.A("test_id")},
        )
    
    # Define the ci_code field as linking to the ci_detail template
    ci_code = tables.LinkColumn(
        'v2_ci_detail',
        kwargs={"ci_code": tables.A("ci_code__ci_code")},
        )

    class Meta:
        model = GenomicTest
        fields = [
            'ci_code__cancer_id__cancer_type',
            'ci_code',
            'test_code',
            'test_name',
            'targets_essential',
            'scope_id__test_scope',
            'tech_id__technology',
            'currently_provided',
            'inhouse_technology',
            ]


class V1CITable(tables.Table):
    # Define the ci_code field as linking to the ci_detail template
    ci_code = tables.LinkColumn(
        'v1_ci_detail',
        kwargs={"ci_code": tables.A("ci_code")},
        )

    class Meta:
        model = ClinicalIndication
        fields = [
            'cancer_id',
            'ci_code',
            'ci_name',
            ]


class V2CITable(tables.Table):
    # Define the ci_code field as linking to the ci_detail template
    ci_code = tables.LinkColumn(
        'v2_ci_detail',
        kwargs={"ci_code": tables.A("ci_code")},
        )

    class Meta:
        model = ClinicalIndication
        fields = [
            'cancer_id',
            'ci_code',
            'ci_name',
            ]


class V1CIDetailTable(tables.Table):
    # Define the test_code field as linking to the test_detail template
    test_code = tables.LinkColumn(
        'v1_test_detail',
        kwargs={"test_id": tables.A("test_id")},
        )

    class Meta:
        model = GenomicTest
        fields = [
            'test_code',
            'test_name',
            'eligibility',
            'targets_essential',
            ]


class V2CIDetailTable(tables.Table):
    # Define the test_code field as linking to the test_detail template
    test_code = tables.LinkColumn(
        'v2_test_detail',
        kwargs={"test_id": tables.A("test_id")},
        )

    class Meta:
        model = GenomicTest
        fields = [
            'test_code',
            'test_name',
            'eligibility',
            'targets_essential',
            ]
