# Create your views here.

from tentrack.models import Player, Week, Match
from tentrack.forms import MatchResultForm
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Avg
from operator import attrgetter

def home(request):
    this_week = Week.objects.get(open=True) # what if not one?
    return render_to_response('tentrack/home.html', {'this_week':this_week})

def mpost(request):
    this_week = Week.objects.get(open=True) # what if not one?
    if request.method == 'POST':
        form = MatchResultForm(request.POST)
        if form.is_valid():
            pw1 = form.cleaned_data['player_w1']
            pw2 = form.cleaned_data['player_w2']
            pl1 = form.cleaned_data['player_l1']
            pl2 = form.cleaned_data['player_l2']
            s = form.cleaned_data['score']
            w = Week.objects.get(open=True) # what if not one?
            m = Match(date=timezone.now(), week=w, score=s, pgain=0)
            m.save()
            m.player_w.add(pw1)
            m.player_w.add(pw2)
            m.player_l.add(pl1)
            m.player_l.add(pl2)
            m.calculate_pgain()
            m.save()
            return HttpResponseRedirect(reverse('tentrack_weekly',args=(w.id,)))
    else:
        form = MatchResultForm()
    return render_to_response('tentrack/mpost.html', {'form':form, 'this_week':this_week}, context_instance=RequestContext(request))

def mentors(request):
    mtlist=[[39, 38, 37, 72, 71],[40, 46, 70, 69],[41, 48, 50, 49, 65],[42, 52, 60, 55, 63],
               [44, 36, 35, 64],[56, 45, 59, 68],[58, 47, 57, 53, 73],[62, 74, 61, 66, 54]]
    mentors_list=[]
    for mt in mtlist:
        mentor=Player.objects.get(id=mt[0])
        mentees=Player.objects.filter(id__in=mt[1:])
        mstat=mentees.aggregate(mp=Avg('points'))
        mentors_list.append({'mentorname':mentor.name, 'mentees':mentees, 'mpoints':int(mstat['mp'])})
    return render_to_response('tentrack/mentors.html', {'mentors_list':mentors_list})

def pmatrix(request):
    #players=Player.objects.order_by('-points')    
    players=list(Player.objects.all())
    for p in players:
        p.mcount = p.match_w.count() + p.match_l.count()
    players.sort(key=attrgetter('mcount'), reverse=True)
    itab={}
    ind=0
    for p in players:
        itab[p.name]=ind
        ind+=1
    L=len(players)
    pmat=[[0 for j in range(L)] for i in range(L)]
    matches=Match.objects.all()
    for m in matches:
        wp = m.player_w.all()
        lp = m.player_l.all()
        w0=itab[wp[0].name]
        w1=itab[wp[1].name]
        l0=itab[lp[0].name]
        l1=itab[lp[1].name]
        pmat[w0][w1]+=1
        pmat[w1][w0]+=1
        pmat[l0][l1]+=1
        pmat[l1][l0]+=1
        pmat[w0][l0]+=1
        pmat[l0][w0]+=1
        pmat[w1][l1]+=1
        pmat[l1][w1]+=1
        pmat[w0][l1]+=1
        pmat[l1][w0]+=1
        pmat[w1][l0]+=1
        pmat[l0][w1]+=1
    pvec=[]
    for r in players:
	pvec.append(r.name)
    pmtable=[[0 for j in range(1+L)] for i in range(1+L)]
    pmtable[0][0]=""
    pmtable[0][1:1+L]=pvec
    for i in range(L):
        pmtable[i+1]=[pvec[i]]+pmat[i]
    return render_to_response('tentrack/pmatrix.html', {'pmtable':pmtable})

# def pindex(request):
#    player_list = Player.objects.all()
#    return render_to_response('tentrack/pindex.html', {'player_list': player_list})

# def pdetail(request, player_id):
#     p = get_object_or_404(Player, pk=player_id)
#     return render_to_response('tentrack/pdetail.html', {'player':p})

# def windex(request):
#    week_list = Week.objects.all()
#    return render_to_response('tentrack/windex.html', {'week_list': week_list})

# def weekly(request, week_id):
#    w = get_object_or_404(Week, pk=week_id)
#    return render_to_response('tentrack/weekly.html', {'week': w})

