import numpy as np
import tensorflow as tf
from collections import defaultdict
from math import sqrt
from random import sample

from base_model import *
from input_builder import InputBuilder
from tester import test_model, generate_submission


INPUT_SHAPE = 722 + 180

class NeuralNet(BaseModel):
    _layers = [1]
    _input_builder = None
    learning_rate = 0.1
    mb_size = 256
    nb_epochs = 10000
    dropout = 0.0
    # Each |lr_decay_time| epochs the learning rate is divided by two
    lr_decay_time = 5000

    def _create_model(self) -> None:
        self.x = tf.placeholder(tf.float32, [None, INPUT_SHAPE])
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
        self.loss = tf.losses.log_loss(self.y, signal)
        self.accuracy = tf.reduce_mean(
            tf.cast(tf.equal(tf.round(signal), tf.round(self.y)), tf.float32))

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

    def learn(self, training_games: List[Game], training_decks: List[Deck], config: ModelConfig = None) -> None:
        self._set_config(config)

        def extract_winner(game):
            if game['winner'] == 0:
                return [1]
                #return [0.5 + game['winner_hp']/60]
            else:
                return [0]
                #return [0.5 - game['winner_hp']/60]

        self.games = []
        self.winners = []
        for training_game in training_games:
            self.games.append(self._input_builder.build_game_input(training_game))
            self.winners.append(extract_winner(training_game))

            reversed_game = {
                'bot0': training_game['bot1'],
                'bot1': training_game['bot0'],
                'deck0': training_game['deck1'],
                'deck1': training_game['deck0'],
                'winner': 1-training_game['winner'],
                'winner_hp': training_game['winner_hp']
            }
            self.games.append(self._input_builder.build_game_input(reversed_game))
            self.winners.append(extract_winner(reversed_game))
        self.games = np.array(self.games)
        self.winners = np.array(self.winners)

        print(self.games.shape)
        print(self.winners.shape)

        # Copied from KNN
        self.training_results = defaultdict(lambda: defaultdict(lambda: (0, 0)))
        self.training_games = training_games
        self.training_decks = training_decks
        for game in self.training_games:
            player0, player1 = (game['bot0'], game['deck0']), (game['bot1'], (game['deck1']))
            wins = self.training_results[player0][player1]
            if game['winner'] == 0:
                wins = (wins[0] + 1, wins[1])
            else:
                wins = (wins[0], wins[1] + 1)
            self.training_results[player0][player1] = wins
            self.training_results[player1][player0] = (wins[1], wins[0])

        self.sess = tf.Session()
        # Initialize variables (kernels for dense layers).
        tf.global_variables_initializer().run(session=self.sess)

        for epoch_no in range(self.nb_epochs):
            batch = sample(range(len(self.games)), k=self.mb_size)
            batch_x = self.games[batch]
            batch_y = self.winners[batch]

            loss, acc, _, preds = self.sess.run([self.loss, self.accuracy, self.op_train, self.preds], feed_dict={
                self.x: batch_x,
                self.y: batch_y
            })
            if epoch_no % 100 == 0:
                print("Epoch {0}: loss: {1}, acc: {2}".format(epoch_no, loss, acc))
            if epoch_no > 0 and epoch_no % self.lr_decay_time == 0:
                # Learning rate decay
                self.learning_rate /= 2
        pass

    def predict_match_result(self, bot0: str, deck0: Deck, bot1: str, deck1: DeckName) -> float:
        game_input = self._input_builder.build_game_input(game={
            'bot0': bot0,
            'bot1': bot1,
            'deck0': deck0['deckName'],
            'deck1': deck1
        })
        game_input = game_input.reshape((1, INPUT_SHAPE))
        pred = self.sess.run([self.preds], feed_dict={self.x: game_input})[0][0][0]
        return pred

    # returns the predicted winrate of (bot, deck) vs all (bot, deck) pairs in the training set
    def predict(self, bot: str, deck: Deck) -> float:
        winrate = 0
        for player in self.training_results:
            winrate += self.predict_match_result(bot, deck, player[0], player[1])
        winrate /= len(self.training_results)
        print(winrate)
        return winrate * 100


if __name__ == '__main__':
    test_model(NeuralNet)
    generate_submission(NeuralNet, {})
