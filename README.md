####  README

- 生成当前项目的requirements.txt

  ```
  # https://www.cnblogs.com/wangyuxing/p/11162232.html
  # pip install pipreqs
  # pipreqs\pipreqs.py 文件121行修改encoding="utf-8"
  # 命令：pipreqs ./
  ```

- 源码修改

  1. ddt.py

     - 参考：<https://www.cnblogs.com/huwang-sun/p/11201907.html> 

     ```python
     def mk_test_name(name, value, index=0):
         # 注释的源码部分
         # index = "{0:0{1}}".format(index + 1, index_len)
         # if not is_trivial(value):
         #     return "{0}_{1}".format(name, index)
         # try:
         #     value = str(value)
         # except UnicodeEncodeError:
         #     # fallback for python2
         #     value = value.encode('ascii', 'backslashreplace')
         # test_name = "{0}_{1}_{2}".format(name, index, value)
         # return re.sub(r'\W|^(?=\d)', '_', test_name)
     
         # 如果数据是list，则获取字典当中第一个数据作为测试用例名称   添加部分:129-
         if type(value) is dict:
             try:
                 value = value["用例ID"] + value["接口名称"]
             except:
                 return "{0}_{1}".format(name, index)
         try:
             value = str(value)
         except UnicodeEncodeError:
             # fallback for python2
             value = value.encode('ascii', 'backslashreplace')
         test_name = "{0}_{1}_{2}".format(name, index, value)
         return re.sub(r'\W|^(?=\d)', '_', test_name)
     ```

     

  2. HTMLTestRunner.py

     - 参考：<https://www.cnblogs.com/captainmeng/p/7736949.html> 
     - 参考：<https://www.jianshu.com/p/c5b1df72acfa> 

     ```python
     class _TestResult(TestResult):
         # note: _TestResult is a pure representation of results.
         # It lacks the output and reporting ability compares to unittest._TextTestResult.
     
         # 显示打印信息，修改第一处
         # def __init__(self, verbosity=1):
         def __init__(self, verbosity=2):
             TestResult.__init__(self)
             self.stdout0 = None
             self.stderr0 = None
             self.success_count = 0
             self.failure_count = 0
             self.error_count = 0
             self.verbosity = verbosity
     
             # result is a list of result in 4 tuple
             # (
             #   result code (0: success; 1: fail; 2: error),
             #   TestCase object,
             #   Test output (byte string),
             #   stack trace,
             # )
             self.result = []
     ```

     

     ```python
     class HTMLTestRunner(Template_mixin):
         """
         """
         # 显示打印信息，修改第二处
         # def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
         def __init__(self, stream=sys.stdout, verbosity=2, title=None, description=None):
             self.stream = stream
             self.verbosity = verbosity
             if title is None:
                 self.title = self.DEFAULT_TITLE
             else:
                 self.title = title
             if description is None:
                 self.description = self.DEFAULT_DESCRIPTION
             else:
                 self.description = description
     
             self.startTime = datetime.datetime.now()
     
         # 控制台显示日志信息，用例的名称
         # def run(self, test):
         def run(self, test, verbosity):
             "Run the given test case or test suite."
             # result = _TestResult(self.verbosity)
             result = _TestResult(verbosity)
             test(result)
             self.stopTime = datetime.datetime.now()
             self.generateReport(test, result)
             # print(sys.stderr, '\nTimeElapsed: %s' % (self.stopTime-self.startTime))
             sys.stderr.write('\nTime Elapsed: %s\n' % (self.stopTime - self.startTime))
             return result
     ```

     

     ```python
         def _generate_report_test(self, rows, cid, tid, n, t, o, e):
             # e.g. 'pt1.1', 'ft1.1', etc
             has_output = bool(o or e)
             tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid+1,tid+1)
             name = t.id().split('.')[-1]
             doc = t.shortDescription() or ""
             desc = doc and ('%s: %s' % (name, doc)) or name
             tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL
     
             # o and e should be byte string because they are collected from stdout and stderr?
     
             # 注释掉一下信息，为了报告中显示打印信息
             # if isinstance(o,str):
             #     # TODO: some problem with 'string_escape': it escape \n and mess up formating
             #     # uo = unicode(o.encode('string_escape'))
             #     uo = e
             # else:
             uo = o
             if isinstance(e,str):
                 # TODO: some problem with 'string_escape': it escape \n and mess up formating
                 # ue = unicode(e.encode('string_escape'))
                 ue = e
             else:
                 ue = e
     ```

     - 解决报错：<_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>  

  

