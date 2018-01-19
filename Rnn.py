"""
meacial@live.cn
link: blog.csdn.net/u014595019/article/details/52571966
深度学习笔记
"""
import numpy as np
import jieba


# data I/O
data = open('/Users/lgp/project/python/com.meacial/神经网络/1.txt','rb').read() # should be simple plain text file
data = data.decode('gbk')
data = list(jieba.cut(data,cut_all=False))
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)
print('data has %d characters, %d unique.' % (data_size,vocab_size))

char_to_ix = {ch:i for i,ch in enumerate(chars)}
ix_to_char = {i:ch for i,ch in enumerate(chars)}


# hyperparaeters
hidden_size = 200 # size of hidden layer of neurons
seq_length = 25 # number of steps to unroll the RNN for
learning_rate = 1e-1


# model parameters
Wxh = np.random.randn(hidden_size,vocab_size) * 0.01 # input to hidden
Whh = np.random.randn(hidden_size,hidden_size) * 0.01 # hidden to hidden
Why = np.random.randn(vocab_size,hidden_size) * 0.01 # hidden to output
bh = np.zeros((hidden_size,1)) # hidden bias
by = np.zeros((vocab_size,1)) # output bias



def lossFun(inputs, targets ,hprev):
	"""
	:param inputs: list of integers
	:param targets: list of integers
	:param hprev: Hx1 array of initial hidden state
	:return: the loss ,gradients on model parameters , and last hidden state
	"""
	xs, hs, ys, ps = {},{},{},{}

	hs[-1] = np.copy(hprev) # hprev 中间层的值，存作-1，为第一个做准备

	loss = 0

	# forward pass
	for t in range(len(inputs)):
		xs[t] = np.zeros((vocab_size,1)) # encode in 1-of-k representation
		xs[t][inputs[t]] = 1 # x[t]是一个第t个输入单词的向量

		# 双曲正切，激活函数，作用跟sigmoid类似
		# h(t) = tanh(Wxh * X + Whh * h(t-1) + bh) 生成新的中间层
		hs[t] = np.tanh(np.dot(Wxh,xs[t]) + np.dot(Whh, hs[t-1]) + bh) # hidden state tanh
		# y(t) = Why * h(t) + by
		ys[t] = np.dot(Why, hs[t]) + by # unnormalized log probabilities for next chars
		# softmax regularization
		# p(t) = softmax(y(t))
		ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t])) # probabilities for next chars , 对输入做softmax
		# loss += -log(value) 预期输出是1，因此这里的value只就是此次的代价函数，使用-log(*)使得离正确输出越远，代价函数就越高
		loss += -np.log(ps[t][targets[t],0]) # softmax (cross - entropy loss) 代价函数是交叉熵


	# 将输入循环一遍以后，得到各个时间段的h,y和p
	# 得到此时累计的loss,准备进行更新矩阵
	# backward pass: compute gradients going backwords
	dWxh, dWhh, dWhy = np.zeros_like(Wxh),np.zeros_like(Whh),np.zeros_like(Why) # 各举止的参数进行
	dbh, dby = np.zeros_like(bh), np.zeros_like(by)
	dhnext = np.zeros_like(hs[0]) # 下一个时间段的潜在层，初始化为零向量
	for t in reversed(range(len(inputs))): # 把时间作为维度，则梯度的计算应该沿着时间回溯
		dy = np.copy(ps[t]) # 设dy为实际输出（单位向量）为y,代价函数为交叉熵函数
		dy[targets[t]] -= 1 # backprop into y. see h
		dWhy += np.dot(dy,hs[t].T) # dy * h(t).T h层值越大的相，如果错误，则惩罚越严重，反之奖励越多，
		dby += dy
		dh = np.dot(Why.T, dy) + dhnext
		dhraw= (1- hs[t]* hs[t] ) * dh
		dbh += np.dot(dhraw, xs[t].T)
		dWxh += np.dot(dhraw, xs[t].T)
		dWhh += np.dot(dhraw,hs[t-1].T)
		dhnext = np.dot(Whh.T,dhraw)

	for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
		np.clip(dparam,-5,5,out=dparam)
	return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(inputs)-1]



def sample(h, seed_ix, n):
	"""
	sample a sequence of integers from the model
	:param h: is the memory state
	:param seed_ix: is seed letter for first time step
	:param n:
	:return:
	"""
	x = np.zeros((vocab_size,1))
	x[seed_ix] = 1
	ixes = []
	for t in range(n):
		h = np.tanh(np.dot(Wxh,x)+np.dot(Whh,h) + bh)
		y = np.dot(Why,h)+by
		p = np.exp(y) / np.sum(np.exp(y)) # softmax
		ix = np.random.choice(range(vocab_size),p=p.ravel()) # 根据softmax的到的结果，按照概率产生下一个字符
		x = np.zeros((vocab_size,1)) # 产生下一轮的输入
		x[ix] = 1
		ixes.append(ix)
	return ixes



n, p = 0, 0
mWxh, mWhh, mWhy = np.zeros_like(Wxh),np.zeros_like(Whh),np.zeros_like(Why)
mbh,mby = np.zeros_like(bh), np.zeros_like(by) # memory variables for adagrad
smooth_loss = -np.log(1.0 / vocab_size) * seq_length
while True:
	if p+seq_length + 1 >= len(data) or n == 0:
		hprev = np.zeros((hidden_size,1))
		p = 0
	inputs = [char_to_ix[ch] for ch in data[p:p+seq_length]]
	targets = [char_to_ix[ch] for ch in data[p+1: seq_length+1]]

	if n % 100 == 0:
		sample_ix = sample(hprev,inputs[0],200)
		txt = ''.join(ix_to_char[ix] for ix in sample_ix)
		print('------\n %s \n------' % (txt,))

	loss, dWxh, dWhh, dWhy, dbh, dby, hprev = lossFun(inputs,targets,hprev)
	smooth_loss = smooth_loss * 0.999 + loss * 0.001

	if n % 100 == 0:
		print('iter %d, loss : %f' % (n, smooth_loss))


	for param, dparam, mem in zip([Wxh, Whh, Why, bh, by],[dWxh, dWhh, dWhy, dbh, dby], [mWxh, mWhh, mWhy, mbh, mby]):
		mem += dparam * dparam
		param += -learning_rate * dparam / np.sqrt(mem+1e-8)

	p += seq_length
	n += 1










