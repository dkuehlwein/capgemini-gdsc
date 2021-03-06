"""
Handling requests from views.py and connects with database.
"""

__author__ = "Gondal, Saad Abdullah"

import subprocess
import random
import os
from time import time
from .models import Result, Score, Summaries, TeamsOutput
from django.utils import timezone
from django.conf import settings
from trueskill import Rating, rate_1vs1

models_url = os.path.join(settings.BASE_DIR, '..', 'models')


def select_two_teams():
    """ Selects two teams at random.

    Returns:
         :returns random_team_name: String name
    """
    teams = os.listdir(models_url)
    team_scores = [get_or_create_score_by_team_name(team) for team in teams]

    # Sort teams by how often they were used
    team_scores.sort(key=lambda x: x.nr_of_queries)
    team_a = team_scores[0]  # Team a is the team with the fewest number of queries

    # Determine potential opponents
    mu_min = team_a.mu - 3 * team_a.sigma
    mu_max = team_a.mu + 3 * team_a.sigma
    potential_opponents = [team for team in team_scores[1:] if ((team.mu > mu_min) and (team.mu < mu_max))]
    #print('Found %s opponents' % len(potential_opponents))
    if len(potential_opponents) == 0:
        potential_opponents = team_scores[1:]

    # Pick opponent
    team_b = random.sample(potential_opponents, 1)[0]

    #print(team_a.team_id, team_b.team_id)
    #print(team_a.nr_of_queries, team_b.nr_of_queries)
    return team_a.team_id, team_b.team_id


def execute_model(query_string, team_name, program_name):
    """ Executes models according to the given team name.
    Args:
        :param query_string: search string
        :param team_name: team name. Used to find the model against this name.
        :param program_name: Either P (python) or R.

    Returns:
        :returns result_output: Dictionary of file names and corresponding summaries.
        :returns run_time: Run time of the given model
        :returns result_output_plain: A comma seperated string of file names only.
    """
    base_path = models_url + "/" + team_name + "/"
    print(team_name + ", " + program_name)

    python_program = "python"
    r_program = "Rscript"
    result_output = ''

    before_time = time()
    if program_name == ".py":
        script_name = "GDSC_recommendation_model.py"
        result_output = subprocess.Popen(
            [python_program, base_path + script_name, query_string],  # , settings.MEDIA_URL],
            stdout=subprocess.PIPE, cwd=base_path).communicate()
    elif program_name == ".R":
        script_name = "GDSC_recommendation_model.R"
        result_output = subprocess.Popen(
            [r_program, base_path + script_name, query_string],  # , settings.MEDIA_URL],
            stdout=subprocess.PIPE, cwd=base_path).communicate()
    else:
        print("Problem!")
    after_time = time()
    run_time = round(after_time - before_time, 2)

    result_output_plain = ''
    result_output = result_output[0].decode('UTF-8')
    result_output = result_output.splitlines()

    if not result_output == []:
        result_output, result_output_plain = get_summaries(result_output, result_output_plain)
    else:
        print('ERROR: Cannot get file names from model ' + str(team_name))
    return result_output, run_time, result_output_plain


def get_summaries(arr_ppt_file_names, result_output_plain):
    """ Get summaries of files in arr_ppt_file_names

    :param arr_ppt_file_names: List of file names generated by model
    :param result_output_plain: Populates this parameter against file names.
    :returns: summary_text, result_output_plain
    """
    summary_text = {}
    for file in arr_ppt_file_names:
        name = str(file).split('.')[0]
        try:
            summary_obj = Summaries.objects.get(ppt_file_names__contains=str('' + name + '.'))
            summary_text[file] = summary_obj.file_summary
            result_output_plain += file + ','
        except Summaries.DoesNotExist:
            print('Summary not found for :: ' + name)
            summary_text[file] = '---'
        except Exception as e:
            print(e)
            summary_text[file] = '---'
    return summary_text, result_output_plain


