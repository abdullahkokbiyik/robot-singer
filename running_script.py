import os
from generate_abc_file import generate_abc_file

file_name = input("Give your abc file a name: \n")
generate_abc_file(file_name)
for file in os.listdir("./example"):
    if file.endswith(".abc"):
        print(file[:-4].capitalize())
option = input("Type the name of abc file listed above: \n")


os.system("cd ecantorix && make ../example/" + option.lower() + ".wav")
