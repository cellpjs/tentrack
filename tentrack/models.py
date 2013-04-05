import datetime
import math
from django.db import models
# from django.forms import ModelForm
from django.utils import timezone

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=30) #primary_key=True?
    points = models.IntegerField(default=800)
    def __unicode__(self):
        return self.name

class Week(models.Model):
    open = models.BooleanField()
    def __unicode__(self):
        return u"%d" % self.id
    def finalize(self):
        #check and remove duplicates -- also in forms.py
        matches = self.match_set.all().order_by('id')
        clist = []
        dlist = []
        for m in matches:
            tt = []
            pp = m.player_w.all().order_by('id') # pp[0].id <= pp[1].id
            tt.append(pp[1].id*(pp[1].id+1)/2+pp[0].id)
            pp = m.player_l.all().order_by('id')
            tt.append(pp[1].id*(pp[1].id+1)/2+pp[0].id)
            tt.sort() # tt[0] <= tt[1]
            c = tt[1]*(tt[1]+1)/2+tt[0]
            if c in clist:
                dlist.append(m.id)
            else:
                clist.append(c)
        duplicates = self.match_set.filter(id__in=dlist)
        duplicates.delete()
        # apply points
        matches = self.match_set.all()
        for m in matches:
            for p in m.player_w.all():
                p.points+=m.pgain
                p.save()
            for p in m.player_l.all():
                p.points-=m.pgain/2
                p.save()
        # keep points >= 400
        for m in matches:
            for p in m.player_w.all():
                p.points=max(400, p.points)
                p.save()
            for p in m.player_l.all():
                p.points=max(400, p.points)
                p.save() 


class Match(models.Model):
    date = models.DateTimeField()
    week = models.ForeignKey(Week) # each Match is related to a single Week
    player_w = models.ManyToManyField(Player, related_name='match_w')
    player_l = models.ManyToManyField(Player, related_name='match_l')
    SCORE_CHOICES = ((0,'6:0'),(1,'6:1'),(2,'6:2'),(3,'6:3'),(4,'6:4'),(5,'6:5 TB'))
    score = models.IntegerField(choices=SCORE_CHOICES)
    pgain = models.IntegerField()
    def __unicode__(self):
        return u"%s" % self.date # more details?
    #def was_played_recently(self):
    #    return self.date >= timezone.now() - datetime.timedelta(days=7)
    def calculate_pgain(self):
        team_w = self.player_w.all()
        team_l = self.player_l.all()
        R_w = sum(p.points for p in team_w)/len(team_w)
        R_l = sum(p.points for p in team_l)/len(team_w)
        Q_w=math.pow(10,R_w/400.)
        Q_l=math.pow(10,R_l/400.)
        E_w=Q_w/(Q_w+Q_l)
        self.pgain=int(32*(1-E_w))

    class Meta:
        ordering = ['-id']

# class MatchResultForm(ModelForm):
#    class Meta:
#        model = Match
#        exclude = ('date', 'week', 'pgain')

# player statistics can be derived from matches
# wins
# losses
# f(wins,losses)
# partners
# opponents


