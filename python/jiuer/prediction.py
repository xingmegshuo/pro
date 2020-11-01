from keras.models import load_model
import jieba.analyse
import numpy as np
from keras.preprocessing import sequence

model = load_model('weight.h5')



def text_to_index_array(dic,sentence):
    new_sentence = []
    for sen in sentence:
        new_sen = []
        for word in sen:
            try:
                new_sen.append(dic[word])
            except:
                new_sen.append(0)
            # print(word)
        new_sentence.append(new_sen)
    return np.array(new_sentence)






def conver_vector_predict(str_r):
    new_str = jieba.analyse.extract_tags(str_r,topK=20,withWeight=False,allowPOS=())
    # print(type(open('index_dict.txt').read()))
    index_dict = eval(open('./index_dict.txt').read())
    x = text_to_index_array(index_dict,[new_str])
    x = sequence.pad_sequences(x,maxlen=50)
    y = model.predict_classes(x)
    return y


value = conver_vector_predict('AJ潮男站街必备 出门约会上街撩妹！')
class_data = eval(open('./class_data.txt').read())
print([k for k,v in class_data.items() if v==value[0]][0])