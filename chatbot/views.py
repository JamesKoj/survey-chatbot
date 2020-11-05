from django.http import JsonResponse
import numpy as np
import tensorflow.compat.v1 as tf
# from tensorflow.compat.v1.keras.backend import set_session
import json
import pickle
import chatbot.helpers
from .questions import switch_question
# third party imports
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer
from .models import Post

global sess, trained_model, graph
# Why was session not necessary on heroku, probably because we're using Tensorflow 2.0
# sess = tf.Session()
# set_session(sess)

# graph = tf.get_default_graph()
trained_model = tf.keras.models.load_model('chatbot/chatbotmodel_Q1.h5')

intents = json.loads(open('chatbot/intents2.json').read())
words = pickle.load(open('chatbot/words.pkl','rb'))


# Create your views here.
class ChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            raw_sentence = serializer.data["user_response"]
            sentence = chatbot.helpers.clean_up_sentence(raw_sentence)
            sentence_array = chatbot.helpers.bow(sentence, words, show_details=True)
            # with graph.as_default():
                # set_session(sess)
            sentiment_probabilities = trained_model.predict(np.array([sentence_array]))[0]
            # returns a list of predictions with an error threshold of 0.57
            prediction = chatbot.helpers.predict_class(sentiment_probabilities, 0.57)
            res = chatbot.helpers.getResponse(prediction, intents)
            # full prediction list without an error threshold to add to API endpoint
            chatbot_predictions = chatbot.helpers.predict_class(sentiment_probabilities, 0)
            return JsonResponse(switch_question(serializer.data["qid"], res["tag"], chatbot_predictions))
        return Response(serializer.errors)

