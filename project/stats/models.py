from django.db import models
from userK.models import CustomUser
from .services import get_sym_plus_if_num_is_positive
from django.utils import timezone


class ScoreHistory(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    score = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} | {}{}'.format(self.player.username,
                                  get_sym_plus_if_num_is_positive(self.score),
                                  self.score)

    def save(self, *args, **kwargs):
        super(ScoreHistory, self).save(*args, **kwargs)
        self.player.save()
