# -*- coding: utf-8 -*-
#讀json檔案，將新聞標題取出，並轉成大寫

def get_topics():
    #輸入user資料
    import os
    import pandas as pd
    import json
    import sys

    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    project_path = os.path.join(current_dir_path, '__APPTemplate')
    data_path = os.path.join(project_path, 'data.json')
    with open(data_path) as f:
        fff = json.load(f)

    user1_news = []
    user2_news = []
    user3_news = []
    a = -2
    for id in fff['UserId']:
        a += 2
        if id == '1':
            user1_news.append(fff['Other'][a][0])
            dict1 = {'user':user1_news}
            df1 = pd.DataFrame(dict1)
        if id == '2':
            user2_news.append(fff['Other'][a][0])
            dict2 = {'user':user2_news}
            df2 = pd.DataFrame(dict2)
        if id == '3':
            user3_news.append(fff['Other'][a][0])
            dict3 = {'user':user3_news}
            df3 = pd.DataFrame(dict3)

    if fff['UserId'][-1] == '1':
        df_this_user = df1
    elif fff['UserId'][-1] == '2':
        df_this_user = df2
    elif fff['UserId'][-1] == '3':
        df_this_user = df3
    else:
        sys.exit()
    title=df_this_user['user'].str.lower()

    #開始跑演算法
    from nltk import pos_tag
    from nltk import word_tokenize
    from nltk import FreqDist
    from nltk.corpus import stopwords
    import string

    #斷詞
    words = sum(title.map(word_tokenize), [])

    #判斷是否為名詞
    is_noun = lambda pos: pos[:2] == 'NN'
    nouns = [word for (word, pos) in pos_tag(words) if is_noun(pos)] 

    #去除stopword、半形標點、全形標點
    nouns2 = [word for word in nouns if word not in (stopwords.words('english') and string.punctuation and "‘’‛“”„‟")]
    nouns3 = [word for word in nouns2 if len(word)> 1]

    #找出頻率第一高的名詞
    common = FreqDist(nouns3).most_common(1)[0][0].capitalize()



    #把新聞title有涵蓋頻率第一高的名詞都抓出來
    import os
    import json

    path = "C:\\Users\\USER\\Desktop\\News_DailyData_AdjustedSource\\"
    #path = os.path.join(current_dir_path, 'News_DailyData_AdjustedSource')
    dirs = os.listdir(path)

    #related_news = pd.DataFrame(columns=['description', 'link'])
    news_title = list()

    for f in dirs:
        file_path = os.path.join(path, f)    
        file = open(file_path, mode= 'r', encoding="utf-8")
        jsonData = json.load(file)
        file.close()
        for news in jsonData:
            try:
                if common in news['title']:
                    news_title.append(news['title'])
            except TypeError:
                continue

    #把新聞標題拆成2dlist            
    split_news_title = []

    #手動刪去法
    badwords = ["‘’‛“”„‟", 'New','Judge','Says','Court','Administration']

    for t in news_title:
        split_title = word_tokenize(t)
        split_title1 = [word for (word, pos) in pos_tag(split_title) if is_noun(pos)] 
        split_title2 = [word for word in split_title1 if word.lower() not in stopwords.words('english')]
        split_title3 = [word for word in split_title2 if word.lower() not in  string.punctuation]
        split_title4 = [word for word in split_title3 if word not in badwords]
        split_title5 = [word for word in split_title4 if len(word)> 1]
        split_news_title.append(split_title5)



    #找出與common有最高相關性的三個字詞
    from gensim.models.word2vec import Word2Vec
    
    def hash(astring):
        return ord(astring[0])

    model = Word2Vec(split_news_title,seed = 1, workers = 1)

    def most_similar(w2v_model, words, topn=10):
        similar_df = pd.DataFrame()
        for word in words:
            try:
                similar_words = pd.DataFrame(w2v_model.wv.most_similar(word, topn=topn), columns=[word, 'cos'])
                similar_df = pd.concat([similar_df, similar_words], axis=1)
            except:
                print(word, "not found in Word2Vec model!")
        return similar_df

    similar_word = most_similar(model, [common])

    #output = topic, sub1 , sub2 , sub3
    output = [common, similar_word.iloc[0,0], similar_word.iloc[1,0], similar_word.iloc[2,0]]

    return output