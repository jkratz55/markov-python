#!/usr/bin/env python

'''
 * Copyright 2002-2014 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
'''

#----------------------------------------------------------------------
# MarkovLanguage.py
# Joseph Kratz
#
# Python implementation of the Markov Alogrithm
#----------------------------------------------------------------------

import sys
import random

#----------------------------------------------------------------------

class MarkovLanguage(object):

    #------------------------------------------------------------------

    def __init__(self, state_size=2):

        '''intialize data structure with specified number of words per state'''

        self.state_size = state_size
        self.word_map = {}
        self.state = []

    #------------------------------------------------------------------

    def add_word(self, word):

        '''add specified word to the Markov model and update the state
        accordingly'''

        # if state is of specified size
        if len(self.state) == self.state_size:

            # make state a tuple since dictionary keys must be immutable
            state = tuple(self.state)

            # if state in dictionary add word as a possible next work
            if state in self.word_map:
                self.word_map[state].append(word)
            else:
                # if not, create state with this as the next word
                self.word_map[state] = [word]

            # remove first word in state
            self.state.pop(0)

        # append word to state
        self.state.append(word)

    #------------------------------------------------------------------        

    def set_state(self, phrase):

        '''set state to specified phrase (mainly to allow testing)'''

        self.state = list(phrase.split())

    #------------------------------------------------------------------        

    def predict(self, starting_phrase=None):

        '''return a possible next word based on the current state'''

        # getting starting phrase if specified
        if starting_phrase is not None:
            self.state = starting_phrase.split()

        # convert state to a tuple
        self.state = tuple(self.state)

        # attempt to find next word
        try:
            word = random.choice(self.word_map[self.state])
        except:
            # if not, pick a random state and get the next word
            self.state = random.choice(self.word_map.keys())
            word = random.choice(self.word_map[self.state])

        # convert state to a list so we can change it
        self.state = list(self.state)
        
        # remove first word
        self.state.pop(0)
        
        # add new word to state
        self.state.append(word)
        return word

#----------------------------------------------------------------------

def main(argv):

    if len(argv) < 2:
        fname = raw_input('enter filename: ')
    else:
        fname = argv[1]

    if len(argv) < 3:
        state_size = input('enter state size: ')
    else:
        state_size = int(argv[2])

    n = input('enter number of words to output: ')

    ml = MarkovLanguage(state_size)
    f = open(fname, 'r')
    for line in f:
        for word in line.split():
            ml.add_word(word)

    for i in xrange(n):
        if i % 10 == 0:
            print
        w = ml.predict()
        print w,

#----------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
