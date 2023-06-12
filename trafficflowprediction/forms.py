from django import forms

from trafficflowprediction.models import CarInfo


class CarInfoForm(forms.ModelForm):
    # 配置中心，修改关于CSS的内容
    class Meta:
        model = CarInfo
        fields = '__all__'  # 验证所有字段

        widgets = {
            'lane_name': forms.TextInput(attrs={'class': 'form-control'}),
            'lane_code': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.TextInput(attrs={'class': 'form-control'}),
            'car_type': forms.TextInput(attrs={'class': 'form-control'}),
            'speed': forms.NumberInput(attrs={'class': 'form-control'}),
            'car_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'axles': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle1_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle2_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle3_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle4_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle5_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle6_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle7_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle8_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle9_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'axle10_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'overload': forms.TextInput(attrs={'class': 'form-control'}),
            'overspeed': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'lane_name': '车道名称',
            'lane_code': '车道代码',
            'time': '时间',
            'car_type': '车型',
            'speed': '速度',
            'car_length': '车长',
            'axles': '轴数',
            'total_weight': '总重',
            'axle1_weight': '轴重1',
            'axle2_weight': '轴重2',
            'axle3_weight': '轴重3',
            'axle4_weight': '轴重4',
            'axle5_weight': '轴重5',
            'axle6_weight': '轴重6',
            'axle7_weight': '轴重7',
            'axle8_weight': '轴重8',
            'axle9_weight': '轴重9',
            'axle10_weight': '轴重10',
            'overload': '超重',
            'overspeed': '超速',
            'state': '状态',
        }
