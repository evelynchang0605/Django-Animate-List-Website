from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Animate, Recommend
from django.conf import settings
from django.urls import reverse
from django.views import generic
import csv, os
import matplotlib.pyplot as plt
import pandas as pd

# Create your views here.

class IndexView(generic.ListView):
    template_name = "my_animation_list_app/index.html"
    context_object_name = "latest_animate_list"

    def get_queryset(self):
        return Animate.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Animate
    template_name = "my_animation_list_app/detail.html"

    def get_queryset(self):
        return Animate.objects.all()

class ResultsView(generic.DetailView):
    model = Animate
    template_name = "my_animation_list_app/results.html"

def vote(request, animate_id):
    animate = get_object_or_404(Animate, pk=animate_id)
    try:
        selected_choice = animate.recommend_set.get(pk=request.POST["recommend"])
    except (KeyError, Recommend.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "my_animation_list_app/detail.html",
            {
                "animate_title": animate,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("my_animation_list_app:results", args=(animate.id,)))
#Export my vote result to csv
def export_mylist_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="MyAnimateList.csv"'
    writer = csv.writer(response)
    #Write the CSV header
    writer.writerow(['title_text','votes'])
    '''
    animates = Animate.objects.all()
    for animate in animates:
        writer.writerow([
            animate.title_text,
            animate.zone_text,
            animate.pub_date,
            animate.animate_description,
        ])
    '''
    recommends = Recommend.objects.all()
    for recommend in recommends:
        writer.writerow([
            #recommend.title_id,
            recommend.title,
            #recommend.recommend_text,
            recommend.votes,
        ])
    return response
#change my vote result from csv to img
def change_mylist_csv_to_img(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', 'MyAnimateList.csv')
    df = pd.read_csv(csv_file_path)
    plt.bar(df['title_text'], df['votes'])
    plt.xlabel(df['title_text'])
    plt.ylabel(df['votes'])
    plt.title('MyAnimate Vote Result')
    plt.savefig("VoteResult.png")

    return render(request, 'results.html')