def add_new_result(winner_team, query, team_a, team_b, current_logged_in_user_id, team_a_result, team_b_result,
                   team_a_time, team_b_time):
    """ Adds new result and updates scores.

    Gets previous scores of teamA and team_b to update with new scores based on
    the argument winner_team.

    Args:
        :param winner_team: name of the winning team or 'Draw'
        :param query: search query offered
        :param team_a: name of first team
        :param team_b: name of second team
        :param current_logged_in_user_id:
        :param team_a_result: output generated by team A
        :param team_b_result: output generated by team B
    """
    if 'Draw' not in winner_team:
        winner_team = winner_team.split(':')[1]
        new_result = Result(search_query=query, model_A=team_a, model_B=team_b, result=winner_team,
                            game_date=timezone.now(), user_id=current_logged_in_user_id)
    else:
        new_result = Result(search_query=query, model_A=team_a, model_B=team_b, result=winner_team,
                            game_date=timezone.now(), user_id=current_logged_in_user_id)
    new_result.save()

    # Update scores
    team_a_score = Score.objects.get(team_id=team_a)
    team_b_score = Score.objects.get(team_id=team_b)
    update_scores(team_a_score, team_b_score, winner_team, new_result.id)

    # Store outputs
    team_output = TeamsOutput(result_id=new_result.id, model_a_output=team_a_result, model_b_output=team_b_result,
                              model_a_execution_time=team_a_time, model_b_execution_time=team_b_time)
    team_output.save()


def get_or_create_score_by_team_name(team_name):
    """ Returns scores or add them if they don't already exist.

    If DoesNotExist exception occurs, this function assumes that this team
    is playing for the first time and adds its name in the database.
    This new team is initialized with the default scores of TrueSkill Rating.

    Args:
        :param team_name: name of the team to get score.

    Returns:
        :returns score: object of model class Scores
    """
    try:
        score = Score.objects.get(team_id=team_name)
    except Score.DoesNotExist:  # initializes team with default scores for the first time
        trues_kill_rating = Rating()
        score = Score(team_id=team_name, mu=trues_kill_rating.mu, sigma=trues_kill_rating.sigma,
                      nr_of_queries=0, result_id=-1)
        score.save()
    return score


def update_scores(team_a_score, team_b_score, win_key, result_id):
    """ Updates scores according to TrueSkill Rating

    Args:
        :param team_a_score: object of model class Scores representing Team A score
        :param team_b_score: object of model class Scores representing Team B score
        :param win_key: name of the winning team or 'Draw'
        :param result_id: Foreign key of DSCIV_result table
    """
    rating_team_a = Rating(mu=team_a_score.mu, sigma=team_a_score.sigma)
    rating_team_b = Rating(mu=team_b_score.mu, sigma=team_b_score.sigma)

    if 'Draw' in win_key:
        new_rating_team_a, new_rating_team_b = rate_1vs1(rating1=rating_team_a, rating2=rating_team_b, drawn=True)
    elif team_a_score.team_id in win_key:
        new_rating_team_a, new_rating_team_b = rate_1vs1(rating1=rating_team_a, rating2=rating_team_b)
    elif team_b_score.team_id in win_key:
        new_rating_team_b, new_rating_team_a = rate_1vs1(rating1=rating_team_b, rating2=rating_team_a)
    else:
        new_rating_team_a = ''
        new_rating_team_b = ''
        print("Could not assign new ratings.")

    # Update Mu and Sigma ratings
    team_a_score.mu, team_a_score.sigma = new_rating_team_a.mu, new_rating_team_a.sigma
    team_b_score.mu, team_b_score.sigma = new_rating_team_b.mu, new_rating_team_b.sigma

    # Update results ids
    team_a_score.result_id = result_id
    team_b_score.result_id = result_id

    # Update nr of queries
    team_a_score.nr_of_queries += 1
    team_b_score.nr_of_queries += 1

    # Save results
    team_a_score.save()
    team_b_score.save()
