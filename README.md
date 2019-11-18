####  README

- 生产requirements.txt

  ```
  # https://www.cnblogs.com/wangyuxing/p/11162232.html
  # pip install pipreqs
  # pipreqs\pipreqs.py 文件121行修改encoding="utf-8"
  # 命令：pipreqs ./
  ```

- callback执行过程分解

  ```python
  def call_back(done):
      pre_execs = checkOrder
      res_more = dict()
      if checkOrder:
          for pre_exec in eval(pre_execs):
              checkOrder = Data(case_file, sheet_name).get_case_pre(pre_exec)
              res = call_back(checkOrder)
  
              def call_back(checkOrder):
                  checkOrder = case[data_key.pre_exec]
                  res_more = dict()
                  if pre_execs:
                      for pre_exec in eval(pre_execs):
                          checkOrder = Data(case_file, sheet_name).get_case_pre(pre_exec)
                          res = call_back(checkOrder)
  
                          def call_back(checkOrder):
                              goods_detail = case[data_key.pre_exec]
                              res_more = dict()
                              if pre_execs:
                                  for pre_exec in eval(pre_execs):
                                      goods_detail = Data(case_file, sheet_name).get_case_pre(pre_exec)
                                      res = call_back(goods_detail)
  
                                      def call_back(goods_detail):
                                          pre_execs = None
                                          res_more = dict()
                                          return run_pre(case)
  
                                      res_more[pre_exec] = res
                                  return func(goods_detail, res_more)
  
                          res_more[pre_exec] = res
                      return func(checkOrder, res_more)
  
              res_more[pre_exec] = res
          return func(done, res_more)
      return run_pre(case)
  ```

  

