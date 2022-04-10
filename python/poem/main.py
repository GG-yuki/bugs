import numpy as np
import collections
import torch
from torch.autograd import Variable
import torch.optim as optim
import time
import rnn as rnn_lstm
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='RNN to write poems')
    parser.add_argument('--lr', default=0.005, type=float,
                        help='learning rate (default: 0.05)')
    parser.add_argument('--workers', default=5, type=int,
                        help='number of data loading workers (default: 4)')
    parser.add_argument('--batch', default=1, type=int,
                        help='mini-batch size (default: 256)')
    parser.add_argument('--seed', type=int, default=31, help='random seed (default: 31)')
    return parser.parse_args()


start_token = 'G'
end_token = 'E'
batch_size = 16
datasets = './poem.txt'
seeds = 31
epoches = 200


def process_poems1(file_name):
    """

    :param file_name:
    :return: poems_vector  have tow dimmention ,first is the poem, the second is the word_index
    e.g. [[1,2,3,4,5,6,7,8,9,10],[9,6,3,8,5,2,7,4,1]]

    """
    poems = []
    with open(file_name, "r", encoding='utf-8', ) as f:
        for line in f.readlines():
            try:
                title, content = line.strip().split(':')
                # content = content.replace(' ', '').replace('，','').replace('。','')
                content = content.replace(' ', '')
                if '_' in content or '(' in content or '（' in content or '《' in content or '[' in content or \
                        start_token in content or end_token in content:
                    continue
                if len(content) < 5 or len(content) > 80:
                    continue
                content = start_token + content + end_token
                poems.append(content)
            except ValueError as e:
                print("error")
                pass
    # 按诗的字数排序
    poems = sorted(poems, key=lambda line: len(line))
    # print(poems)
    # 统计每个字出现次数
    all_words = []
    for poem in poems:
        all_words += [word for word in poem]
    counter = collections.Counter(all_words)  # 统计词和词频。
    count_pairs = sorted(counter.items(), key=lambda x: -x[1])  # 排序
    words, _ = zip(*count_pairs)
    words = words[:len(words)] + (' ',)
    word_int_map = dict(zip(words, range(len(words))))
    poems_vector = [list(map(word_int_map.get, poem)) for poem in poems]
    return poems_vector, word_int_map, words


def process_poems2(file_name):
    """
    :param file_name:
    :return: poems_vector  have tow dimmention ,first is the poem, the second is the word_index
    e.g. [[1,2,3,4,5,6,7,8,9,10],[9,6,3,8,5,2,7,4,1]]

    """
    poems = []
    with open(file_name, "r", encoding='utf-8', ) as f:
        # content = ''
        for line in f.readlines():
            try:
                line = line.strip()
                if line:
                    content = line.replace(' '' ', '').replace('，', '').replace('。', '')
                    if '_' in content or '(' in content or '（' in content or '《' in content or '[' in content or \
                            start_token in content or end_token in content:
                        continue
                    if len(content) < 5 or len(content) > 80:
                        continue
                    # print(content)
                    content = start_token + content + end_token
                    poems.append(content)
                    # content = ''
            except ValueError as e:
                # print("error")
                pass
    # 按诗的字数排序
    poems = sorted(poems, key=lambda line: len(line))
    # print(poems)
    # 统计每个字出现次数
    all_words = []
    for poem in poems:
        all_words += [word for word in poem]
    counter = collections.Counter(all_words)  # 统计词和词频。
    count_pairs = sorted(counter.items(), key=lambda x: -x[1])  # 排序
    words, _ = zip(*count_pairs)
    words = words[:len(words)] + (' ',)
    word_int_map = dict(zip(words, range(len(words))))
    poems_vector = [list(map(word_int_map.get, poem)) for poem in poems]
    return poems_vector, word_int_map, words


def generate_batch(batch_size, poems_vec, word_to_int):
    n_chunk = len(poems_vec) // batch_size
    x_batches = []
    y_batches = []
    for i in range(n_chunk):
        start_index = i * batch_size
        end_index = start_index + batch_size
        x_data = poems_vec[start_index:end_index]
        y_data = []
        for row in x_data:
            y = row[1:]
            y.append(row[-1])
            y_data.append(y)
        """
        x_data             y_data
        [6,2,4,6,9]       [2,4,6,9,9]
        [1,4,2,8,5]       [4,2,8,5,5]
        """
        # print(x_data[0])
        # print(y_data[0])
        # exit(0)
        x_batches.append(x_data)
        y_batches.append(y_data)
    return x_batches, y_batches


