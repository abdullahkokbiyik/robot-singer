import os
from turkishnlp.detector import TurkishNLP as nlp
import random
from flask import Flask, render_template, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST', 'GET'])
def generate():

    os.system("rm -r static/generation/*")
    data = request.get_data()
    data = json.loads(data)
    file_name = data['file_name']
    lyric = data['lyric']
    transpose = data['transpose']
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
        lyrics.close()
    else:
        poem = lyric.lstrip("\n")
    # Write selected poem to file
    selected_poem = open("static/generation/lyrics.txt", "w")
    selected_poem.write(poem)
    selected_poem.close()

    # Read notes file. This file includes all possible notes (not exactly all btw). We will choose randomly between them
    notes = open("example/notes/notes.txt", "r")
    # Append notes to a list
    notes_list = notes.read().rstrip("\n").split(" ")
    notes.close()

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
    selected_poem = open("static/generation/lyrics.txt", "r")
    line = selected_poem.readline()

    # Init model
    obj = nlp()
    # obj.download()
    obj.create_word_set()

    while line:
        line_stripped = line.rstrip("\n")
        syllabicated = obj.syllabicate_sentence(line_stripped)
        line_len = sum(len(x) for x in syllabicated)
        for i in range(line_len):
            if i != line_len:
                outfile.write(notes_list[random.randrange(0, len(notes_list))] + " ")
            else:
                outfile.write(notes_list[random.randrange(0, len(notes_list))])
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
    app.run(host='0.0.0.0', port=5000)
