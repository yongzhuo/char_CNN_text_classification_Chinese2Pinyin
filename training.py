# coding=utf-8
import tensorflow as tf
from data_helper import Dataset
import time
import os
from tensorflow.python import debug as tf_debug
from charCNN import CharCNN
import datetime
from config import config

# Load data
print("正在载入数据...")
# 函数dataset_read：输入文件名,返回训练集,测试集标签
# 注：embedding_w大小为vocabulary_size × embedding_size
train_data = Dataset(config.train_data_source)
dev_data = Dataset(config.dev_data_source)
train_data.dataset_read()
dev_data.dataset_read()

print ("得到120000维的doc_train，label_train")
print ("得到9600维的doc_dev, label_train")

tf.reset_default_graph()

with tf.Graph().as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=True,
      log_device_placement=False)
    sess = tf.Session(config=session_conf)
    # sess = tf_debug.LocalCLIDebugWrapperSession(sess)
    with sess.as_default():
        cnn = CharCNN(
            l0=config.l0,
            num_classes=config.nums_classes,
            conv_layers=config.model.conv_layers,
            fc_layers=config.model.fc_layers,
            l2_reg_lambda=0)

        # cnn = CharConvNet()
        global_step = tf.Variable(0, name="global_step", trainable=False)
        optimizer = tf.train.AdamOptimizer(config.model.learning_rate)
        grads_and_vars = optimizer.compute_gradients(cnn.loss)
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

        # Keep track of gradient values and sparsity (optional)
        grad_summaries = []
        for g, v in grads_and_vars:
            if g is not None:
                grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name), g)
                sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
                grad_summaries.append(grad_hist_summary)
                grad_summaries.append(sparsity_summary)
        grad_summaries_merged = tf.summary.merge(grad_summaries)

        # Output directory for models and summaries
        timestamp = str(int(time.time()))
        out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
        print("Writing to {}\n".format(out_dir))

        # Summaries for loss and accuracy
        loss_summary = tf.summary.scalar("loss", cnn.loss)
        acc_summary = tf.summary.scalar("accuracy", cnn.accuracy)

        # Train Summaries
        train_summary_op = tf.summary.merge([loss_summary, acc_summary, grad_summaries_merged])
        train_summary_dir = os.path.join(out_dir, "summaries", "train")
        train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

        # Dev summaries
        dev_summary_op = tf.summary.merge([loss_summary, acc_summary])
        dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
        dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

        # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
        checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
        checkpoint_prefix = os.path.join(checkpoint_dir, "model")
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        saver = tf.train.Saver(tf.global_variables())

        # Initialize all variables
        sess.run(tf.global_variables_initializer())

        def train_step(i, x_batch, y_batch):
            """
            A single training step
            """
            feed_dict = {
              cnn.input_x: x_batch,
              cnn.input_y: y_batch,
              cnn.dropout_keep_prob: config.model.dropout_keep_prob
            }
            _, step, summaries, loss, accuracy = sess.run(
                [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
                feed_dict)
            time_str = datetime.datetime.now().isoformat()
            print("{}: epoches {}, step {}, loss {:g}, acc {:g}".format(time_str, i, step, loss, accuracy))
            train_summary_writer.add_summary(summaries, step)

        def dev_step(i, losss, accuracyy, x_batch, y_batch, writer=None):
            """
            Evaluates model on a dev set
            """
            feed_dict = {
              cnn.input_x: x_batch,
              cnn.input_y: y_batch,
              cnn.dropout_keep_prob: 1.0
            }
            step, summaries, loss, accuracy, predictions = sess.run(
                [global_step, dev_summary_op, cnn.loss, cnn.accuracy, cnn.predictions],
                feed_dict)
            time_str = datetime.datetime.now().isoformat()
            print("{}: epoches {}, step {}, loss {:g}, acc {:g}".format(time_str, i, step, loss, accuracy))
            print(predictions)
            if writer and losss > loss and accuracy > accuracyy:
                writer.add_summary(summaries, step)
                print("writed")
            return loss, accuracy, predictions

        print("初始化完毕，开始训练")
        losss, accuracyy = 0, 0
        for i in range(config.training.epoches):
            batch_train = train_data.next_batch()
            # 训练模型
            train_step(i, batch_train[0], batch_train[1])
            current_step = tf.train.global_step(sess, global_step)
            # train_step.run(feed_dict={x: batch_train[0], y_actual: batch_train[1], keep_prob: 0.5})
            # 对结果进行记录
            if current_step % config.training.evaluate_every == 0:
                print("\nEvaluation:")
                # dev_step(dev_data.doc_image, dev_data.label_image, writer=dev_summary_writer)
                batch_dev_data = dev_data.next_batch()
                loss1, accuracy1, predictions = dev_step(i, losss, accuracyy, batch_dev_data[0], batch_dev_data[1],
                                            writer=dev_summary_writer)
                losss, accuracyy = loss1, accuracy1
                print("")
            if current_step % config.training.checkpoint_every == 0:
                path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                print("Saved model checkpoint to {}\n".format(path))


        # print("初始化完毕，开始训练")
        # for i in range(config.training.epoches):
        #     batch_train = train_data.next_batch()
        #     # 训练模型
        #     train_step(i, batch_train[0], batch_train[1])
        #     current_step = tf.train.global_step(sess, global_step)
        #     # train_step.run(feed_dict={x: batch_train[0], y_actual: batch_train[1], keep_prob: 0.5})
        #     # 对结果进行记录
        #     losss, accuracyy = 0, 0
        #     if current_step % config.training.evaluate_every == 0:
        #         print("\nEvaluation:")
        #         # dev_step(dev_data.doc_image, dev_data.label_image, writer=dev_summary_writer)
        #         for k in range(config.val_twice):
        #             batch_dev_data = dev_data.next_batch()
        #             loss1, accuracy1 = dev_step(k, losss, accuracyy, batch_dev_data[0], batch_dev_data[1], writer=dev_summary_writer)
        #             losss, accuracyy = losss + loss1, accuracyy + accuracy1
        #         print("")
        #     if current_step % config.training.checkpoint_every == 0:
        #         path = saver.save(sess, checkpoint_prefix, global_step=current_step)
        #         print("Saved model checkpoint to {}\n".format(path))

                    # loss_val_old = 0
        # accuracy_val_old = 0
        # print ("初始化完毕，开始训练")
        # time_str = datetime.datetime.now().isoformat()
        # current_step = 0
        # for i in range(config.training.epoches):
        #     for j in range(config.train_twice):
        #         batch_train = train_data.next_batch()
        #         # 训练模型
        #         train_step(i, batch_train[0], batch_train[1])
        #         current_step = tf.train.global_step(sess, global_step)
        #     # train_step.run(feed_dict={x: batch_train[0], y_actual: batch_train[1], keep_prob: 0.5})
        #     # 对结果进行记录
        #     print("\nEvaluation:")
        #     loss_val = 0
        #     accuracy_val = 0
        #     for k in range(config.val_twice):
        #         batch_dev_data = dev_data.next_batch()
        #         loss1, accuracy1, predictions = dev_step(i, batch_dev_data[0], batch_dev_data[1])
        #         loss_val, accuracy_val = loss_val + loss1, accuracy_val + accuracy1
        #         if k == config.val_twice - 1:
        #             loss_val = loss_val/config.val_twice
        #             accuracy_val = accuracy_val/config.val_twice
        #             print("{}: valepoches {}, valstep {}, valloss {:g}, acc {:g}".format(time_str, i, k+1, loss_val, accuracy_val))
        #             if loss_val_old > loss_val and accuracy_val_old > accuracy_val:
        #                 path = saver.save(sess, checkpoint_prefix, global_step=current_step)
        #                 loss_val_old = loss_val
        #                 accuracy_val_old = accuracy_val

        # if current_step % config.training.checkpoint_every == 0:
        #     path = saver.save(sess, checkpoint_prefix, global_step=current_step)
        #     print("Saved model checkpoint to {}\n".format(path))
        # import xpinyin
        # import numpy as np
        # p = xpinyin.Pinyin()
        # embedding_w, embedding_dic = train_data.onehot_dic_build()
        # label_dict = {0:'VIDEO',1:'TV',2:'APP',3:'CONTROL',4:'WEATHER',5:'MUSIC'}
        # label_class = np.zeros(6, dtype='float32')
        # label_class[0] = 1
        # if current_step == 801:
        #     while True:
        #         print("input_Chinese:")
        #         text = input()
        #         textpinyin = p.get_pinyin(text, ' ')
        #         doc_image = []
        #         label_image = []
        #         # text = "Wall St. Bears Claw Back Into the Black (Reuters).Reuters - Short-sellers, Wall Street's dwindling\band of ultra-cynics, are seeing green again."
        #         doc_vec = train_data.doc_process(textpinyin, embedding_dic)
        #         doc_image.append(doc_vec)
        #         label_image.append(label_class)
        #         batch_xx = np.array(doc_image, dtype='int64')
        #         batch_yy = np.array(label_image, dtype='int32')
        #         los, accurac,  predictio= dev_step(i, 0, 0, batch_xx, batch_yy)
        #         ppred = str(predictio[0]).replace('[','').replace(']','')
        #         label_pred = label_dict[int(ppred)]  # 转换为list
        #         print(label_pred)


