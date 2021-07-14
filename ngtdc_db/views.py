from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig

from .models import GenomicTest
from .tables import GenomicTestTable
from .filters import GenomicTestFilter


class TableListView(ListView):
    model = GenomicTest

    def get_context_data(self, **kwargs):
        context = super(TableListView, self).get_context_data(**kwargs)
        filter = GenomicTestFilter(self.request.GET, queryset=self.object_list)
        
        table = GenomicTestTable(filter.qs)
        RequestConfig(self.request, ).configure(table )

        context['filter'] = filter
        context['table'] = table
        return context


def test_detail(request, test_code):
    test_record = GenomicTest.objects.select_related(
        'ci_code',
        'ci_code__cancer_type',
        'test_scope',
        'technology',
        ).get(test_code = test_code)

    return render(request, 'ngtdc_db/test_info.html',
        {'test_record' : test_record})
