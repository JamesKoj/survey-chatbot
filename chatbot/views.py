from django.http import JsonResponse
import numpy as np
import chatbotAPI.settings as chatbotSett
import chatbot.helpers
from .questions import switch_question
# third party imports 
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer
from .models import Post

# Why was session not necessary on heroku, probably because we're using Tensorflow 2.0
# sess = tf.Session()
# set_session(sess)

# graph = tf.get_default_graph()



# Create your views here.
class ChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            raw_sentence = serializer.data["user_response"]
            sentence = chatbot.helpers.clean_up_sentence(raw_sentence)
            sentence_array = chatbot.helpers.bow(sentence, chatbotSett.words, show_details=True)
            # with graph.as_default():
                # set_session(sess)
            sentiment_probabilities = chatbotSett.trained_model.predict(np.array([sentence_array]))[0]
            # returns a list of predictions with an error threshold of 0.57
            prediction = chatbot.helpers.predict_class(sentiment_probabilities, 0.57)
            res = chatbot.helpers.getResponse(prediction, chatbotSett.intents)
            # full prediction list without an error threshold to add to API endpoint
            chatbot_predictions = chatbot.helpers.predict_class(sentiment_probabilities, 0)
            return JsonResponse(switch_question(serializer.data["qid"], res["tag"], chatbot_predictions))
        return Response(serializer.errors)

