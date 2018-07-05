# coding=utf-8
class TrainingConfig(object):
    decay_step = 15000
    decay_rate = 0.95
    # epoches = 3000
    epoches = 1000
    # epoches = 2
    evaluate_every = 100
    checkpoint_every = 100

class ModelConfig(object):
    conv_layers = [[256, 7, 3],
                   [256, 7, 3],
                   [256, 3, None],
                   [256, 3, None],
                   [256, 3, None],
                   [256, 3, 3]]

    fc_layers = [1024, 1024]
    dropout_keep_prob = 0.9
    # learning_rate = 0.001
    learning_rate = 0.0001
class Config(object):
    # alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"
    alphabet = "bpmfdtnlgkhjqxzcsrywaoeiuv0123456789-./+-="

    alphabet_size = len(alphabet)
    l0 = 128
    batch_size = 128
    nums_classes = 6
    # nums_classes = 4
    example_nums = 120000
    val_nums = 9600
    val_twice = int(val_nums/batch_size)
    train_twice = int(example_nums/batch_size)

    # train_data_source = 'data/ag_news_csv/train.csv'
    # dev_data_source = 'data/ag_news_csv/test.csv'
    sample_data_source = 'data/ag_news_csv/test.csv'  #预测时当对象用，只是为了使用data_helper中的字符2数字，以及词嵌入表的使用，必须
	
    train_data_source = 'D:/DataSet/MachaneLearing/Classification/ner_5/train/ALL_10_5_pinyin.txt.train'  #必须，训练数据
    dev_data_source = 'D:/DataSet/MachaneLearing/Classification/ner_5/train/ALL_10_5_pinyin.txt.val'      #必须，验证数据
    test_data_source = 'D:/DataSet/MachaneLearing/Classification/ner_5/train/ALL_10_5_pinyin.txt.test'    #测试数据
    classes_data_source = 'data/ag_news_csv/classes.txt'                                                  #类别数据，本实例6个类
    training = TrainingConfig()

    model = ModelConfig()


config = Config()
