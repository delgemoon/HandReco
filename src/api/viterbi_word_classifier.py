'''
Created on Jul 25, 2011

@author: C
'''
import sys
sys.path.append("../gui")
sys.path.append("../api")
sys.path.append("..")

from hmm import HMM
from api.simple_image_feature_extractor import SimpleImageFeatureExtractor
from api.character_classifier import CharacterClassifier
from java.io import File
import unittest
import pickle
import random
import inspect

def zeros(x, y = None, content = 1e-10):
    ''' Return a matrix of zeros with height x and width y. '''
    if y == None:
        return [content] * x
    matrix = []
    for i in range(x):
        matrix.append([content] * y)
    return matrix

class WordClassifier(object):
    '''
    Classifies a possible misspelled word to a word
    '''


    def __init__(self, words=None):
        self.words = words

        self.alphabet =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.alphabet = ["@"] + self.alphabet + ["$"]
        len_states = len(self.alphabet)
        pi = zeros(len_states)
        pi[0] = 1.0
        A = zeros(len_states, len_states)
        for word in self.words:
            numbers = self.observationsToNumbers('@' + word + '$')
            for n1, n2 in zip(numbers[:-1], numbers[1:]):
                A[n1][n2] += 1
        for i in range(len_states):
            A[i] = [j * 1.0 / sum(A[i]) for j in A[i]]
        #words = ["pig","dog","cat","bee","ape","elk","hen","cow"]
        content = 0.3 / (len_states - 3)
        B = zeros(len_states, len_states, 1e-10)
        
        normalized_count_matrix_100_examples = \
        [[0.8, 0.0, 0.01, 0.0, 0.0, 0.07, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.05, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0],
         [0.0, 0.86, 0.0, 0.0, 0.04, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.04, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04],
         [0.0, 0.0, 0.86, 0.0, 0.0, 0.04, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.07, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.48, 0.0, 0.02, 0.0, 0.0, 0.0, 0.02, 0.0, 0.0, 0.0, 0.0, 0.08, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.05, 0.0, 0.0, 0.79, 0.0, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06],
         [0.0, 0.0, 0.11, 0.0, 0.0, 0.62, 0.0, 0.0, 0.01, 0.0, 0.23, 0.0, 0.0, 0.0, 0.0, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.79, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03, 0.0, 0.13, 0.01, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02],
         [0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.56, 0.0, 0.13, 0.0, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02, 0.2, 0.04, 0.0, 0.0, 0.01, 0.0],
         [0.05, 0.01, 0.0, 0.0, 0.0, 0.02, 0.0, 0.0, 0.34, 0.0, 0.0, 0.0, 0.15, 0.02, 0.0, 0.0, 0.0, 0.04, 0.03, 0.02, 0.0, 0.01, 0.08, 0.15, 0.08, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.81, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.18, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.01, 0.09, 0.02, 0.0, 0.27, 0.0, 0.0, 0.0, 0.0, 0.58, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.02, 0.0, 0.0],
         [0.0, 0.0, 0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.96, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03, 0.01, 0.0, 0.0, 0.44, 0.13, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.17, 0.08, 0.14, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06, 0.0, 0.0, 0.0, 0.0, 0.24, 0.21, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.18, 0.05, 0.22, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.03, 0.04, 0.01, 0.0, 0.08, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.79, 0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.01, 0.0, 0.0, 0.29, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.13, 0.54, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02, 0.0, 0.89, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.14, 0.0, 0.0, 0.1, 0.0, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.62, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.1],
         [0.0, 0.12, 0.0, 0.01, 0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02, 0.0, 0.0, 0.0, 0.73, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.93, 0.0, 0.0, 0.01, 0.0, 0.03, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0, 0.09, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.79, 0.02, 0.04, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03, 0.0, 0.14, 0.13, 0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.21, 0.3, 0.07, 0.0, 0.09, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.17, 0.09, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13, 0.05, 0.55, 0.0, 0.0, 0.0],
         [0.03, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06, 0.0, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.83, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.14, 0.01, 0.06, 0.0, 0.0, 0.62, 0.0],
         [0.0, 0.04, 0.0, 0.0, 0.12, 0.0, 0.07, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.12, 0.12, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.52]]

        for i in range(1, len_states - 1):
            B[i][1:-1] = normalized_count_matrix_100_examples[i-1] 
            
        for i in range(len(B)):
            B[i] = [j if j > 1e-10 else 1e-10 for j in B[i]]
        
        B[0] = zeros(len_states, content = 1e-10)
        B[0][0] = 1.0
        
        last_state = len_states - 1
        B[last_state] = zeros(len_states, content = 1e-10)
        B[last_state][last_state] = 1.0

        self.hmm = HMM(pi,A,B,self.alphabet)
    
    def observationsToNumbers(self, observations):
        return [self.alphabet.index(o) for o in observations]
    
    def distanceBetweenTwoWords(self, word1, word2):
        if len(word1) != len(word2):
            return max(len(word1), len(word2))
        
        return sum([1 if c1 != c2 else 0 for c1, c2 in zip(word1, word2)])

    def classify(self,observations):
        O =  self.observationsToNumbers('@' + observations + '$')
        result = self.hmm.viterbi(O)
        result = [self.alphabet[i] for i in result]
        result = reduce(str.__add__, result)
        result = result[1:-1]
        distances = [self.distanceBetweenTwoWords(result, eachWord) for eachWord in self.words]
        corrected_result = self.words[distances.index(min(distances))]
        return result,corrected_result
    
    def test(self,test_examples):
        '''
        Parameter:
        test_examples - is a list of tuples were the first element in the tuples
        is a string representing a word that the classifier should handle and the second
        element is a list of test examples for that word.
        
        Returns:
        Fraction of correctly classified test examples
        '''

        correctly_classified_counter = 0.0
        wrongly__classified_counter = 0.0
        for word, examples in test_examples:
            for example in examples:
                result = self.classify(example)
                if result== word:
                    correctly_classified_counter = correctly_classified_counter + 1
                else:
                    wrongly__classified_counter = wrongly__classified_counter + 1
        total_nr_of_tests = correctly_classified_counter + wrongly__classified_counter
        score = correctly_classified_counter / total_nr_of_tests
        return score
    
    def to_string(self):
        return "not finished"
     
