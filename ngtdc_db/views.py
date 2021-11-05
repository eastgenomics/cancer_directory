from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig

from .models import (
    GenomicTest,
    ClinicalIndication,
    EssentialTarget,
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
    """View class to display all genomic test records from directory version
    1 as a table. Uses V1MainTable table with V1MainFilter filter."""

    # Specify the model used in this view and the template to display it in
    model = GenomicTest
    template_name = 'ngtdc_db/main_list.html'

    def get_queryset(self, **kwargs):
        """Define the queryset as only GenomicTest records from directory
        version 1."""

        queryset = GenomicTest.objects.filter(version = '1')
        return queryset

    def get_context_data(self, **kwargs):
        """Specify which table and filter to apply to the model."""

        context = super(V1MainList, self).get_context_data(**kwargs)
        filter = V1MainFilter(self.request.GET, queryset=self.object_list)
        table = V1MainTable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '1'

        return context


class V2MainList(ListView):
    """View class to display all genomic test records from directory version
    2 as a table. Uses V2MainTable table with V2MainFilter filter."""

    # Specify the model used in this view and the template to display it in
    model = GenomicTest
    template_name = 'ngtdc_db/main_list.html'

    def get_queryset(self, **kwargs):
        """Define the queryset as only GenomicTest records from directory
        version 2."""

        queryset = GenomicTest.objects.filter(version = '2')
        return queryset

    def get_context_data(self, **kwargs):
        """Specify which table and filter to apply to the model."""

        context = super(V2MainList, self).get_context_data(**kwargs)
        filter = V2MainFilter(self.request.GET, queryset=self.object_list)
        table = V2MainTable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '2'

        return context


class V1CIList(ListView):
    """View class to display all clinical indication values from directory
    version 1 as a table. Uses V1CITable table with V1CIFilter filter."""

    # Specify the model used in this view and the template to display it in
    model = ClinicalIndication
    template_name = 'ngtdc_db/ci_list.html'

    def get_queryset(self):
        """Define the queryset as all ClinicalIndication records."""

        queryset = ClinicalIndication.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        """Specify which table and filter to apply to the model."""

        context = super(V1CIList, self).get_context_data(**kwargs)
        filter = V1CIFilter(self.request.GET, queryset=self.object_list)
        table = V1CITable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '1'

        return context


class V2CIList(ListView):
    """View class to display all clinical indication values from directory
    version 2 as a table. Uses V2CITable table with V2CIFilter filter."""

    # Specify the model used in this view and the template to display it in
    model = ClinicalIndication
    template_name = 'ngtdc_db/ci_list.html'

    def get_queryset(self):
        """Define the queryset as all ClinicalIndication records."""

        queryset = ClinicalIndication.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        """Specify which table and filter to apply to the model."""

        context = super(V2CIList, self).get_context_data(**kwargs)
        filter = V2CIFilter(self.request.GET, queryset=self.object_list)
        table = V2CITable(filter.qs)

        RequestConfig(self.request, ).configure(table )
        context['filter'] = filter
        context['table'] = table
        context['directory_version'] = '2'

        return context


def v1_test_detail(request, test_id):
    """View function to display information from a specific genomic test
    record (from directory version 1)."""

    # Allow accessing fields in other linked tables
    test_record = GenomicTest.objects.select_related(
        'ci_code',
        'ci_code__cancer_id',
        'scope_id',
        'tech_id',
        ).get(test_id = test_id)
    
    # Get the essential targets associated with this test ID
    essential_links = EssentialTarget.objects.filter(
        test_id = test_id
        )

    # Specify the directory version for the view
    directory_version = '1'

    # Render the view in the specified template, passing the listed arguments
    return render(
        request,
        'ngtdc_db/test_detail.html',
        {
            'test_record' : test_record,
            'essential_links' : essential_links,
            'directory_version' : directory_version,
        },
        )


def v2_test_detail(request, test_id):
    """View function to display information from a specific genomic test
    record (from directory version 2)."""

    # Allow accessing fields in other linked tables
    test_record = GenomicTest.objects.select_related(
        'ci_code',
        'ci_code__cancer_id',
        'scope_id',
        'tech_id',
        ).get(test_id = test_id)
    
    # Get the essential targets associated with this test ID
    essential_links = EssentialTarget.objects.filter(
        test_id = test_id
        )

    # Specify the directory version for the view
    directory_version = '2'

    # Render the view in the specified template, passing the listed arguments
    return render(
        request,
        'ngtdc_db/test_detail.html',
        {
            'test_record' : test_record,
            'essential_links' : essential_links, 
            'directory_version' : directory_version,
        },
        )


def v1_ci_detail(request, ci_code):
    """View function to display tests associated with a specific clinical
    indication record (from directory version 1)."""

    # Get the ClinicalIndication record for this CI code
    ci_record = ClinicalIndication.objects.get(ci_code = ci_code)

    # Get the GenomicTest records which have this CI code and are from
    # directory version 1
    ci_tests = GenomicTest.objects.select_related('ci_code').filter(
        ci_code = ci_code,
        version = '1'
        )
    
    # Specify which table to display the queryset in
    tests_table = V1CIDetailTable(ci_tests)

    # Specify the directory version for the view
    directory_version = '1'

    # Render the view in the specified template, passing the listed arguments
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
    """View function to display tests associated with a specific clinical
    indication record (from directory version 2)."""

    # Get the ClinicalIndication record for this CI code
    ci_record = ClinicalIndication.objects.get(ci_code = ci_code)

    # Get the GenomicTest records which have this CI code and are from
    # directory version 2
    ci_tests = GenomicTest.objects.select_related('ci_code').filter(
        ci_code = ci_code,
        version = '2'
        )

    # Specify which table to display the queryset in
    tests_table = V2CIDetailTable(ci_tests)

    # Specify the directory version for the view
    directory_version = '2'

    # Render the view in the specified template, passing the listed arguments
    return render(
        request,
        'ngtdc_db/ci_detail.html',
        {
            'directory_version' : directory_version,
            'ci_record' : ci_record,
            'tests_table' : tests_table
        },
        )
