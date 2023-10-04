from django.db import models
from users.models import Profile


# Create your models here.


class Repair(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(blank=True, null=True,
                                       upload_to='repairs/%Y/%m/%d',
                                       default='default.jpg')
    demo_link = models.CharField(max_length=200, blank=True, null=True)
    source_link = models.CharField(max_length=200, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote = models.IntegerField(default=0)
    vote_percent = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_percent', '-vote', 'title']  # -created

    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    def get_vote_count(self):
        reviews = self.review_set.all()
        up_voted = reviews.filter(value='up').count()
        total_votes = reviews.count()

        ration = (up_voted / total_votes) * 100
        self.vote = total_votes
        self.vote_percent = ration

        self.save()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Проголосовать положительно'),
        ('down', 'Проголосовать отрицательно'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=100, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'repair']]
