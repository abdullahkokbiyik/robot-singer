import pretty_midi
import numpy as np
import glob
import pickle
import random

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.layers import BatchNormalization as BatchNorm
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

SEQUENCE_LENGTH = 100
GENERATED_NOTE_COUNT = 500

def generate_notes_string(CREATED_FILE_NAME, OUTPUT_FOLDER):

  ## Load the note arrays from disk to train the model. ##
  with open('GenerateNotes/data/pitch_of_notes', 'rb') as filepath:
      pitch_of_notes = pickle.load(filepath)
      
  ## Get all uniques. ##
  unique_pitch = sorted(set(pitch for pitch in pitch_of_notes))
  
  ## Get all unique counts. ##
  vocab_size_pitch = len(unique_pitch)

  ## Prediction of pitch values. ##
  network_input_pitch, normalized_input_pitch = prepare_network_data(pitch_of_notes, unique_pitch, vocab_size_pitch)
  model_pitch = create_network(normalized_input_pitch, vocab_size_pitch, "pitch")
  predicted_pitch = generate_notes(model_pitch, network_input_pitch, unique_pitch, vocab_size_pitch)
  
  create_midi_to_str(predicted_pitch, CREATED_FILE_NAME, OUTPUT_FOLDER)




def prepare_network_data(feature_to_string, unique_int, len_unique_int, sequence_length=SEQUENCE_LENGTH):

  ## Dictionary of uniques. ##
  unique_to_int = dict((feature, number) for number, feature in enumerate(unique_int))

  network_input = list()
  
  for i in range(0, len(feature_to_string) - sequence_length, 1):
    sequence_input = feature_to_string[i:i + sequence_length]
    network_input.append(list(unique_to_int[feature] for feature in sequence_input))

  pattern_count = len(network_input)

  ## Reshape the input into a format compatible with LSTM layers. ##
  ## Normalized input is a column vector of notes' sequences. ##
  normalized_input = np.reshape(network_input, (pattern_count, sequence_length, 1))
  ## Normalized input is normalized now. ##
  normalized_input = normalized_input / float(len_unique_int)

  return network_input, normalized_input



def create_network(network_input, n_vocab, feature):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    
    ## Load the weights. ##
    model.load_weights("GenerateNotes/" + feature + '_weights.hdf5')
    return model



def generate_notes(model, network_input, unique_int, len_unique_int, generating_feature_count=GENERATED_NOTE_COUNT):
  ## Pick a random input to start prediction. ##
  start = np.random.randint(0, len(network_input)-1)

  ## Map integers with uniques. ##
  int_to_unique = dict((number, feature) for number, feature in enumerate(unique_int))

  ## Select first input of network. ##
  initial_input = network_input[start]
  predicted_features = list()

  ## Generate notes. ##
  for note_index in range(generating_feature_count):
    prediction_input = np.reshape(initial_input, (1, len(initial_input), 1))
    prediction_input = prediction_input / float(len_unique_int)

    prediction = model.predict(prediction_input, verbose=0)

    ## Select one-hot vector's index. ##
    index = np.argmax(prediction)
    predicted_feature = int_to_unique[index]
    predicted_features.append(predicted_feature)

    ## Shift the initial input. ##
    initial_input.append(index)
    initial_input = initial_input[1:len(initial_input)]

  return predicted_features



def create_midi_to_str(predicted_pitch, CREATED_FILE_NAME, OUTPUT_FOLDER):
  new_name = CREATED_FILE_NAME

  with open(OUTPUT_FOLDER + new_name + ".txt", "w+") as new_file:
    for i in range(len(predicted_pitch)):
      for pitch in predicted_pitch[i].split("-"):
        note = pretty_midi.note_number_to_name(int(pitch))
        new_file.write(note + " ")
