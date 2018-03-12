from django.db import connection


def create_score_backup_trigger(**kwargs):
    print('...... Creating backup trigger for evaluation ......')
    trigger_sql = 'DROP TRIGGER IF EXISTS insert_new_scores;'
    cursor = connection.cursor()
    cursor.execute(trigger_sql)

    trigger_sql = 'CREATE TRIGGER insert_new_scores AFTER INSERT ON evaluation_score ' \
                  'FOR EACH ROW BEGIN ' \
                  'INSERT INTO evaluation_scoresbk (score_id, team_id, mu, sigma, result_id) ' \
                  'SELECT id, team_id, mu, sigma, result_id FROM evaluation_score WHERE id = NEW.id; ' \
                  'END;'
    cursor = connection.cursor()
    cursor.execute(trigger_sql)

    trigger_sql = 'DROP TRIGGER IF EXISTS update_new_scores;'
    cursor = connection.cursor()
    cursor.execute(trigger_sql)

    trigger_sql = 'CREATE TRIGGER update_new_scores AFTER UPDATE ON evaluation_score ' \
                  'FOR EACH ROW BEGIN ' \
                  'INSERT INTO evaluation_scoresbk (score_id, team_id, mu, sigma, result_id) ' \
                  'SELECT id, team_id, mu, sigma, result_id FROM evaluation_score WHERE id = NEW.id; ' \
                  'END;'
    cursor = connection.cursor()
    cursor.execute(trigger_sql)
    print('...... Trigger created ......')
