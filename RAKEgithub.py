import re
import MeCab
import operator
tagger = MeCab.Tagger()


def splitsentences(text):
    """separate document into sentences(split with punctuation mark)"""
    sentences = re.split("。|、|！|？|…|――", text)
    return sentences


def separatewords(text):
    """do mornophical analysis, separate the words.
       if a noun (or name) connects to another noun (or name), combine into one word
    """
    words_list = []
    node = tagger.parseToNode(text)
    pos = "no"
    while node:
        if "名詞" in node.feature and "数" not in node.feature and "人名" not in node.feature:
            if pos == "yes":
                words_list[-1] = words_list[-1] + node.surface
            else:
                words_list.append(node.surface)
                pos = "yes"
        elif "名詞" in node.feature and "数" not in node.feature and "人名" in node.feature:
            if pos == "name":
                words_list[-1] = words_list[-1] + node.surface
            else:
                words_list.append(node.surface)
            pos = "name"
        else:
            words_list.append(node.surface)
            pos = "no"
        node = node.next
    return words_list


def calculatewordscore(sentences_list):
    """calculate the score of each word"""
    word_frequency = {}
    word_degree = {}
    for sentence in sentences_list:
        word_list = separatewords(sentence)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)
    return word_score


def main():
    """get top10 of words with highest scores"""
    filepath = "filepath"  # please input the filepath
    with open(filepath, "r", encoding="utf-8") as r:
        lines = r.readlines()
        for i in lines:
            allwords = []
            sentences_list = splitsentences(i)
            word_score = calculatewordscore(sentences_list)
            result = sorted(word_score.items(), key=operator.itemgetter(1), reverse=True)
            for j in result:
                allwords.append(j[0])
            print(allwords[: 5])


if __name__ == "__main__":
    main()