class TestWordClassifier(unittest.TestCase):

    feature_extraction_number_of_segments = 11
    feature_extraction_classification_factor = 4.6
    word_list1 = ["pig","dog","cat","bee","ape","elk","hen","cow"]
    word_list2 = ['asexual', 'amoral', 'anarchy', 'anhydrous', 'anabaptist', 'anachronism', 'abnormal',
                   'abduct', 'abductor', 'abscission', 'agent', 'agency', 'agenda', 'antipathy', 
                   'antitank', 'anticlimax', 'aquarium', 'aqueous', 'automatic', 'automaton', 
                   'bisexual', 'biennial', 'binary', 'benefit', 'benevolent', 'benefactor', 
                   'beneficent', 'biology', 'biography', 'circumference', 'circumlocution', 
                   'circumstance', 'democracy', 'theocrat', 'technocracy', 'diagonal', 'dialectic', 
                   'dialogue', 'diagnosis', 'dynamic', 'dynamo', 'dynasty', 'dynamite', 'exotic', 
                   'exterior', 'extraneous', 'extemporaneous', 'exophalmic', 'exogenous', 'exothermic', 
                   'federation', 'confederate', 'fraternize', 'fraternity', 'fraternal', 'fratricide', 
                   'geology', 'geography', 'geocentric', 'geomancy', 'graphic', 'graphite', 
                   'graphology', 'heterogeneous', 'heterosexual', 'heterodox', 'heterodont', 
                   'heterocyclic', 'heterozygous', 'homogeneous', 'homogenized', 'homozygous', 
                   'identity', 'idiopathic', 'individual', 'idiosyncrasy', 'idiopathic', 'incredible', 
                   'ignoble', 'inglorious', 'inhospitable', 'infinite', 'infinitesimal', 'immoral', 
                   'interact', 'interstellar', 'interpret', 'interstitial', 'legal', 'legislature', 
                   'lexicon', 'lexicography', 'liberty', 'library', 'liberal', 'locality', 'local', 
                   'circumlocution', 'mission', 'transmit', 'remit', 'monocle', 'monopoly', 'monogamy', 
                   'monovalent', 'monomania', 'monarchy', 'oligarchy', 'oligopoly', 'paternal', 
                   'paternity', 'patricide', 'peripatetic', 'periscope', 'perineum', 'peritoneum', 
                   'political', 'metropolitan', 'premier', 'preview', 'premium', 'prescient', 'project', 
                   'projectile', 'public', 'republic', 'pub', 'publican', 'psychology', 'solo', 
                   'solitary', 'synchronize', 'symphony', 'sympathy', 'syncretic', 'syncope', 
                   'subterfuge', 'subtle', 'subaltern', 'subterranean', 'telegraph', 'telephone', 
                   'teleology', 'transport', 'transcend', 'transmogrify', 'utility', 'utilitarian', 
                   'video', 'vision', 'visible']
    alphabet =['a','b','c','d','e','f','g','h','i','j','k','l',
               'm','n','o','p','q','r','s','t','u','v','w','x','y','z']

    def extract_test_examples_to_file(self):
        extractor = SimpleImageFeatureExtractor(nr_of_divisions=self.feature_extraction_number_of_segments, 
                                    size_classification_factor=self.feature_extraction_classification_factor)
        examples_dir = File(File(File(File(str(inspect.getfile( inspect.currentframe() ))).getParent(),".."),".."),"word_examples_for_test").getCanonicalPath()
        empty, character_test_examples = extractor.extract_training_and_test_examples(examples_dir, #character_examples word_examples_for_test
                                                                            nr_of_training_examples=0,
                                                                            nr_of_test_examples=10)
                                                                            
        output = open('datatest_segments_' +
                      str(self.feature_extraction_number_of_segments) + '_cf_'+
                      str(self.feature_extraction_classification_factor).replace('.','_')+
                      '.pkl', 'wb')
        pickle.dump(character_test_examples, output)
        output.close()
   
   
    def get_test_examples(self):
        self.extract_test_examples_to_file()
        # the same effect to create the word testing data
        example_file = ('datatest_segments_' +
                        str(self.feature_extraction_number_of_segments) + '_cf_'+
                        str(self.feature_extraction_classification_factor).replace('.','_')+
                        '.pkl')
        pkl_file = open(example_file, 'rb')
        character_test_examples = pickle.load(pkl_file)
        character_test_examples.sort()
        #pprint.pprint(training_examples)
        pkl_file.close()
        return character_test_examples
    
    def get_character_classifier(self):
        path_to_this_dir = File(str(inspect.getfile( inspect.currentframe() ))).getParent()
        classifier_filename = ("character_classifier_" +
                               str(self.feature_extraction_number_of_segments) +
                               "_segments_cf_"+str(self.feature_extraction_classification_factor).replace('.','_')+
                               ".dat")
        character_classifier_file = open(File(path_to_this_dir,classifier_filename).getPath(),'r')
        character_classifier = CharacterClassifier(from_string_string=character_classifier_file.read())
        character_classifier_file.close()
        return character_classifier
        
    def gernerate_observation_from_word(self,word, character_classifier, character_test_examples):
        def gernerateCharacterFeatures(character):
            '''randomly choice the features of the character from the training_examples'''
            allFeatures = character_test_examples[self.alphabet.index(character)][1]
            return random.choice(allFeatures)
        observations = []
        for eachCharacter in word:
            character_features = gernerateCharacterFeatures(eachCharacter)
            observation = character_classifier.classify_character_string(character_features)
            observations.append(str(observation))
        observations = reduce(str.__add__, observations)
        return observations

    
    def test_word_once(self, word, wordClassifier, character_classifier, character_test_examples):
        #transfer the list of characters to their corresponding string
        observations = self.gernerate_observation_from_word(word, character_classifier, character_test_examples)
        word = wordClassifier.classify(observations.lower())
        return observations.lower(), word
    
    def classify(self, words):     

        character_test_examples = self.get_test_examples()
        character_classifier = self.get_character_classifier()
        word_classifier = WordClassifier(words=words)

        def testWordManyTimes(word, test_numbers = 100):
            for i in range(test_numbers):
                print self.test_word_once(word,word_classifier, character_classifier, character_test_examples)
        
        for eachWord in words:
            print eachWord
            testWordManyTimes(eachWord,10)
            
    def test_classify(self):
        print("WORD LIST 1")
        self.classify(self.word_list1)
        
        print("WORD LIST 2")
        self.classify(self.word_list2)
        
            
    def score(self, words):
        
        character_test_examples = self.get_test_examples()
        character_classifier = self.get_character_classifier()
        word_classifier = WordClassifier(words)
        
        def score_for_word(word, number_of_tests = 100):
            nr_of_correctly_classified = 0.0
            for i in range(number_of_tests):
                observation, (viterbi,classification) = self.test_word_once(word,word_classifier, character_classifier, character_test_examples)
                if classification == word:
                    nr_of_correctly_classified = nr_of_correctly_classified + 1
            return (nr_of_correctly_classified + 0.0) / (number_of_tests + 0.0)
        
        total_word_score = 0.0
        for word in words:
            score_for_w = score_for_word(word, number_of_tests = 10)
            total_word_score = total_word_score + score_for_w
            print '"Score for word '+ word + '" = ' + str(score_for_w)
        
        print "SCORE = " + str(total_word_score/(len(words)+0.0))
        
    def test_score(self):
        print("SCORE FOR WORD LIST 1")
        self.score(self.word_list1)
        
        print("SCORE FOR WORD LIST 2")
        self.score(self.word_list2)
        
                

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()
    
'''
Actually, I'm trying to use viterbi algorithm to do word classifier.
'''
        
        
