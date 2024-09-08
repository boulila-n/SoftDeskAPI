from django.db import models
from django.utils import timezone

from users.models import User


class Project(models.Model):
    TYPE_CHOICES = (
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android')
    )
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    date_created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_created')
    contributors = models.ManyToManyField(User, related_name='projects_contributed_to')

    def __str__(self):
        return self.name


class Contributor(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.contributor.username


class Issue(models.Model):
    STATUT_CHOICES = (
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
    )
    PRIORITE_CHOICES = (
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH'),
    )
    BALISE_CHOICES = (
        ('BUG', 'BUG'),
        ('FEATURE', 'FEATURE'),
        ('TASK', 'TASK'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    assigne_a = models.ForeignKey(Contributor, on_delete=models.CASCADE,
                                  related_name='issues_assignees', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='To Do')
    priority = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='MEDIUM')
    balise = models.CharField(max_length=10, choices=BALISE_CHOICES, default='TASK')

    def __str__(self):
        return self.name


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    creator = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    texte = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    link_issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='linked_issue')

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()
        super(Comment, self).save(*args, **kwargs)