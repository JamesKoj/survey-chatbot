import nltk
from nltk import ngrams
from nltk.stem import WordNetLemmatizer
import numpy as np
lemmatizer = WordNetLemmatizer()
import pickle
classes = pickle.load(open('chatbot/classes.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

    # add the bigrams to the sentence words
    twograms = ngrams(sentence.split(), 2)
    for phrase in twograms:
        phrase_string = phrase[0] + " " + phrase[1]
        sentence_words.append(phrase_string.lower())

    # add the 3-grams to the sentence words
    threegrams = ngrams(sentence.split(), 3)
    for phrase in threegrams:
        phrase_string = phrase[0] + " " + phrase[1] + " " + phrase[2]
        sentence_words.append(phrase_string.lower())

    print(sentence_words)
    return sentence_words


# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

            # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # bag of words - matrix of N words, vocabulary matrix
    array_length = len(words)
    bag = [0]*array_length
    for s in sentence:
        # check if phrase is found in the bag of words and return the index if found
        # could consider using hash table instead
        s_index = binary_search(words, 0, array_length-1, s)
        # if s is found in the bag_of_words set the index
        if s_index>-1:
            bag[s_index] = 1
            if show_details:
                print ("found in bag: %s" % s)

    return np.array(bag)


def predict_class(results, error_threshold):
    print(np.array([results]))
    probabilities = [[i,r] for i,r in enumerate(results) if r>error_threshold]
    # sort by strength of probability
    probabilities.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in probabilities:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    # append the 'default_fallback' intent to the end of the list, so that the list always contains the fallback intent
    return_list.append({"intent": "default_fallback", "probability": None})
    print(return_list)
    return return_list


def getResponse(ints, intents_json):
    # set tag to highest intent
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = i
            return result
