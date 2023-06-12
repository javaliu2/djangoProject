import argparse
import os

import numpy as np
import pandas as pd
import torch
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from torch import nn
import matplotlib as mpl


class Data_processer:
    def __init__(self, test_file, lag):
        self.test_file = test_file
        self.lag = lag

        self.scaler = MinMaxScaler(feature_range=(0, 1))
        attr = "Flow"
        df = pd.read_csv(self.test_file, encoding="utf-8").fillna(0)
        self.scaler.fit(df[attr].values.reshape(-1, 1))

    def get_Dataset(self):
        print("Generating test dataset...")

        attr = "Flow"
        df = pd.read_csv(self.test_file, encoding="utf-8").fillna(0)

        flow = self.scaler.transform(df[attr].values.reshape(-1, 1)).reshape(1, -1)[0, :]

        testset = []
        for i in range(self.lag, len(flow)):
            testset.append(flow[i - self.lag:i + 1])

        testset = np.array(testset, dtype=np.float32)

        testX = torch.from_numpy(testset[:, :-1])
        testY = torch.from_numpy(testset[:, -1]).unsqueeze(1)

        print("Done.")

        return testX, testY


class MyLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout=0):
        super(MyLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers,
                            dropout=dropout, batch_first=True)
        self.linear = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        hn = hn[-1, :, :]
        return self.sigmoid(self.linear(hn))

    def mse(self, real, prediction):
        return np.round(np.mean((prediction - real) ** 2), 2)

    def rmse(self, real, prediction):
        return np.round(np.sqrt(np.mean((prediction - real) ** 2)), 2)

    def mape(self, real, prediction):
        return np.around(np.mean(np.abs((prediction - real) / real)) * 100, 2)

    def smape(self, real, prediction):
        return np.around(np.mean(2 * np.abs(prediction - real) / (np.abs(real) + np.abs(prediction))) * 100, 2)

    def mae(self, real, prediction):
        return np.round(np.mean(np.abs(prediction - real)), 2)


def get_parsers():
    parser = argparse.ArgumentParser()

    # parser.add_argument('--mode', default="train", help="train/test")
    parser.add_argument('--mode', default="test", help="train/test")
    parser.add_argument('--epoch', default=150, type=int)
    parser.add_argument('--batch_size', default=256, type=int)
    parser.add_argument('--lr', default=0.001, type=float)
    parser.add_argument('--time_lag', default=6, type=int)
    parser.add_argument('--hidden_size', default=64, type=int)
    parser.add_argument('--num_layers', default=3, type=int)

    return parser.parse_args(args=[])


class Prediction:

    def __init__(self, direction, internal):
        self.direction = direction
        self.internal = internal
        self.data = os.getcwd() + '\\trafficflowprediction\\data\\' + internal + '_' + direction + '.csv'
        self.model = os.getcwd() + '\\trafficflowprediction\\model\\' + internal + '_' + direction

    def predicte(self):
        args = get_parsers()
        lstm = MyLSTM(1, args.hidden_size, args.num_layers)
        data = Data_processer(self.data, args.time_lag)
        testX, testY = data.get_Dataset()

        lstm.load_state_dict(torch.load(self.model, map_location='cpu'))

        x = testX[:, :].unsqueeze(2)
        y_predict = lstm(x)
        y_label = testY
        y_predict = y_predict.detach().cpu().numpy()
        y_label = y_label.numpy()
        y_predict = data.scaler.inverse_transform(y_predict).reshape(1, -1)[0, :]
        y_label = data.scaler.inverse_transform(y_label).reshape(1, -1)[0, :]

        rmse = lstm.rmse(y_label, y_predict)

        mape = lstm.mape(y_label, y_predict)

        mae = lstm.mae(y_label, y_predict)

        # 绘图
        F = plt.figure()
        fig = F.add_subplot(111)

        t = len(y_label)
        x_index = pd.date_range('2016-06-01 00:00', periods=t, freq=self.internal + 'min')[args.time_lag:]
        fig.plot(x_index, y_label[:len(x_index)], linestyle='-', linewidth=1, color="red", label="真实值")
        fig.plot(x_index, y_predict[:len(x_index)], linestyle='-', linewidth=1, color="blue", label="预测值")

        plt.xlabel("时间(分钟)")
        plt.ylabel("交通量(车/" + self.internal + "分钟)")
        plt.legend()

        fig.xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))

        # 不能正确显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        path = os.getcwd() + "/trafficflowprediction/static/trafficflowprediction/img/" + self.internal + '_' \
               + self.direction + ".png"
        plt.savefig(path)
        plt.show()
        return {'rmse': rmse, 'mape': mape, 'mae': mae}
