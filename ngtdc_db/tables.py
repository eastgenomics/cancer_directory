import django_tables2 as tables
from .models import GenomicTest


class GenomicTestTable(tables.Table):
    test_code = tables.LinkColumn('test_detail',
        kwargs={"test_code": tables.A("test_code")})

    class Meta:
        model = GenomicTest
        fields = [
            'ci_code__cancer_type',
            'ci_code',
            'test_code',
            'test_name',
            'targets',
            'test_scope',
            'technology',
            ]
