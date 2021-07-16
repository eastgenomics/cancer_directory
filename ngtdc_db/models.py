from django.db import models


class CancerType(models.Model):
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


class ClinicalIndication(models.Model):
    """Table of clinical indication (CI) codes and names"""
    
    cancer_id = models.ForeignKey(
        CancerType,
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


class Scope(models.Model):
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


class InHouseTest(models.Model):
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


class CurrentlyProvided(models.Model):
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


class Target(models.Model):
    """Table of possible genomic targets"""

    target_id = models.AutoField(
        primary_key = True,
        )

    target = models.CharField(
        verbose_name='Target',
        max_length=100,
        )

    def __str__(self):
        return self.target


class GenomicTest(models.Model):
    """Table of genomic test codes, names, and eligibility criteria"""
    
    ci_code = models.ForeignKey(
        ClinicalIndication,
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

    targets = models.ManyToManyField(
        Target,
        through='LinkTestToTarget',
        verbose_name='Targets',
        )

    scope_id = models.ForeignKey(
        Scope,
        verbose_name='Test Scope',
        on_delete=models.CASCADE,
        )

    tech_id = models.ForeignKey(
        Technology,
        verbose_name='Technology',
        on_delete=models.CASCADE,
    )

    inhouse_id = models.ForeignKey(
        InHouseTest,
        verbose_name='In-House Test',
        on_delete=models.CASCADE,
    )

    eligibility = models.TextField(
        verbose_name='Eligibility Criteria',
        )

    provided_id = models.ForeignKey(
        CurrentlyProvided,
        verbose_name='Currently Provided',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.test_code

    def target_string(self):
        """Create a string of a test's targets."""
        return ', '.join([target for target in self.targets])


class LinkTestToTarget(models.Model):
    """Intermediate table linking each test to its targets"""

    test_code = models.ForeignKey(
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
