# char-CNN-text-classification-tensorflow

## [Here is an article explaining this code](http://blog.csdn.net/Irving_zhang/article/details/75634108) ##

## 代码来源
   代码绝大部分来源于[lc222/char-cnn-text-classification-tensorflow](https://github.com/lc222/char-cnn-text-classification-tensorflow)，
   仅作中文转pingyin处理, 添加predict

## Reqirement ##
- Python 3.5.5
- Numpy [1.13.1]
- TensorFlow 1.2.1-1.8

## predition ##
python pred_inupt.py


                                                                Connected to pydev debugger (build 171.3780.115)
                                                                正在载入数据、模型...
                                                                载入模型成功1...
                                                                载入模型成功2...
                                                                input_Chinese:
                                                                我想看斗破
                                                                我想看斗破 	 VIDEO
                                                                耗时：  1.718341588973999
                                                                input_Chinese:
                                                                我想唱歌
                                                                我想唱歌 	 APP
                                                                耗时：  0.004961252212524414
                                                                input_Chinese:
                                                                明天天气怎么样
                                                                明天天气怎么样 	 WEATHER
                                                                耗时：  0.0034716129302978516
                                                                input_Chinese:

## Running ##
need构造 训练数据，验证数据， 标签数据
python training.py

## Models ##
charCNN.py : 9-layer large convolutional neural network based on raw character.

## 数据与步骤 ##
自己构造，
a.首先xpinyinUtil.py，  将    
                             我想看火影     （这里是'\t'）       VIDEO    
                      转化为    
                             VIDEO	       （这里是'\t'）        zai jiao zhou de tian qi
                      拼音
                      
b.然后suffle.py打乱  训练数据和验证数据 120000:9600
c.配好config的地址和参数（主要就是训练数据和验证数据、标签数据） 
                      标签数据格式  VIDEO 1
                                   MUSIC 2
d.接着就是training.py   训练800step, 准确率95、96%这样,  验证准确率85.9%，还不错，不过没有LSTM那么好就是了
## 正确的是1e-4
试了试其他的epsilon=[0.01, 0.001, 1e-5]，学习率为默认0.001。
结果是：前两个太大（？）学习不到什么loss在1.3震荡；
1e-5的结果和默认的1e-8没区别，同样在step=4000左右崩了（然后回升）。 求调参经验！
举报回复


##  您好，首先谢谢您的分享。 Q: 我在训练3k步左右（acc=0.8, loss=0.2左右）时，acc骤降（至0.2）loss突增（至10000+），
然后又慢慢回到0.7（acc）左右。请问您有出现这种情况吗？原因您清楚吗？
PS: github上有解释说是Adam的问题（https://stackoverflow.com/questions/42327543/adam-optimizer-goes-haywire-after-200k-batches-training-loss-grows/42420014#42420014）？

问题：restore的时候费了很大力气
