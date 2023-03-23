import re


# load the data
movie_lines_data = open(file="../data/movie_lines.txt",
                        encoding="utf-8", errors="ignore").read().split("\n")
movie_conversations_data = open(file="../data/movie_conversations.txt",
                                encoding="utf-8", errors="ignore").read().split("\n")


# make a dictionary that maps each line and its id
def map_id_to_line(lines_data):
    id_to_line = {}
    for line in lines_data:
        _line = line.split(' +++$+++ ')
        if len(_line) == 5:
            id_to_line[_line[0]] = _line[4]
    return id_to_line

def clean_conversations(conversations_data):
    conversations_list = []
    for conversation in conversations_data[:-1]:
        clean_conv = (conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "")).replace(" ", "")
        conversations_list.append(clean_conv.split(","))
    return conversations_list

# Define a function to preprocess text
def preprocess(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text

def map_conversations():
    line_id_dict = map_id_to_line(movie_lines_data)
    conversation_ids = clean_conversations(movie_conversations_data)
    questions = []
    answers = []
    for conversation in conversation_ids:
        for i in range(len(conversation) - 1):
            preprocess_question = preprocess(line_id_dict[conversation[i]])
            preprocess_answer = preprocess(line_id_dict[conversation[i+1]])
            questions.append(preprocess_question)
            answers.append(preprocess_answer)
    for i in range(len(answers)):
        answers[i] += ' <EOS>'
    return {"questions": questions, "answers": answers}

def count_occurences():
    word_to_count = {}
    for question in map_conversations().get("questions"):
        for word in question.split():
            if word not in word_to_count:
                word_to_count[word] = 1
            else:
                word_to_count[word] += 1
    for answer in map_conversations().get("answers"):
        for word in answer.split():
            if word not in word_to_count:
                word_to_count[word] = 1
            else:
                word_to_count[word] += 1
    return word_to_count

def map_to_unique_integer():
    count_words_dict = count_occurences()
    tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
    threshold = 20
    words_to_int = {}
    word_number = 0
    for word, count in count_words_dict.items():
        if count >= threshold:
            words_to_int[word] = word_number
            word_number += 1
    # add tokens ids
    for token in tokens:
        if token in words_to_int:
            continue
        words_to_int[token] = len(words_to_int) + 1
    # inverse the dictionary
    int_to_words = {w_int: w for w, w_int in words_to_int.items()}
    return int_to_words

def conv_to_int(conversation_type):
    cleaned_text = map_conversations().get(conversation_type)
    int_to_words_dict = map_to_unique_integer()
    conv_to_int = []
    res = dict((v, k) for k, v in int_to_words_dict.items())
    for line in cleaned_text:
        ints = []
        for word in line.split():
            if word not in res:
                ints.append(res["<OUT>"])
            else:
                ints.append(res[word])
        conv_to_int.append(ints)
    return conv_to_int

def sort_by_occurence():
    sorted_questions = []
    sorted_answers = []
    conv_questions_int = conv_to_int("questions")
    conv_answers_int = conv_to_int("answers")
    for length in range(1, 25 + 1):
        for i in enumerate(conv_questions_int):
            if len(i[1]) == length:
                sorted_questions.append(conv_questions_int[i[0]])
                sorted_answers.append(conv_answers_int[i[0]])
    return {"sorted_questions": sorted_questions, "sorted_answers": sorted_answers}








# map_conversations()
# mappp = map_conversations().get("questions")
#
# for i in mappp:
#     preprocess(i)
