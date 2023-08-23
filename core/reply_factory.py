
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    session[str(current_question_id)+"_response"]=answer.strip()

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    qid = 1
    if current_question_id :
       qid =current_question_id+1
    if qid<len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[qid-1]["question_text"]+"\n Options are:"+"\n".join(PYTHON_QUESTION_LIST[qid-1]["options"]), qid
    else:
        return None,None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score=0
    for i in range(len(PYTHON_QUESTION_LIST)):
        if str(i+1)+"_response" in session:
            if session.get(str(i+1)+"_response") ==  PYTHON_QUESTION_LIST[i]["answer"]:
                score+=1

    return "Score is:"+str(score)
