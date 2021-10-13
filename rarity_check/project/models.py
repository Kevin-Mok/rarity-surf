from django.db import models

class Project(models.Model):
    contract_address = models.CharField(max_length=42)
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)
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

class TokenType(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_token_type',
            fields=['project', 'name'])]

    def __str__(self):
        return f"{self.name}"

class Token(models.Model):
    project = models.ForeignKey('Project',
            on_delete=models.CASCADE)
    token_type = models.ForeignKey('TokenType',
            on_delete=models.CASCADE,
            blank=True, null=True)
    number = models.IntegerField()
    rank = models.IntegerField(blank=True, null=True)
    tools_rank = models.IntegerField(blank=True, null=True)
    traits = models.ManyToManyField(TraitValue)
    score = models.DecimalField(blank=True, null=True,
            max_digits=9, decimal_places=2)
    os_url = models.URLField()
    image_url = models.URLField()

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique_token',
            fields=['project', 'token_type', 'number'])]
        ordering = ['-score']

    def __str__(self):
        no_type = f"{self.project} #{self.number}"
        has_type = f"{self.token_type} #{self.number} ({self.project})"
        return no_type if self.token_type is None else has_type
        #  return f"{self.token_type} #{self.number} ({self.project})"
