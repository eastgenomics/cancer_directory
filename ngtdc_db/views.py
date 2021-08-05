from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig

from .models import (
    GenomicTest,
    ClinicalIndication,
    EssentialTarget,
    DesirableTarget,
    )

from .tables import (
    V1MainTable,
    V2MainTable,
    V1CITable,
    V2CITable,
    V1CIDetailTable,
    V2CIDetailTable,
    )
    
from .filters import (
    V1MainFilter,
    V2MainFilter,
    V1CIFilter,
    V2CIFilter,
    )


class V1MainList(ListView):
    model = GenomicTest
    template_name = 'ngtdc_db/main_list.html'

    def get_queryset(self, **kwargs):
        queryset = GenomicTest.objects.filter(version = '1')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(V1MainList, self).get_context_data(**kwargs)
        filter = V1MainFilter(self.request.GET, queryset=self.object_list)
        table = V1MainTable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '1'

        return context


class V2MainList(ListView):
    model = GenomicTest
    template_name = 'ngtdc_db/main_list.html'
    directory_version = '2'

    def get_queryset(self, **kwargs):
        queryset = GenomicTest.objects.filter(version = '2')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(V2MainList, self).get_context_data(**kwargs)
        filter = V2MainFilter(self.request.GET, queryset=self.object_list)
        table = V2MainTable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '2'

        return context


class V1CIList(ListView):
    model = ClinicalIndication
    template_name = 'ngtdc_db/ci_list.html'
    directory_version = '1'

    def get_queryset(self):
        queryset = ClinicalIndication.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(V1CIList, self).get_context_data(**kwargs)
        filter = V1CIFilter(self.request.GET, queryset=self.object_list)
        table = V1CITable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '1'

        return context


class V2CIList(ListView):
    model = ClinicalIndication
    template_name = 'ngtdc_db/ci_list.html'
    directory_version = '2'

    def get_queryset(self):
        queryset = ClinicalIndication.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(V2CIList, self).get_context_data(**kwargs)
        filter = V2CIFilter(self.request.GET, queryset=self.object_list)
        table = V2CITable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '2'

        return context


def v1_test_detail(request, test_id):
    directory_version = '1'

    test_record = GenomicTest.objects.select_related(
        'ci_code',
        'ci_code__cancer_id',
        'scope_id',
        'tech_id',
        ).get(test_id = test_id)
    
    essential_links = EssentialTarget.objects.filter(
        test_id = test_id
        )

    return render(
        request,
        'ngtdc_db/test_detail.html',
        {
            'directory_version' : directory_version,
            'test_record' : test_record,
            'essential_links' : essential_links, 
        },
        )


def v2_test_detail(request, test_id):
    directory_version = '2'

    test_record = GenomicTest.objects.select_related(
        'ci_code',
        'ci_code__cancer_id',
        'specialist_id',
        'scope_id',
        'tech_id',
        'cc_id',
        'family_id',
        'citt_id',
        ).get(test_id = test_id)
    
    essential_links = EssentialTarget.objects.filter(
        test_id = test_id
        )

    desirable_links = DesirableTarget.objects.filter(
        test_id = test_id
        )

    return render(
        request,
        'ngtdc_db/test_detail.html',
        {
            'directory_version' : directory_version,
            'test_record' : test_record,
            'essential_links' : essential_links, 
            'desirable_links' : desirable_links
        },
        )


def v1_ci_detail(request, ci_code):
    directory_version = '1'

    ci_record = ClinicalIndication.objects.get(ci_code = ci_code)

    ci_tests = GenomicTest.objects.select_related('ci_code').filter(
        ci_code = ci_code,
        version = '1'
        )
        
    tests_table = V1CIDetailTable(ci_tests)

    return render(
        request,
        'ngtdc_db/ci_detail.html',
        {
            'directory_version' : directory_version,
            'ci_record' : ci_record,
            'tests_table' : tests_table
        },
        )


def v2_ci_detail(request, ci_code):
    directory_version = '2'

    ci_record = ClinicalIndication.objects.get(ci_code = ci_code)

    ci_tests = GenomicTest.objects.select_related('ci_code').filter(
        ci_code = ci_code,
        version = '2'
        )
        
    tests_table = V2CIDetailTable(ci_tests)

    return render(
        request,
        'ngtdc_db/ci_detail.html',
        {
            'directory_version' : directory_version,
            'ci_record' : ci_record,
            'tests_table' : tests_table
        },
        )
