import subprocess

class BackendLogic():
    def select2teams():
        randomteamname = [1,2]
        return randomteamname

    def executemodel(querystring, teamname, programname):
        BASE_PATH = "C:/Users/gautkar/Documents/Office/2018/08 Data Science Community/WebServiceFramework/capgemini-gdsc/mysite/DSCIV/"
        DSCIV_MODEL_NAME = "GDSC_recommendation_model.py"
        PROGRAM_NAME_PYTHON = "python"
        PROGRAM_NAME_R = "R"
        if(programname == "P"):
            restult = subprocess.Popen([PROGRAM_NAME_PYTHON, BASE_PATH + DSCIV_MODEL_NAME, querystring], stdout = subprocess.PIPE).communicate
        else:
            restult = subprocess.Popen([PROGRAM_NAME_R, BASE_PATH + DSCIV_MODEL_NAME, querystring], stdout = subprocess.PIPE).communicate
        return restult
