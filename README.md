# char-CNN-text-classification-tensorflow

## [Here is an article explaining this code](http://blog.csdn.net/Irving_zhang/article/details/75634108) ##

## Reqirement ##
- Python 3.5.5
- Numpy 1.13.1
- TensorFlow 1.2.1-1.8

## Running ##
python training.py

## Models ##
charCNN.py : 9-layer large convolutional neural network based on raw character.

## Dataset ##
If dataset is not found under datasets_dir, it will be downloaded automatically. 
The feeding method is used now to get data into TF model.

-- ag: [AG](http://www.di.unipi.it/~gulli/AG_corpus_of_news_articles.html) is a collection of more than 1 million 
news articles. News articles have been gathered from more than 2000 news sources by ComeToMyHead in more than 1 year of 
activity. ComeToMyHead is an academic news search engine which has been running since July, 2004.


## 正确的是1e-4
试了试其他的epsilon=[0.01, 0.001, 1e-5]，学习率为默认0.001。
结果是：前两个太大（？）学习不到什么loss在1.3震荡；
1e-5的结果和默认的1e-8没区别，同样在step=4000左右崩了（然后回升）。 求调参经验！
举报回复


##  您好，首先谢谢您的分享。 Q: 我在训练3k步左右（acc=0.8, loss=0.2左右）时，acc骤降（至0.2）loss突增（至10000+），
然后又慢慢回到0.7（acc）左右。请问您有出现这种情况吗？原因您清楚吗？
PS: github上有解释说是Adam的问题（https://stackoverflow.com/questions/42327543/adam-optimizer-goes-haywire-after-200k-batches-training-loss-grows/42420014#42420014）？

问题：restore的时候费了很大力气