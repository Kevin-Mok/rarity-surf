from django.db import models

class Project(models.Model):
    contract_address = models.CharField(max_length=42)
    name = models.CharField(max_length=20, unique=True)
    max_supply = models.IntegerField()
    ipfs_hash = models.CharField(max_length=46, blank=True)
    api_url = models.URLField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_project',
            fields=['contract_address', 'name'])]
        ordering = ['name']

    def __str__(self):
        return self.name

class TraitType(models.Model):
    project = models.ForeignKey('Project',
            on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_trait_type',
            fields=['project', 'name'])]
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.project})"

class TraitValue(models.Model):
    trait_type = models.ForeignKey('TraitType',
            on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    rarity = models.DecimalField(blank=True, null=True,
            max_digits=4, decimal_places=2)
    score = models.DecimalField(blank=True, null=True,
            max_digits=8, decimal_places=2)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_trait_value',
            fields=['trait_type', 'name'])]
        ordering = ['rarity']

    def __str__(self):
        return f"{self.name} [ {self.trait_type} ]"

class Token(models.Model):
    project = models.ForeignKey('Project',
            on_delete=models.CASCADE)
    number = models.IntegerField()
    traits = models.ManyToManyField(TraitValue)
    score = models.DecimalField(blank=True, null=True,
            max_digits=9, decimal_places=2)
    os_url = models.URLField()
    image_url = models.URLField()

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_token',
            fields=['project', 'number'])]
        ordering = ['-score']

    def __str__(self):
        return f"{self.project} #{self.number}"
