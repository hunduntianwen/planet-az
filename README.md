## 安装说明
安装python 3.6+
使用pip安装以下包
```
pip install prettytable  
pip install PyYAML  
pip install numpy  
pip install ephem  
pip install matplotlib  
```

## 使用方法

```
python planet_az.py -c config.yaml
```

运行后弹出绘图窗口, 控制台会输出行星方位信息，每隔5秒刷新。

在控制台ctrl+c关闭程序

## 配置文件
observer 填写观察者的经纬度，海拔，压强  
stars 填写自定义天体，可填多个