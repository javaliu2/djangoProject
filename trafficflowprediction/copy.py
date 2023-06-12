def post(self, request):
    direction = request.POST.get('direction')
    internal = request.POST.get('internal')
    # 处理数据，将结果保存在/data/data_{{internal}}.csv文件
    self.process_data(direction, internal)
    # 根据direction和internal调用不同的模型
    p = utils.Prediction(direction, internal)
    loss = p.predicte()
    # 将预测得到的图片以及指标发送给前端
    pic = 'trafficflowprediction/img/' + internal + '_' + direction + '.png'
    return render(request, 'trafficflowprediction/prediction_show.html', {'img': pic, 'loss': loss})