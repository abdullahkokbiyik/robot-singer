import os
from generate_abc_file import generate_abc_file

file_name = input("Give your music file a name: \n")
generate_abc_file(file_name.lower())

os.system("cd ecantorix && make ../example/" + file_name.lower() + ".wav")
