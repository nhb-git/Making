#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：7/15/2020  1:41 PM 
# 文件名称   ：HouseStark.py


class ArgvHandle:
    def __init__(self, argv_list):
        self.argvs = argv_list
        self.parse_argv()

    def parse_argv(self):
        if len(self.argvs) > 1:
            self.argvs[1] if hasattr(self, self.argvs[1]) else self.help_msg()
        else:
            self.help_msg()

    def help_msg(self):
        msg = '''
            collect_data
            run_forever
            get_assert_id
            report_assert
        '''
        print(msg)

    def collect_data(self):
        obj = info_collection.InfoCollection()
        assert_data = obj.collect()
