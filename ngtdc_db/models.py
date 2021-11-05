from django.db import models


class CancerType(models.Model):
    """Table of discrete cancer type values"""

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
    """Table of discrete clinical indication (CI) code/name pair values"""

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


class TestScope(models.Model):
    """Table of discrete test scope values"""

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
    """Table of discrete technology values"""

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


class Target(models.Model):
    """Table of discrete genomic target values"""

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
    """Table of discrete genomic test records"""

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

    targets_essential = models.ManyToManyField(
        Target,
        through='EssentialTarget',
        verbose_name='Targets (Essential)',
        related_name = 'EssentialTarget_related',
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

    eligibility = models.TextField(
        verbose_name='Eligibility Criteria',
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
        return '{a} {b}'.format(a=self.test_id, b=self.target_id)
