from subprocess import call

option = input("Type the name of abc file listed below: \n"
               "entchen\n"
               "nacht-v\n"
               "sadi-moma\n"
               "sadi-moma-flite\n"
               "sadi-moma-pitchbend\n"
               "sadi-moma-qon\n"
               "sarastro\n")

call("abc2midi " + option + ".abc -o " + option + ".mid", shell=True)
call("perl ecantorix/ecantorix.pl -O mmp -o " + option + ".mmp " + option + ".mid", shell=True)
call("lmms -o " + option + ".wav --render " + option + ".mmp", shell=True)
call("find . -type f -regextype 'posix-egrep' -iregex '.*(_)[a-zA-Z0-9_]*\\.(wav)$' -delete", shell=True)
call("find . -type f -regextype 'posix-egrep' -iregex '.*[a-zA-Z0-9_]*\\.(pitch)$' -delete", shell=True)
call("find . -type f -regextype 'posix-egrep' -iregex '.*[a-zA-Z0-9_]*\\.(mmp)$' -delete", shell=True)
call("find . -type f -regextype 'posix-egrep' -iregex '.*[a-zA-Z0-9_]*\\.(mid)$' -delete", shell=True)
call("rm -r tmp", shell=True)
