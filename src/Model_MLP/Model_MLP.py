"""
* Created by PyCharm.
* User: tuhoangbk
* Date: 05/10/2018
* Time: 23:30
*Have a nice day　:*)　:*)
"""
from keras.models import Sequential, Model
from keras.layers import Embedding, LSTM, Dropout,TimeDistributed, Dense, Activation, GRU, Input
from keras.utils import plot_model

def model_rnn_lstm(vocab_dim, hidden_size, input_dim, output_dim, use_dropout=True):
    model = Sequential()
    model.add(Embedding(vocab_dim, hidden_size, input_length=input_dim))
    model.add(LSTM(hidden_size, return_sequences=True))
    model.add(LSTM(hidden_size, return_sequences=True))

    if use_dropout:
        model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(vocab_dim)))
    model.add(Activation('softmax'))
    plot_model(model, to_file='new_model.png')

    return model

def model_rnn_gru(vocab_dim, hidden_size, input_dim, output_dim, use_dropout=True):
    # input_dim = 0  # Size of the vocabulary, i.e. maximum integer index + 1.
    # hidden_size = 0  # Dimension of the dense embedding.
    # num_steps = 20  # Length of input sequences
    # output_dim = 0
    # use_dropout = True
    model = Sequential()
    model.add(Embedding(vocab_dim, hidden_size, input_length=input_dim))
    model.add(GRU(hidden_size, return_sequences=True))
    model.add(GRU(hidden_size, return_sequences=True))

    if use_dropout:
        model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(vocab_dim)))
    model.add(Activation('softmax'))
    plot_model(model, to_file='new_model.png')

    return model

def build_model(vocab_size_china, vocab_size_vietnam, hidden_size):
    encoder_inputs = Input(shape=(None,))
    # Chinese words embedding
    en_x = Embedding(vocab_size_china, hidden_size)(encoder_inputs)
    # Encoder lstm
    encoder = LSTM(50, return_state=True)
    encoder_outputs, state_h, state_c = encoder(en_x)
    # We discard `encoder_outputs` and only keep the states.
    encoder_states = [state_h, state_c]
    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = Input(shape=(None,))
    # french word embeddings
    dex = Embedding(vocab_size_vietnam, hidden_size)
    final_dex = dex(decoder_inputs)
    # decoder lstm
    decoder_lstm = LSTM(50, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(final_dex,
                                         initial_state=encoder_states)
    decoder_dense = Dense(vocab_size_vietnam, activation='softmax')
    decoder_outputs = decoder_dense(decoder_outputs)
    # While training, model takes eng and french words and outputs #translated french word
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    # rmsprop is preferred for nlp tasks
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

    model.summary()
    plot_model(model, to_file='new_model.png')
    return model


