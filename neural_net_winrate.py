import numpy as np
import tensorflow as tf
from collections import defaultdict
from math import sqrt
from random import sample

from base_model import *
from input_builder import InputBuilder
from loader import map_decks_by_name
from tester import test_model, generate_submission


class NeuralNet(BaseModel):
    _layers = [1]
    _input_builder = None
    learning_rate = 0.2
    dropout = 0.5
    mb_size = 64
    nb_epochs = 40000
    # Each |lr_decay_time| epochs the learning rate is divided by two
    lr_decay_time = 5000

    def _create_model(self) -> None:
        self.x = tf.placeholder(tf.float32, [None, 361])
        self.y = tf.placeholder(tf.float32, [None, 1])

        signal = self.x
        for neurons_count in self._layers[:-1]:
            # Initialize layer with random values such that std. dev = sqrt(2 / N).
            # Not that it matters in such a small neural net.
            w_init = tf.initializers.random_normal(stddev=sqrt(2 / neurons_count))
            cur_dense_layer = tf.layers.dense(inputs=signal,
                                              units=neurons_count,
                                              activation=tf.nn.sigmoid,
                                              kernel_initializer=w_init)
            signal = cur_dense_layer
            # Apply dropout
            signal = tf.layers.dropout(inputs=signal, rate=self.dropout)

        last_dense_layer = tf.layers.dense(inputs=signal,
                                           activation=tf.nn.sigmoid,
                                           units=1)

        signal = last_dense_layer
        self.preds = signal
        self.loss = tf.losses.mean_squared_error(self.y, signal)

        self.op_train = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(self.loss)

    def __init__(self):
        self._input_builder = InputBuilder()
        self._create_model()

    def _set_config(self, config: ModelConfig) -> None:
        if 'layers' in config:
            self._layers = config['layers']
        if 'lr' in config:
            self.learning_rate = config['lr']
        if 'mb_size' in config:
            self.mb_size = config['mb_size']
        if 'nb_epochs' in config:
            self.nb_epochs = config['nb_epochs']
        if 'lr_decay_time' in config:
            self.lr_decay_time = config['lr_decay_time']

    def _compute_win_rates(self, training_games: List[Game], training_decks: List[Deck]) -> None:
        training_decks = map_decks_by_name(training_decks)
        # Copied from KNN
        wins = defaultdict(int)
        total_games = defaultdict(int)
        winrates = defaultdict(float)
        for game in training_games:
            player0, player1 = (game['bot0'], game['deck0']), (game['bot1'], (game['deck1']))
            total_games[player0] += 1
            total_games[player1] += 1
            if game['winner'] == 0:
                wins[player0] += 1
            else:
                wins[player1] += 1
        self.players = []
        self.winrates = []
        for k in wins:
            winrates[k] = wins[k] / total_games[k]
            deck_name = k[1]
            deck = training_decks[deck_name]
            bot_name = k[0]
            self.players.append(self._input_builder.build_single_player_input(deck, bot_name))
            self.winrates.append(winrates[k])
        self.players = np.array(self.players)
        self.winrates = np.array(self.winrates).reshape((len(self.winrates), 1))


    def learn(self, training_games: List[Game], training_decks: List[Deck], config: ModelConfig = None) -> None:
        self._set_config(config)

        self._compute_win_rates(training_games, training_decks)
        print(self.players.shape)
        print(self.winrates.shape)

        self.sess = tf.Session()
        # Initialize variables (kernels for dense layers).
        tf.global_variables_initializer().run(session=self.sess)

        for epoch_no in range(self.nb_epochs):
            batch = sample(range(len(self.players)), k=self.mb_size)
            batch_x = self.players[batch]
            batch_y = self.winrates[batch]
            loss, _, preds = self.sess.run([self.loss, self.op_train, self.preds], feed_dict={
                self.x: batch_x,
                self.y: batch_y
            })
            if epoch_no % 100 == 0:
                print("Epoch {0}: loss: {1}".format(epoch_no, loss))
            if epoch_no > 0 and epoch_no % self.lr_decay_time == 0:
                # Learning rate decay
                self.learning_rate /= 2
        pass

    # returns the predicted winrate of (bot, deck) vs all (bot, deck) pairs in the training set
    def predict(self, bot: str, deck: Deck) -> float:
        deck_bot_input = self._input_builder.build_single_player_input(deck, bot).reshape((1, 361))
        winrate = self.sess.run([self.preds], feed_dict={self.x: deck_bot_input})[0][0][0]
        return winrate * 100


if __name__ == '__main__':
    #test_model(NeuralNet)
    generate_submission(NeuralNet, {})
