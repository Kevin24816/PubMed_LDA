import pickle
import os


home = os.path.dirname(__file__) +"/"
progress_file = open(home+"status/PROGRESS REPORT", 'w')
progress_file.write("")
progress_file.close()

d = home + "/temp/"
if not os.path.exists(d):
    os.makedirs(d)

s = home + "/status/"
if not os.path.exists(s):
    os.makedirs(s)

def log_writeline(line):
    file = open(s + "Log", 'a')
    file.write("\n")
    file.write(line)
    file.close()

def log_overwrite(write_lines):
    file = open(s + "Log", 'w')
    for line in write_lines:
        file.write(line + "\n")
    file.close()

def clear_log():
    file = open(s + "Log", 'w')
    file.close()

def sort_logging_lines():
    lines = open(s + "Log").read().split("\n")
    line_Dict = {}
    score_to_settings = {}
    for line in lines:
        if line != "":
            perplexity = float(line.split("\t")[0].replace("log_p = ", "").replace(" ||", ""))
            settings = line.split("(")[-1].replace(")", "")
            line_Dict[perplexity] = line
            score_to_settings[perplexity] = settings
    p = line_Dict.keys()
    p.sort()
    write_lines = []
    for i in range(len(p)-1, -1, -1):
        item = p[i]
        write_lines.append(line_Dict[item])
    log_overwrite(write_lines)

    top_50_scores = p[0:50] #settings not in top 50
    top_50_score_to_settings = {}
    for score in top_50_scores:
        top_50_score_to_settings[score] = score_to_settings[score]
    pickle_file(top_50_score_to_settings, "top_50")

def wprint(string):
    """prints string and writes to file"""
    print string
    f = open(s + "PROGRESS REPORT", 'a')
    f.write(string + "\n")
    f.close()

def update_progress(report_str):
    progress_file = open(s + "PROGRESS REPORT", 'a')
    progress_file.write(report_str)
    progress_file.close()

def pickle_file(object, name, directory = d):
    if not os.path.exists(d):
        os.makedirs(directory)
    output = open(directory + name, 'wb')
    pickle.dump(object, output)
    output.close()

def unpickle(name, directory = d):
    if not os.path.exists(directory):
        print "FILE DOES NOT EXIST"
    with open(directory + name, 'rb') as f:
        return pickle.load(f)
