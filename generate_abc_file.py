from turkishnlp.detector import TurkishNLP as nlp


def generate_abc_file(file_name):
    lyrics = open("lyrics.txt", "r")
    notes = open("notes.txt", "r")
    conf = open("example/"+file_name+".conf", "w")
    outfile = open("example/"+file_name+".abc", "w")
    outfile.write("X:0\nM:4/4\nL:1/4\nQ:120\nK:C\nV:1\n")
    line = lyrics.readline()
    obj = nlp()
    #obj.download()
    obj.create_word_set()
    while line:
        note_line = notes.readline()
        outfile.write(note_line.rstrip("\n") + "|" + "\nw:")
        line_stripped = line.rstrip("\n")
        syllabicated = obj.syllabicate_sentence(line_stripped)
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
        line = lyrics.readline()

    conf.write("$ESPEAK_VOICE = \"tr\";\n"
               "$ESPEAK_TRANSPOSE = -15;\n"
               "do '../ecantorix/examples/extravoices/melt.inc;'\n")
    conf.close()
    notes.close()
    outfile.close()
    lyrics.close()
