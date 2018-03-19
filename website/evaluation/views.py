"""
Django views to handle requests from templates and transfer them to backendlogic.py
"""
import os
import mimetypes
import glob
from time import time
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DataSciencesearch, Winnerselection
from .backendlogic import execute_model, select_two_teams, add_new_result, models_url
from django.conf import settings
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from django.contrib import messages


# Create your views here.

def get_program_name(selected_team_name):
    name = glob.glob(models_url + "/" + selected_team_name + "/" + '/GDSC_recommendation_model.*')
    program_name = name[0].split('GDSC_recommendation_model')[1]
    return program_name


def search(request):
    if request.POST:
        DataSciencesearch(request.POST)

        query = request.POST['businessquery']

        before_time = time()
        team_name = select_two_teams()
        after_time = time()
        run_time = round(after_time - before_time, 2)
        print('Teams selected in ' + str(run_time) + ' seconds.')

        # query execution of team 1
        program_name = get_program_name(selected_team_name=team_name[0])
        result_output1, run_time1, result_plain1 = execute_model(query, team_name[0], program_name)

        # query execution of team 2
        program_name = get_program_name(selected_team_name=team_name[1])
        result_output2, run_time2, result_plain2 = execute_model(query, team_name[1], program_name)

        context = {'result1': result_output1, 'team1': team_name[0], 'run_time1': run_time1,
                   'result_plain1': result_plain1,
                   'result2': result_output2, 'team2': team_name[1], 'run_time2': run_time2,
                   'result_plain2': result_plain2,
                   'search_query': query}
        return render(request, 'evaluation/result.html', context)
    else:
        return render(request, 'evaluation/search.html')


def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_URL, file_name)
    file_wrapper = FileWrapper(open(file_path, 'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response


def result(request):
    if request.POST:
        validation_form = Winnerselection(request.POST)
        form_post_data = [validation_form.data, ][0]

        winner_team = form_post_data['Winner']
        team_name_1 = form_post_data['team_name_1']
        team_name_2 = form_post_data['team_name_2']
        search_query = form_post_data['search_query']

        team_1_output = form_post_data['team_1_output']
        team_2_output = form_post_data['team_2_output']

        context = {'result': form_post_data, 'message': 'Winner record saved successfully!'}

        add_new_result(winner_team=winner_team, query=search_query, team_a=team_name_1, team_b=team_name_2,
                       current_logged_in_user_id=request.user.id, team_a_result=team_1_output,
                       team_b_result=team_2_output)

        messages.success(request, 'Winner record saved successfully!')
        return render(request, 'evaluation/search.html', context)
    else:
        return render(request, 'evaluation/result.html')
