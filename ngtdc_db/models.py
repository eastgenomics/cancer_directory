from django.db import models


"""
Section 2: Models for data from 2nd directory version (July 2021)

"""


class CancerTypeJul21(models.Model):
    """Table of general cancer types (from test directory worksheet names)"""

    cancer_id = models.AutoField(
        primary_key = True,
        )

    cancer_type = models.CharField(
        verbose_name='Cancer Type',
        max_length=25,
        )

    def __str__(self):
        return self.cancer_type


class ClinicalIndicationJul21(models.Model):
    """Table of clinical indication (CI) codes and names"""
    
    cancer_id = models.ForeignKey(
        CancerTypeJul21,
        verbose_name='Cancer Type',
        on_delete=models.CASCADE,
        )

    ci_code = models.CharField(
        primary_key=True,
        verbose_name='CI Code',
        max_length=15,
        )

    ci_name = models.TextField(
        verbose_name='CI Name',
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.ci_code, b=self.ci_name)


class SpecialistJul21(models.Model):
    """Table of specialist test groups"""

    specialist_id = models.AutoField(
        primary_key = True,
        )

    specialist_group = models.CharField(
        verbose_name='Specialist Test Group',
        max_length=25, 
        )

    def __str__(self):
        return self.specialist_group


class ScopeJul21(models.Model):
    """Table of possible test scopes"""

    scope_id = models.AutoField(
        primary_key = True,
        )

    test_scope = models.CharField(
        verbose_name='Test Scope',
        max_length=150,
        )

    class Meta:
        ordering = ['test_scope']

    def __str__(self):
        return self.test_scope


class TechnologyJul21(models.Model):
    """Table of possible test technologies"""

    tech_id = models.AutoField(
        primary_key = True,
        )

    technology = models.CharField(
        verbose_name='Technology',
        max_length=50,
        )

    class Meta:
        ordering = ['technology']

    def __str__(self):
        return self.technology


class InHouseTestJul21(models.Model):
    """Table of possible in-house test technologies"""

    inhouse_id = models.AutoField(
        primary_key = True,
        )

    inhouse = models.CharField(
        verbose_name='In-House Test',
        max_length=100,
        )

    class Meta:
        ordering = ['inhouse']

    def __str__(self):
        return self.inhouse


class CommissioningCategoryJul21(models.Model):
    """Table of commissioning categories"""

    cc_id = models.AutoField(
        primary_key = True,
        )

    commissioning = models.CharField(
        verbose_name='Commissioning Category',
        max_length=10, 
        )

    def __str__(self):
        return self.commissioning


class FamilyStructureJul21(models.Model):
    """Table of optimal family structure values"""

    family_id = models.AutoField(
        primary_key = True,
        )

    family_structure = models.CharField(
        verbose_name='Optimal Family Structure',
        max_length=10, 
        )

    def __str__(self):
        return self.family_structure


class CITTJul21(models.Model):
    """Table of CITT comment values"""

    citt_id = models.AutoField(
        primary_key = True,
        )

    citt_comment = models.TextField(
        verbose_name='CITT Comment',
        )

    def __str__(self):
        return self.citt_comment


class TTJul21(models.Model):
    """Table of CITT comment values"""

    tt_id = models.AutoField(
        primary_key = True,
        )

    tt_code = models.CharField(
        verbose_name='TT Code',
        max_length=10, 
        )

    def __str__(self):
        return self.tt_code


class CurrentlyProvidedJul21(models.Model):
    """Table of possible values for whether test is currently provided
    in-house"""

    provided_id = models.AutoField(
        primary_key = True,
        )

    provided = models.CharField(
        verbose_name='Currently Provided',
        max_length=15,
        )

    def __str__(self):
        return self.provided


class TargetJul21(models.Model):
    """Table of possible genomic targets"""

    target_id = models.AutoField(
        primary_key = True,
        )

    target = models.CharField(
        verbose_name='Target',
        max_length=100,
        )
    
    hgnc_id = models.CharField(
        verbose_name='HGNC ID',
        max_length=50,
    )

    def __str__(self):
        return self.target


