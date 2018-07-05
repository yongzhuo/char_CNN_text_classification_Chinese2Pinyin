# coding=utf-8
import tensorflow as tf
from data_helper import Dataset
import time
from config import config
import numpy as np
import xpinyin
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

class char_CNN:
    with tf.device('/cpu:0'):
        pin = xpinyin.Pinyin()
        # Load data
        print("正在载入数据、模型...")
        #主要是onehot用
        sample_data_source = Dataset(config.sample_data_source)
        # test_data = Dataset(config.test_data_source)
        #获取最新的，可以改
        checkpoint_file = tf.train.latest_checkpoint('./runs/1530261778/checkpoints')
        graph = tf.Graph()
        with graph.as_default():
            sess = tf.Session()
            with sess.as_default():
                # Load the saved meta graph and restore variables
                saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
                saver.restore(sess, checkpoint_file)

                print("载入模型成功1...")
                # Get the placeholders from the graph by name
                input_x = graph.get_operation_by_name("input_x").outputs[0]
                # input_y = graph.get_operation_by_name("input_y").outputs[0]
                dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

                # Tensors we want to evaluate
                predictions = graph.get_operation_by_name("output_layer/predictions").outputs[0]

                #词向量嵌入， index2label
                embedding_w, embedding_dic = sample_data_source.onehot_dic_build()
                label_dict = {0: 'VIDEO', 1: 'TV', 2: 'APP', 3: 'CONTROL', 4: 'WEATHER', 5: 'MUSIC'}
                print("载入模型成功2...")


                @staticmethod
                def rec(text, sentencepinyin):
                    try:
                        doc_image = []
                        doc_vec = char_CNN.sample_data_source.doc_process(sentencepinyin, char_CNN.embedding_dic)
                        doc_image.append(doc_vec)
                        batch_xx = np.array(doc_image, dtype='int64')
                        prediction = char_CNN.sess.run(char_CNN.predictions, {char_CNN.input_x: batch_xx, char_CNN.dropout_keep_prob: 1.0})
                        ppred = str(prediction[0]).replace('[', '').replace(']', '')
                        label_pred = char_CNN.label_dict[int(ppred)]  # str转int  int转label
                        print(text, '\t', label_pred)
                        return label_pred
                    except:
                        print(text, "rec text wrong!")

                

