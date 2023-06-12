import json

import os
from pathlib import Path
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
import pandas as pd

from trafficflowprediction import utils
from trafficflowprediction.forms import CarInfoForm
from trafficflowprediction.models import CarInfo


def other(request):
    return render(request, 'trafficflowprediction/other.html')


def index(request):
    return render(request, 'trafficflowprediction/base.html')


class Upload(View):
    current = 0

    def get(self, request):
        exist = request.GET.get('getProgressNum')
        if exist:
            # print(Upload.current)  # debug
            return HttpResponse(Upload.current)
        else:
            return render(request, 'trafficflowprediction/upload.html')

    def post(self, request):
        # 读取文件内容，保存数据库
        file = request.FILES.get('file_obj')
        response = {'status': 200, 'msg': None}
        data = pd.DataFrame(pd.read_excel(file))
        total = data.shape[0]
        data.fillna(0, inplace=True)
        for index2, row in data.iterrows():
            Upload.current = int(index2 / total * 100)
            # print(Upload.current)
            car = CarInfo(lane_name=row['车道名称'], lane_code=row['车道代码'], time=row['时间'],
                          car_type=row['车型'], speed=row['车速（km/h）'], car_length=row['车长（cm)'],
                          axles=row['轴数（根)'], total_weight=row['总重（kg）'], axle1_weight=row['轴重1（kg）'],
                          axle2_weight=row['轴重2（kg）'], axle3_weight=row['轴重3（kg）'], axle4_weight=row['轴重4（kg）'],
                          axle5_weight=row['轴重5（kg）'], axle6_weight=row['轴重6（kg）'], axle7_weight=row['轴重7（kg）'],
                          axle8_weight=row['轴重8（kg）'], axle9_weight=row['轴重9（kg）'], axle10_weight=row['轴重10（kg）'],
                          overload=row['超重'], overspeed=row['超速'], state=row['状态'])
            car.save()
        response['msg'] = "文件上传成功"
        return JsonResponse(response, safe=False)


class CustomerPaginator(Paginator):
    """
    继承Paginator类，用于保留原有功能、并扩展新的功能
    """

    def __init__(self, current_page, per_pager_num, *args, **kwargs):
        super(CustomerPaginator, self).__init__(*args, **kwargs)
        self.current_page = int(current_page)  # 当前页码
        self.per_page_num = int(per_pager_num)  # 分页自定制显示最多页码个数

    def pager_num_range(self):
        '''
        CustomerPaginator自定制新功能：显示分页页码
        :return:
        '''
        if self.num_pages < self.per_page_num:
            # 当数据的总页码数<自定制的每页显示分页页码数时，显示：1到总页码数
            return range(1, self.num_pages + 1)

        # 自定制每页显示页码数/2，取整，主要是想当前页码显示在页码中央：
        part = int(self.per_page_num / 2)

        if self.current_page <= part:
            # 如果当前页码小于自定制每页显示页码数的一半
            return range(1, self.per_page_num + 1)

        if self.current_page + part > self.num_pages:
            # 如果当前页码加上自定制每页显示页码数的一半,大于总页码数：
            return range(self.num_pages - self.per_page_num + 1, self.num_pages + 1)
        # 在上面的极端值情况后，常规情况是取当前页前后-+part范围
        return range(self.current_page - part, self.current_page + part + 1)


def show(request, p):
    stu_list = CarInfo.objects.all()

    current_page = int(p)
    # 由于上面使用CustomerPaginator继承了Paginator，所以这里使用CustomerPaginator实例化，
    # 传入4个参数：当前页码、每页显示页码个数、全部数据、每页显示数据条数
    paginator = CustomerPaginator(current_page, 10, stu_list, 14)

    try:
        # page对象
        posts = paginator.page(current_page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "trafficflowprediction/show.html", {"posts": posts})


class Detail(DetailView):
    model = CarInfo
    template_name = 'trafficflowprediction/detail.html'


class Update(UpdateView):
    form_class = CarInfoForm
    model = CarInfo
    template_name = 'trafficflowprediction/update.html'
    success_url = reverse_lazy('trafficflowprediction:show', kwargs={'p': 1})