class GenomicTestJul21(models.Model):
    """Table of genomic test codes, names, and eligibility criteria"""
    
    ci_code = models.ForeignKey(
        ClinicalIndicationJul21,
        verbose_name='CI Code',
        on_delete=models.CASCADE,
        )

    test_code = models.CharField(
        primary_key=True,
        verbose_name='Test Code',
        max_length=15,
        )
    
    test_name = models.TextField(
        verbose_name='Test Name',
        )

    specialist_id = models.ForeignKey(
        SpecialistJul21,
        verbose_name = 'Specialist Test Group',
        on_delete=models.CASCADE,
    )

    targets_essential = models.ManyToManyField(
        TargetJul21,
        through='EssentialTargetLinksJul21',
        verbose_name='Targets (Essential)',
        related_name = 'EssentialTargetLinks_related',
        )

    targets_desirable = models.ManyToManyField(
        TargetJul21,
        through='DesirableTargetLinksJul21',
        verbose_name='Targets (Desirable)',
        related_name = 'DesirableTargetLinks_related',
        )

    scope_id = models.ForeignKey(
        ScopeJul21,
        verbose_name='Test Scope',
        on_delete=models.CASCADE,
        )

    tech_id = models.ForeignKey(
        TechnologyJul21,
        verbose_name='Technology',
        on_delete=models.CASCADE,
    )

    inhouse_id = models.ForeignKey(
        InHouseTestJul21,
        verbose_name='In-House Test',
        on_delete=models.CASCADE,
    )

    cc_id = models.ForeignKey(
        CommissioningCategoryJul21,
        verbose_name = 'Commissioning Category',
        on_delete=models.CASCADE,
    )

    eligibility = models.TextField(
        verbose_name='Eligibility Criteria',
        )

    family_id = models.ForeignKey(
        FamilyStructureJul21,
        verbose_name='Optimal Family Structure',
        on_delete=models.CASCADE,
    )

    provided_id = models.ForeignKey(
        CurrentlyProvidedJul21,
        verbose_name='Currently Provided',
        on_delete=models.CASCADE,
    )

    citt_id = models.ForeignKey(
        CITTJul21,
        verbose_name = 'CITT Comment',
        on_delete=models.CASCADE,
    )

    tt_id = models.ForeignKey(
        TTJul21,
        verbose_name = 'TT Code',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.test_code


class EssentialTargetLinksJul21(models.Model):
    """Intermediate table linking each test to its essential targets"""

    test_code = models.ForeignKey(
        GenomicTestJul21,
        verbose_name='Test Code',
        on_delete=models.CASCADE,
        )

    target_id = models.ForeignKey(
        TargetJul21,
        verbose_name='Target',
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.test_code, b=self.target_id)


class DesirableTargetLinksJul21(models.Model):
    """Intermediate table linking each test to its desirable targets"""

    test_code = models.ForeignKey(
        GenomicTestJul21,
        verbose_name='Test Code',
        on_delete=models.CASCADE,
        )

    target_id = models.ForeignKey(
        TargetJul21,
        verbose_name='Target',
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.test_code, b=self.target_id)


"""
Section 1: Models for data from 1st directory version (November 2020)

"""


class CancerTypeNov20(models.Model):
    """Table of general cancer types (from test directory worksheet names)"""

    cancer_id = models.AutoField(
        primary_key = True,
        )

    cancer_type = models.CharField(
        verbose_name='Cancer Type',
        max_length=25, 
        )

    def __str__(self):
        return self.cancer_type


class ClinicalIndicationNov20(models.Model):
    """Table of clinical indication (CI) codes and names"""
    
    cancer_id = models.ForeignKey(
        CancerTypeNov20,
        verbose_name='Cancer Type',
        on_delete=models.CASCADE,
        )

    ci_code = models.CharField(
        primary_key=True,
        verbose_name='CI Code',
        max_length=15,
        )

    ci_name = models.TextField(
        verbose_name='CI Name',
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.ci_code, b=self.ci_name)


class ScopeNov20(models.Model):
    """Table of possible test scopes"""

    scope_id = models.AutoField(
        primary_key = True,
        )

    test_scope = models.CharField(
        verbose_name='Test Scope',
        max_length=150,
        )

    class Meta:
        ordering = ['test_scope']

    def __str__(self):
        return self.test_scope


class TechnologyNov20(models.Model):
    """Table of possible test technologies"""

    tech_id = models.AutoField(
        primary_key = True,
        )

    technology = models.CharField(
        verbose_name='Technology',
        max_length=50,
        )

    class Meta:
        ordering = ['technology']

    def __str__(self):
        return self.technology


class InHouseTestNov20(models.Model):
    """Table of possible in-house test technologies"""

    inhouse_id = models.AutoField(
        primary_key = True,
        )

    inhouse = models.CharField(
        verbose_name='In-House Test',
        max_length=100,
        )

    class Meta:
        ordering = ['inhouse']

    def __str__(self):
        return self.inhouse


class CurrentlyProvidedNov20(models.Model):
    """Table of possible values for whether test is currently provided
    in-house"""

    provided_id = models.AutoField(
        primary_key = True,
        )

    provided = models.CharField(
        verbose_name='Currently Provided',
        max_length=15,
        )

    def __str__(self):
        return self.provided


class TargetNov20(models.Model):
    """Table of possible genomic targets"""

    target_id = models.AutoField(
        primary_key = True,
        )

    target = models.CharField(
        verbose_name='Target',
        max_length=100,
        )

    hgnc_id = models.CharField(
        verbose_name='HGNC ID',
        max_length=50,
    )

    def __str__(self):
        return self.target


class GenomicTestNov20(models.Model):
    """Table of genomic test codes, names, and eligibility criteria"""
    
    ci_code = models.ForeignKey(
        ClinicalIndicationNov20,
        verbose_name='CI Code',
        on_delete=models.CASCADE,
        )

    test_code = models.CharField(
        primary_key=True,
        verbose_name='Test Code',
        max_length=15,
        )
    
    test_name = models.TextField(
        verbose_name='Test Name',
        )

    targets_essential = models.ManyToManyField(
        TargetNov20,
        through='EssentialTargetLinksNov20',
        verbose_name='Targets (Essential)',
        related_name = 'EssentialTargetLinks_related',
        )

    scope_id = models.ForeignKey(
        ScopeNov20,
        verbose_name='Test Scope',
        on_delete=models.CASCADE,
        )

    tech_id = models.ForeignKey(
        TechnologyNov20,
        verbose_name='Technology',
        on_delete=models.CASCADE,
    )

    inhouse_id = models.ForeignKey(
        InHouseTestNov20,
        verbose_name='In-House Test',
        on_delete=models.CASCADE,
    )

    eligibility = models.TextField(
        verbose_name='Eligibility Criteria',
        )

    provided_id = models.ForeignKey(
        CurrentlyProvidedNov20,
        verbose_name='Currently Provided',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.test_code


class EssentialTargetLinksNov20(models.Model):
    """Intermediate table linking each test to its essential targets"""

    test_code = models.ForeignKey(
        GenomicTestNov20,
        verbose_name='Test Code',
        on_delete=models.CASCADE,
        )

    target_id = models.ForeignKey(
        TargetNov20,
        verbose_name='Target',
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.test_code, b=self.target_id)