def run_training(dataset):
    poems_vector, word_to_int, vocabularies = process_poems2('./poem.txt')
    print("finish  loadding data")
    BATCH_SIZE = 100

    torch.manual_seed(seeds)
    word_embedding = rnn_lstm.word_embedding(vocab_length=len(word_to_int) + 1, embedding_dim=100)
    rnn_model = rnn_lstm.RNN_model(batch_sz=BATCH_SIZE, vocab_len=len(word_to_int) + 1, word_embedding=word_embedding,
                                   embedding_dim=100, lstm_hidden_dim=128)

    optimizer = optim.RMSprop(rnn_model.parameters(), lr=0.001)

    loss_fun = torch.nn.NLLLoss()
    for epoch in range(epoches):
        batches_inputs, batches_outputs = generate_batch(BATCH_SIZE, poems_vector, word_to_int)
        n_chunk = len(batches_inputs)
        for batch in range(n_chunk):
            batch_x = batches_inputs[batch]
            batch_y = batches_outputs[batch]  # (batch , time_step)

            loss = 0
            for index in range(BATCH_SIZE):
                x = np.array(batch_x[index], dtype=np.int64)
                y = np.array(batch_y[index], dtype=np.int64)
                x = Variable(torch.from_numpy(np.expand_dims(x, axis=1)))
                y = Variable(torch.from_numpy(y))
                if torch.cuda.is_available():
                    x = x.cuda()
                    y = y.cuda()
                pre = rnn_model(x)
                loss += loss_fun(pre, y)
                if index == 0:
                    _, pre = torch.max(pre, dim=1)
                    print('prediction',
                          pre.data.tolist())  # the following  three line can print the output and the prediction
                    print('b_y       ',
                          y.data.tolist())  # And you need to take a screenshot and then past is to your homework paper.
                    print('*' * 30)
            loss = loss / BATCH_SIZE
            print("epoch  ", epoch, 'batch number', batch, "loss is: ", loss.data.tolist())
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm(rnn_model.parameters(), 1)
            optimizer.step()

            if batch % 20 == 0:
                torch.save(rnn_model.state_dict(), './poem_generator_rnn')
                print("finish  save model")


def to_word(predict, vocabs):  # 预测的结果转化成汉字
    sample = np.argmax(predict)

    if sample >= len(vocabs):
        sample = len(vocabs) - 1

    return vocabs[sample]


def pretty_print_poem(poem):  # 令打印的结果更工整
    shige = []
    for w in poem:
        if w == start_token or w == end_token:
            break
        shige.append(w)
    poem_sentences = poem.split('。')
    for s in poem_sentences:
        if s != '' and len(s) > 2:
            print(s + '。')
    return poem_sentences


def gen_poem(begin_word, training_datasets):
    poems_vector, word_int_map, vocabularies = process_poems2(
            './poem.txt')  # use the other dataset to train the network
    word_embedding = rnn_lstm.word_embedding(vocab_length=len(word_int_map) + 1, embedding_dim=100)
    rnn_model = rnn_lstm.RNN_model(batch_sz=64, vocab_len=len(word_int_map) + 1, word_embedding=word_embedding,
                                   embedding_dim=100, lstm_hidden_dim=128)

    rnn_model.load_state_dict(torch.load('./poem_generator_rnn'))

    # 指定开始的字

    poem = begin_word
    word = begin_word
    while word != end_token:
        input = np.array([word_int_map[w] for w in poem], dtype=np.int64)
        input = Variable(torch.from_numpy(input))
        if torch.cuda.is_available():
            input = input.cuda()
        output = rnn_model(input, is_test=True)
        word = to_word(output.data.tolist()[-1], vocabularies)
        poem += word
        # print(word)
        # print(poem)
        if len(poem) > 30:
            break
    return poem


def main(args):
    time_file = open('time.txt', 'a+')
    localtime = time.asctime(time.localtime(time.time()))
    time_file.write('##################\n')
    time_file.write(datasets)
    time_file.write('\n')
    time_file.write(str(localtime))
    time_file.write('\n')
    run_training(datasets)

    localtime = time.asctime(time.localtime(time.time()))
    time_file.write(str(localtime))
    time_file.write('\n')

    word_list = ["春", "山", "夜", "爱"]

    for start_word in word_list:
        sentences = pretty_print_poem(gen_poem(start_word, datasets))
        time_file.write(sentences[0].split('E')[0])
        time_file.write('\n')


if __name__ == '__main__':
    args = parse_args()
    main(args)
