from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig

from .models import (
    GenomicTestNov20,
    GenomicTestJul21,
    EssentialTargetLinksNov20,
    EssentialTargetLinksJul21,
    DesirableTargetLinksJul21,
    )
from .tables import Nov20_Table, Jul21_Table
from .filters import Nov20_Filter, Jul21_Filter


class Jul21_View(ListView):
    model = GenomicTestJul21
    template_name = 'ngtdc_db/jul21_list.html'

    def get_context_data(self, **kwargs):
        context = super(Jul21_View, self).get_context_data(**kwargs)

        filter = Jul21_Filter(self.request.GET, queryset=self.object_list)
        table = Jul21_Table(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table

        return context


def jul21_detail(request, test_code):
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
        'ngtdc_db/jul21_detail.html',
        {
            'test_record' : test_record,
            'essential_links' : essential_links, 
            'desirable_links' : desirable_links
        },
        )


class Nov20_View(ListView):
    model = GenomicTestNov20
    template_name = 'ngtdc_db/nov20_list.html'

    def get_context_data(self, **kwargs):
        context = super(Nov20_View, self).get_context_data(**kwargs)

        filter = Nov20_Filter(self.request.GET, queryset=self.object_list)
        table = Nov20_Table(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table

        return context


def nov20_detail(request, test_code):
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
        'ngtdc_db/nov20_detail.html',
        {
            'test_record' : test_record,
            'essential_links' : essential_links, 
        },
        )
