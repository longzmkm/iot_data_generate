#iot data generate
###MQTT 协议学习 publish 中上传数据
#### ***payload datas 中的数据定义***
+ datatype = 1
```
    {
        key：value
    }
```
+ datatype = 2 (timestemp 格式 yyyy-mm-dd hh:mm:ss)
```
    {
        key:{timestemp：value}
    }
```
+ datatype = 3 (timestemp 格式 yyyy-mm-dd hh:mm:ss, ,dt是可选字段)
```
    [
        {
            apitag : key,
            "datapoints":[dt:timestemp , "value": value]
        }
    ]
```