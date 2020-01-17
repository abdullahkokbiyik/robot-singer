#-- coding: utf-8 --
import os
import glob
from turkishnlp.detector import TurkishNLP as nlp
import random
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_executor import Executor
from time import sleep
from GenerateNotes.generate import generate_notes_string
import json

app = Flask(__name__)
CORS(app)
executor = Executor(app)
FILE_SIZE = 100
used_note_files = list()
BEG_SEQ = "<S>"
END_SEQ = "</S>"
UNK = "_UNK_"
NEW_LINE = "_NEWLINE_"


@app.route('/')
def index():
    return render_template('index.html')


def generate_notes(file_name):
    generate_notes_string(file_name, "example/notes/")
    print("New note file generated!")


def generate_lyrics(file_name):
    os.system("cd GenerateLyrics && python3 train.py " + file_name)


def highest_freq(array):
    print("Mostly used note is selecting...")
    freq_dict = dict()
    for file in array:
        if file not in freq_dict.keys():
            freq_dict[file] = 1
        else:
            freq_dict[file] += 1
    print("Frequency dict constructed. Continue...")
    mostly_used = array[0]
    for key in freq_dict.keys():
        if freq_dict[key] > freq_dict[mostly_used]:
            mostly_used = key
    print("Mostly used note file is {}!".format(mostly_used))
    return mostly_used


@app.route('/generate', methods=['POST', 'GET'])
def generate():

    file_size = len([name for name in os.listdir('static/generation')])
    if file_size >= FILE_SIZE:
        files = [f for f in glob.glob("static/generation/*", recursive=True)]
        files = sorted(files, key=os.path.getctime)
        files = files[:5]
        for file in files:
            os.system("rm -rf static/generation/" + file)

    # Init model
    obj = nlp()
    # If code runs first time, uncomment two codes below. Running one time is enough.
#    obj.download()
#    obj.create_word_set()

    data = request.get_data()
    data = json.loads(data.decode('utf-8'))
    file_name = data['file_name']
    lyric = data['lyric']
    transpose = data['transpose']
    poem = ""
    if lyric == "None":
        # Generate lyrics from model.
        generate_lyrics(file_name)
        lyrics = open("example/lyrics/" + file_name + "_lyrics.txt", "r")
        poem = lyrics.read().lstrip("\n")
        lyrics.close()
        os.system("rm -rf example/lyrics/" + file_name + "_lyrics.txt")
    else:
        poem = lyric.lstrip("\n")
        lines = poem.split('\n')
        syl = 0
        for line in lines:
            line_strip = line.rstrip('\n')
            line_strip = obj.syllabicate_sentence(line_strip)
            syl += sum(len(x) for x in line_strip)
        # Syllabicate restriction.
        if syl > 129:
            return json.dumps({'status_code': '400'})
    # Write selected poem to file
    selected_poem = open("static/generation/lyrics_" + file_name + ".txt", "w")
    selected_poem.write(poem)
    selected_poem.close()

    # Read notes file. This file includes all possible notes (not exactly all btw). We will choose randomly between them
    random_ = [f for f in glob.glob("example/notes/*.txt", recursive=True)]
    random_ = sorted(random_, key=os.path.getctime)
    random_note = random.choice(random_)
    used_note_files.append(random_note)
    notes = open(random_note, "r")
    # Append notes to a list
    notes_list = notes.read().split(" ")
    notes.close()
    # If too many notes are used, remove mostly used and generate new one at different thread. 
    if len(used_note_files) > FILE_SIZE/2:
        notewbd = highest_freq(used_note_files)
        os.system("rm -rf example/notes/" + notewbd)
        used_note_files.clear()
        executor.submit(generate_notes, file_name)

    # Conf file
    conf = open("static/generation/"+file_name+".conf", "w")
    conf.write("$ESPEAK_VOICE = \"tr\";\n"
               "$ESPEAK_TRANSPOSE = " + transpose + ";\n"
               "do '../ecantorix/examples/extravoices/melt.inc;'\n")
    conf.close()

    # Open output file. This file is .abc file
    outfile = open("static/generation/"+file_name+".abc", "w")
    outfile.write("X:0\n"
                  "M:4/4\n"
                  "L:1/6\n"
                  "Q:160\n"
                  "K:C\n"
                  "V:1\n")

    # Open file which included our selected poem
    selected_poem = open("static/generation/lyrics_" + file_name + ".txt", "r")
    line = selected_poem.readline()
    note_index = 0
    # Create .abc file
    while line:
        line_stripped = line.rstrip("\n")
        syllabicated = obj.syllabicate_sentence(line_stripped)
        line_len = sum(len(x) for x in syllabicated)
        for i in range(line_len):
            if i != line_len:
                outfile.write(notes_list[note_index] + " ")
                note_index += 1
            else:
                outfile.write(notes_list[note_index])
                note_index += 1
        outfile.write("|\nw:")
        for list_word in syllabicated:
            for word_index in range(len(list_word)):
                if len(list_word) == 1:
                    outfile.write(list_word[0] + " ")
                else:
                    outfile.write(list_word[word_index])
                    if word_index != len(list_word) - 1:
                        outfile.write("-")
                    else:
                        outfile.write(" ")
        outfile.write("\n")
        line = selected_poem.readline()

    selected_poem.close()
    outfile.close()
    # Terminal command for generation.
    os.system("cd ecantorix && make ../static/generation/"+file_name+".wav")
    response = {"status_code": "200", "lyrics": poem}
    return json.dumps(response)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000, threaded=True)


