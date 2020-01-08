#-- coding: utf-8 --
import os
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


@app.route('/')
def index():
    return render_template('index.html')


def generate_notes(file_name):
    generate_notes_string(file_name, "example/notes/")


@app.route('/generate', methods=['POST', 'GET'])
def generate():
    file_size = len([name for name in os.listdir('static/generation')])
    if file_size >= FILE_SIZE:
        files = sorted(os.listdir('static/generation'), key=os.path.getctime)[:5]
        for file in files:
            os.system("rm -rf static/generation/" + file)

    # Init model
    obj = nlp()
#    obj.download()
#    obj.create_word_set()

    data = request.get_data()
    data = json.loads(data.decode('utf-8'))
    file_name = data['file_name']
    lyric = data['lyric']
    transpose = data['transpose']
    executor.submit(generate_notes, file_name)
    poem = ""
    if lyric == "None":
        # Random number for selecting a category for our poem
        input_name = random.randrange(1, 4)
        category_file_name = "example/lyrics/category_" + str(input_name) + ".txt"
        # Open relevant category file
        lyrics = open(category_file_name, "r")

        # Pull all poems inside of category file
        poems = lyrics.read().split("<s>")
        # Select random poem
        poem = poems[random.randrange(0, len(poems))].lstrip("\n")
        lines = poem.split('\n')
        syl = 0
        for line in lines:
            line_strip = line.rstrip('\n')
            line_strip = obj.syllabicate_sentence(line_strip)
            syl += sum(len(x) for x in line_strip)
        while syl > 500:
            poem = poems[random.randrange(0, len(poems))].lstrip('\n')
            lines = poem.split('\n')
            syl = 0
            for line in lines:
                line_strip = line.rstrip('\n')
                line_strip = obj.syllabicate_sentence(line_strip)
                syl += sum(len(x) for x in line_strip)
        lyrics.close()
    else:
        poem = lyric.lstrip("\n")
        lines = poem.split('\n')
        syl = 0
        for line in lines:
            line_strip = line.rstrip('\n')
            line_strip = obj.syllabicate_sentence(line_strip)
            syl += sum(len(x) for x in line_strip)
        if syl > 500:
            return json.dumps({'status_code': '400'})
    # Write selected poem to file
    selected_poem = open("static/generation/lyrics_" + file_name + ".txt", "w")
    selected_poem.write(poem)
    selected_poem.close()

    # Read notes file. This file includes all possible notes (not exactly all btw). We will choose randomly between them
    random_note = random.choice(os.listdir("example/notes/"))
    notes = open("example/notes/" + random_note, "r")
    # Append notes to a list
    notes_list = notes.read().rstrip("\n").split(" ")
    notes.close()
    os.system("rm -rf example/notes/" + random_note)

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
                  "L:1/4\n"
                  "Q:120\n"
                  "K:C\n"
                  "V:1\n")

    # Open file which included our selected poem
    selected_poem = open("static/generation/lyrics_" + file_name + ".txt", "r")
    line = selected_poem.readline()
    note_index = 0
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
    os.system("cd ecantorix && make ../static/generation/"+file_name+".wav")
    response = {"status_code": "200", "lyrics": poem}
    return json.dumps(response)


if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host='localhost', port=8000)
    app.run(host="0.0.0.0", port=8000, threaded=True)


