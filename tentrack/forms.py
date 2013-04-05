from django import forms
from tentrack.models import Player
from tentrack.models import Week

class MatchResultForm(forms.Form):
    player_w1 = forms.ModelChoiceField(queryset=Player.objects.order_by('-points','name'), label='')
    player_w2 = forms.ModelChoiceField(queryset=Player.objects.order_by('-points','name'), label='')
    SCORE_CHOICES = ((0,'6:0'),(1,'6:1'),(2,'6:2'),(3,'6:3'),(4,'6:4'),(5,'6:5 TB'))
    score = forms.ChoiceField(choices=SCORE_CHOICES, label='')
    player_l1 = forms.ModelChoiceField(queryset=Player.objects.order_by('-points','name'), label='')
    player_l2 = forms.ModelChoiceField(queryset=Player.objects.order_by('-points','name'), label='')
    def clean(self):
        cleaned_data = super(MatchResultForm, self).clean()
        p1 = cleaned_data.get('player_w1')
        p2 = cleaned_data.get('player_w2')
        p3 = cleaned_data.get('player_l1')
        p4 = cleaned_data.get('player_l2')
        # check duplicate player
        if p1==p2 or p1==p3 or p1==p4 or p2==p3 or p2==p4 or p3==p4 :
            raise forms.ValidationError("Need 4 distinct players!")
        # check duplicate match
        week = Week.objects.get(open=True) # what if not one?
        matches = week.match_set.all()
        clist=[]
        for m in matches:
            tt = []
            pp = m.player_w.all().order_by('id') # pp[0].id <= pp[1].id
            tt.append(pp[1].id*(pp[1].id+1)/2+pp[0].id)
            pp = m.player_l.all().order_by('id')
            tt.append(pp[1].id*(pp[1].id+1)/2+pp[0].id)
            tt.sort() # tt[0] <= tt[1]
            c = tt[1]*(tt[1]+1)/2+tt[0]
            clist.append(c)
        tt = []
        dd = sorted([p1.id, p2.id]) # dd[0] <= dd[1]
        tt.append(dd[1]*(dd[1]+1)/2+dd[0])
        dd = sorted([p3.id, p4.id])
        tt.append(dd[1]*(dd[1]+1)/2+dd[0])
        tt.sort() # tt[0] <= tt[1]
        c = tt[1]*(tt[1]+1)/2+tt[0]
        if c in clist:
            raise forms.ValidationError("Duplicate match!")
        return cleaned_data
