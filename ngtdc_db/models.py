from django.db import models


class CancerType(models.Model):
    """Table of general cancer types (from test directory worksheet names)"""

    cancer_id = models.AutoField(primary_key = True)

    cancer_type = models.CharField(
        max_length=25, 
        verbose_name='Cancer Type'
        )

    def __str__(self):
        return self.cancer_type


class ClinicalIndication(models.Model):
    """Table of clinical indication (CI) codes and names"""

    ci_code = models.CharField(
        primary_key=True, 
        max_length=15, 
        verbose_name='CI Code'
        )

    ci_name = models.TextField(
        verbose_name='CI Name'
        )
    
    cancer_type = models.ForeignKey(
        CancerType, 
        on_delete=models.CASCADE, 
        verbose_name='Cancer Type'
        )

    def __str__(self):
        return "%s %s" % (self.ci_code, self.ci_name)


class Scope(models.Model):
    """Table of possible test scopes"""

    scope_id = models.AutoField(primary_key = True)

    test_scope = models.CharField(
        max_length=150, 
        verbose_name='Test Scope'
        )

    class Meta:
        ordering = ['test_scope']

    def __str__(self):
        return self.test_scope


class Technology(models.Model):
    """Table of possible test technologies"""

    tech_id = models.AutoField(primary_key = True)

    technology = models.CharField(
        max_length=50, 
        verbose_name='Technology'
        )

    class Meta:
        ordering = ['technology']

    def __str__(self):
        return self.technology


class Target(models.Model):
    """Table of possible genomic targets"""

    target_id = models.AutoField(primary_key = True)

    target = models.CharField(
        max_length=100, 
        verbose_name='Target'
        )

    def __str__(self):
        return self.target


class GenomicTest(models.Model):
    """Table of genomic test codes, names, and eligibility criteria"""
    
    ci_code = models.ForeignKey(
        ClinicalIndication, 
        on_delete=models.CASCADE, 
        verbose_name='CI Code'
        )

    test_code = models.CharField(
        primary_key=True, 
        max_length=15, 
        verbose_name='Test Code'
        )
    
    test_name = models.TextField(
        verbose_name='Test Name'
        )

    targets = models.TextField(
        verbose_name='Targets'
        )

    test_scope = models.ForeignKey(
        Scope, 
        on_delete=models.CASCADE, 
        verbose_name='Test Scope'
        )

    technology = models.ForeignKey(
        Technology, 
        on_delete=models.CASCADE, 
        verbose_name='Technology'
        )

    eligibility = models.TextField(
        verbose_name='Eligibility Criteria'
        )

    def __str__(self):
        return "%s %s" % (self.test_code, self.test_name)
    
    def show_targets(self):
        """Create a string of a test's first 10 targets (required to display
        them in Admin)."""
        return ', '.join([target.target for target in self.targets.all()])

    show_targets.short_description = 'Targets'


# class LinkTestToTarget(models.Model):
#     """Intermediate table linking each test to its targets"""

#     test_target = models.ForeignKey(Target, on_delete=models.CASCADE)
#     test_code = models.ForeignKey(GenomicTest, on_delete=models.CASCADE)

#     def __str__(self):
#         return "%s %s" % (self.test_code, self.test_target)
