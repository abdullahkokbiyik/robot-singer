# robot-singer
Robot Singer created by Muhammed Furkan YAVUZ & Abdullah Kökbıyık\
Code needs requirements of eCantorix (https://github.com/ttm/ecantorix) for running\
You must install all requirements of eCantorix.\
Robot Singer is a Flask App. So you need to install Flask.
```
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
```
Requirements for backend is specified above.\
You must also install Keras and pretty-midi for note generation part.\
You must also install dynet for lyric generation part.\
Python version is 3.6
```
python3 running_script.py
```
Type above command to terminal to run program.\
You can find useful links at example/ornek siteler/kullanilan_siteler.txt

