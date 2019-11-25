import os

for file in os.listdir("./example"):
    if file.endswith(".abc"):
        print(file[:-4].capitalize())
option = input("Type the name of abc file listed above: \n")

os.system("cd ecantorix && make ../example/" + option.lower() + ".wav")
