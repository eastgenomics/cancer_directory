from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig

from .models import (
    GenomicTestNov20,
    GenomicTestJul21,
    ClinicalIndicationNov20,
    ClinicalIndicationJul21,
    EssentialTargetLinksNov20,
    EssentialTargetLinksJul21,
    DesirableTargetLinksJul21,
    )

from .tables import (
    Nov20MainTable,
    Nov20CITable,
    Nov20CIDetailTable,
    Jul21MainTable,
    Jul21CITable,
    Jul21CIDetailTable,
    )
    
from .filters import (
    Nov20MainFilter,
    Nov20CIFilter,
    Jul21MainFilter,
    Jul21CIFilter,
    )


class Jul21MainList(ListView):
    model = GenomicTestJul21
    template_name = 'ngtdc_db/jul21_main_list.html'

    def get_context_data(self, **kwargs):
        context = super(Jul21MainList, self).get_context_data(**kwargs)

        filter = Jul21MainFilter(self.request.GET, queryset=self.object_list)
        table = Jul21MainTable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table

        return context


class Jul21CIList(ListView):
    model = ClinicalIndicationJul21
    template_name = 'ngtdc_db/jul21_ci_list.html'

    def get_context_data(self, **kwargs):
        context = super(Jul21CIList, self).get_context_data(**kwargs)

        filter = Jul21CIFilter(self.request.GET, queryset=self.object_list)
        table = Jul21CITable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table

        return context


def jul21_test_detail(request, test_code):
    test_record = GenomicTestJul21.objects.select_related(
        'ci_code',
        'ci_code__cancer_id',
        'specialist_id',
        'scope_id',
        'tech_id',
        'inhouse_id',
        'cc_id',
        'family_id',
        'provided_id',
        'citt_id',
        'tt_id',
        ).get(test_code = test_code)
    
    essential_links = EssentialTargetLinksJul21.objects.filter(
        test_code = test_code
        )

    desirable_links = DesirableTargetLinksJul21.objects.filter(
        test_code = test_code
        )

    return render(
        request,
        'ngtdc_db/jul21_test_detail.html',
        {
            'test_record' : test_record,
            'essential_links' : essential_links, 
            'desirable_links' : desirable_links
        },
        )


def jul21_ci_detail(request, ci_code):
    ci_record = ClinicalIndicationJul21.objects.get(ci_code = ci_code)

    ci_tests = GenomicTestJul21.objects.select_related(
        'ci_code', 'cc_id').filter(ci_code = ci_code)
        
    tests_table = Jul21CIDetailTable(ci_tests)

    return render(
        request,
        'ngtdc_db/jul21_ci_detail.html',
        {
            'ci_record' : ci_record,
            'tests_table' : tests_table
        },
        )


class Nov20MainList(ListView):
    model = GenomicTestNov20
    template_name = 'ngtdc_db/nov20_main_list.html'

    def get_context_data(self, **kwargs):
        context = super(Nov20MainList, self).get_context_data(**kwargs)

        filter = Nov20MainFilter(self.request.GET, queryset=self.object_list)
        table = Nov20MainTable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table

        return context


class Nov20CIList(ListView):
    model = ClinicalIndicationNov20
    template_name = 'ngtdc_db/nov20_ci_list.html'

    def get_context_data(self, **kwargs):
        context = super(Nov20CIList, self).get_context_data(**kwargs)

        filter = Nov20CIFilter(self.request.GET, queryset=self.object_list)
        table = Nov20CITable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table

        return context


def nov20_test_detail(request, test_code):
    test_record = GenomicTestNov20.objects.select_related(
        'ci_code',
        'ci_code__cancer_id',
        'scope_id',
        'tech_id',
        'inhouse_id',
        'provided_id',
        ).get(test_code = test_code)
    
    essential_links = EssentialTargetLinksNov20.objects.filter(
        test_code = test_code
        )

    return render(
        request,
        'ngtdc_db/nov20_test_detail.html',
        {
            'test_record' : test_record,
            'essential_links' : essential_links, 
        },
        )


def nov20_ci_detail(request, ci_code):
    ci_record = ClinicalIndicationNov20.objects.get(ci_code = ci_code)

    ci_tests = GenomicTestNov20.objects.select_related(
        'ci_code').filter(ci_code = ci_code)
        
    tests_table = Nov20CIDetailTable(ci_tests)

    return render(
        request,
        'ngtdc_db/nov20_ci_detail.html',
        {
            'ci_record' : ci_record,
            'tests_table' : tests_table
        },
        )
