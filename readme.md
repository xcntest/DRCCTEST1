一、前言

本框架采用Pytest+Allure+Requests实现，run.py为主运行文件，共实现以下三个功能：

1.爬取yapi接口文档生成测试用例数据yaml模板

2.编辑测试数据yaml模板，自动生成case_suite的py文件

3.调用核心装饰器方法@call_case读取用例数据执行用例并断言

其它功能：
	yaml用例数据文件中需要通过调用函数生成的数据，采用了自定义替换模板来执行函数并替换字符

二、框架结构
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210317163919618.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3RvdG9yb2JpZw==,size_16,color_FFFFFF,t_70#pic_center)
三、处理流程
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021031716572921.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3RvdG9yb2JpZw==,size_16,color_FFFFFF,t_70#pic_center)

