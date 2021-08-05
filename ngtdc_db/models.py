from django.db import models


class CancerType(models.Model):
    """Table of general cancer types (from test directory worksheet
    names)
    """

    cancer_id = models.AutoField(
        primary_key = True,
        )

    cancer_type = models.CharField(
        verbose_name='Cancer Type',
        max_length=25,
        )

    def __str__(self):
        return self.cancer_type


class ClinicalIndication(models.Model):
    """Table of clinical indication (CI) codes and names"""

    cancer_id = models.ForeignKey(
        CancerType,
        verbose_name='Cancer Type',
        on_delete=models.CASCADE,
        )

    ci_code = models.CharField(
        primary_key = True,
        verbose_name='CI Code',
        max_length=15,
        )

    ci_name = models.TextField(
        verbose_name='CI Name',
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.ci_code, b=self.ci_name)


class SpecialistTestGroup(models.Model):
    """Table of specialist test groups"""

    specialist_id = models.AutoField(
        primary_key = True,
        )

    specialist_test_group = models.CharField(
        verbose_name='Specialist Test Group',
        max_length=25, 
        )

    def __str__(self):
        return self.specialist_test_group


class TestScope(models.Model):
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


class Technology(models.Model):
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


class CommissioningCategory(models.Model):
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


class OptimalFamilyStructure(models.Model):
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


class CITTComment(models.Model):
    """Table of CITT comment values"""

    citt_id = models.AutoField(
        primary_key = True,
        )

    citt_comment = models.TextField(
        verbose_name='CITT Comment',
        )

    def __str__(self):
        return self.citt_comment


class Target(models.Model):
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


class GenomicTest(models.Model):
    """Table of genomic test codes, names, and eligibility criteria"""

    test_id = models.AutoField(
        primary_key = True,
    )

    version = models.CharField(
        verbose_name='Test Directory Version',
        max_length=10,
    )

    ci_code = models.ForeignKey(
        ClinicalIndication,
        verbose_name='CI Code',
        on_delete=models.CASCADE,
        )

    test_code = models.CharField(
        verbose_name='Test Code',
        max_length=15,
        )
    
    test_name = models.TextField(
        verbose_name='Test Name',
        )

    specialist_id = models.ForeignKey(
        SpecialistTestGroup,
        verbose_name = 'Specialist Test Group',
        on_delete=models.CASCADE,
        )

    targets_essential = models.ManyToManyField(
        Target,
        through='EssentialTarget',
        verbose_name='Targets (Essential)',
        related_name = 'EssentialTarget_related',
        )

    targets_desirable = models.ManyToManyField(
        Target,
        through='DesirableTarget',
        verbose_name='Targets (Desirable)',
        related_name = 'DesirableTarget_related',
        )

    scope_id = models.ForeignKey(
        TestScope,
        verbose_name='Test Scope',
        on_delete=models.CASCADE,
        )

    tech_id = models.ForeignKey(
        Technology,
        verbose_name='Technology',
        on_delete=models.CASCADE,
        )

    currently_provided = models.CharField(
        verbose_name='Currently Provided',
        max_length=20,
        )

    inhouse_technology = models.TextField(
        verbose_name='In-House Test',
        )

    cc_id = models.ForeignKey(
        CommissioningCategory,
        verbose_name = 'Commissioning Category',
        on_delete=models.CASCADE,
        )

    eligibility = models.TextField(
        verbose_name='Eligibility Criteria',
        )

    family_id = models.ForeignKey(
        OptimalFamilyStructure,
        verbose_name='Optimal Family Structure',
        on_delete=models.CASCADE,
        )

    citt_id = models.ForeignKey(
        CITTComment,
        verbose_name = 'CITT Comment',
        on_delete=models.CASCADE,
        )

    tt_code = models.CharField(
        verbose_name = 'TT Code',
        max_length=10,
        )

    def __str__(self):
        return self.test_code


class EssentialTarget(models.Model):
    """Intermediate table linking each test to its essential targets"""

    test_id = models.ForeignKey(
        GenomicTest,
        verbose_name='Test Code',
        on_delete=models.CASCADE,
        )

    target_id = models.ForeignKey(
        Target,
        verbose_name='Target',
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.test_code, b=self.target_id)


class DesirableTarget(models.Model):
    """Intermediate table linking each test to its desirable targets"""

    test_id = models.ForeignKey(
        GenomicTest,
        verbose_name='Test Code',
        on_delete=models.CASCADE,
        )

    target_id = models.ForeignKey(
        Target,
        verbose_name='Target',
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return '{a} {b}'.format(a=self.test_code, b=self.target_id)
