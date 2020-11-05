import random


# This entire setup is spaghetti code
def switch_question(qid, intent, chatbot_sentiments):
    next_qid = ""
    chatbot_response = ""
    # if the intent is a fallback and the last question was not a fallback
    # ask a fallback question
    if qid == "start":
        next_qid = "q1"
    elif intent == "default_fallback" and qid[-1] != "b":
        next_qid = qid + "b"
    # send end message if qid index is too high
    elif int(qid[1]) > 4:
        next_qid = 'q5'
    # otherwise skip to the next question
    else:
        next_qid = "q"+str(int(qid[1])+1)

    questions = {
        "q1": "Hey There! You've recently signed up to this new StreamingService, would you say your overall impression was positive or negative?",
        "q1b": "Sorry, I didn't get that. Please let us know how you feel about your streaming service.",
        "q2": "Were you satisfied with the sign-up process?",
        "q2b": "Sorry, I didn't get that. Please provide some additional details.",
        "q3": "Based on the last film you watched, would you recommend this streaming service to your friends and family?",
        "q3b": "Sorry, I didn't get that.",
        "q4": "How about our selection, did you find what you were looking for in our selection?",
        "q4b": "Was it exactly what you were looking for?",
        "q5": "That's everything, thanks for chatting with us and have a great day!",
    }

    if intent == "Positive" and next_qid < "q5":
        positive_phrases = [
            "That's good to hear! ",
            "That's great to hear. ",
            "That’s nice! ",
            "Glad to hear you liked it! ",
            "Sounds like you really liked it. ",
            "Ok, great! ",
            "That's great. "
        ]
        chatbot_response += positive_phrases[int(next_qid[1])]

    elif intent == "Negative" and next_qid < "q5":
        negative_phrases = [
            "Oh No! ",
            "Sorry to hear that! ",
            "Sounds like you had some trouble with it! ",
            "Sorry to hear you're unhappy with it. Please continue sharing your experiences. ",
            "Please let us know how we can improve our service. ",
            "Sorry to hear that. Please continue sharing your experiences. "
        ]

        chatbot_response += negative_phrases[int(next_qid[1])]

    chatbot_response += questions[next_qid]

    return {"qid": next_qid, "chatbot_response": chatbot_response, "sentiment_scores": chatbot_sentiments}