class Delete(DeleteView):
    model = CarInfo
    template_name = 'trafficflowprediction/delete.html'
    success_url = reverse_lazy('trafficflowprediction:show', kwargs={'p': 1})


class Clean(View):

    def my_custom_sql(self, sql):
        before = CarInfo.objects.all().count()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
        after = CarInfo.objects.all().count()
        return before - after

    def get(self, request):
        return render(request, 'trafficflowprediction/clean.html')

    def post(self, request):
        # 1、获取前端用户提交的清洗数据规则
        # value = request.POST.get('car_length')
        # value2 = request.POST.get('speed')
        value3 = request.POST.get('axles')
        value4 = request.POST.get('car_type')
        value5 = request.POST.get('overload')
        value6 = request.POST.get('overspeed')
        value7 = request.POST.get('state')

        # 2、对数据库数据进行操作
        sql = 'DELETE FROM trafficflowprediction_carinfo WHERE car_length is null OR speed is null'

        if value3 == '考虑':
            sql = sql + " OR axles is null"
        if value4 != 'none':
            sql = sql + " OR car_type=='" + value4 + "'"
        if value5 != 'none':
            sql = sql + " OR overload=='" + value5 + "'"
        if value6 != 'none':
            sql = sql + " OR overspeed=='" + value6 + "'"
        if value7 != 'none':
            sql = sql + " OR state=='" + value7 + "'"

        # raw()处理的是select语句；update，delete，insert不能采取这种方式
        # res = CarInfo.objects.raw(sql)
        res = self.my_custom_sql(sql)
        # data = {'result': res}
        # 3、前端返回清洗成功提示
        return render(request, 'trafficflowprediction/success.html', {'result': json.dumps(res)})


class Prediction(View):

    def process_data(self, direction, minutes=5):
        """
        处理数据库数据，取数据库某一天的数据，进行预测
        :param minutes: 间隔
        :param direction: 上行或者下行
        :return:none
        """
        temp = '上'
        if direction == 'down':
            temp = '下'
        car_list = CarInfo.objects.all()
        l = []  # 存放时间这一列的数据
        for item in car_list:
            if item.lane_name[0] != temp:
                continue
            l.append(item.time)
        l.sort()

        time_sequence, cnts = [], []
        # 统计每5分钟的车辆数
        # 一天是288个5分钟
        # 得到该文件的第一天
        firstdate = str(l[0][0:l[0].find(' ')])
        intervals = []  # 时间区间，长度：288
        str2 = '{:0>2d}:{:0>2d}:00.0'
        for hour in range(24):
            for minute in range(0, 60, int(minutes)):
                intervals.append(str2.format(hour, minute))
        intervals.append(str2.format(24, 0))
        start = 0
        while start < len(l):
            for j in range(1, len(intervals)):
                cnt = 0
                for i in range(start, len(l)):
                    blankindex = l[i].find(' ')
                    if l[i][0:blankindex] != firstdate:
                        start = i
                        time_sequence.append(firstdate + ' ' + intervals[j - 1])
                        cnts.append(cnt)
                        break
                    if l[i][blankindex + 1:] < intervals[j]:
                        cnt += 1
                        if i + 1 == len(l):
                            start = i + 1
                            time_sequence.append(firstdate + ' ' + intervals[j - 1])
                            cnts.append(cnt)
                            break
                    else:
                        start = i
                        time_sequence.append(firstdate + ' ' + intervals[j - 1])
                        cnts.append(cnt)
                        break
            # 下一天
            if start < len(l):
                firstdate = l[start][0:l[start].find(' ')]

        dataframe = pd.DataFrame({minutes + ' Minutes': time_sequence, 'Flow': cnts})
        path = os.getcwd() + "\\trafficflowprediction\\data\\" + minutes + '_' + direction + ".csv"
        dataframe.to_csv(path, index=False)


    def get(self, request):
        return render(request, 'trafficflowprediction/prediction.html')

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
