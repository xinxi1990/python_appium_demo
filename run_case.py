#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import os
import subprocess
import unittest
from appium import webdriver
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait


class AppiumServer:
    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout

    def start_server(self):
        self.stop_server()
        cmd = "appium --session-override -a %s -p %s" % (self.host, self.port)
        appium_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                          close_fds=True)

        print("启动appium命令:{}".format(cmd))
        is_start = False
        start_time = time.time()
        while not is_start and (time.time() - start_time) < float(self.timeout):
            appium_line = appium_process.stdout.readline().strip().decode()
            time.sleep(1)
            print("---------启动服务中----------")
            if 'listener started' in appium_line:
                print("---------启动服务成功----------")
                is_start = True
        return is_start


    def stop_server(self):
        cmd = "lsof -i:%s" % self.port
        plist = os.popen(cmd).readlines()
        if len(plist) > 1:
            line = plist[1]
            temp_line = line.split("    ")[1]
            temp_pid = temp_line.split(" ")[0]
            os.popen("kill -9 %s" % temp_pid)


class TestAppium(unittest.TestCase):

    loaded = False

    def setUp(self):
        print("setup")
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "demo"
        caps["appPackage"] = "com.dedao.juvenile"
        caps["appActivity"] = "com.dedao.juvenile.business.splash.SplashActivity"
        caps["autoGrantPermissions"] = "true"
        caps["automationName"] = "UiAutomator2"

        if TestAppium.loaded == True:
            caps["noReset"] = "true"

        self.driver = webdriver.Remote("http://127.0.0.1:4724/wd/hub", caps)
        self.driver.implicitly_wait(10)
        loaded = True

    def test_run(self):

        print('==========test_run========>')



if __name__ == '__main__':
    appium_server = AppiumServer("127.0.0.1", "4724", "10")
    if not appium_server.start_server():
        raise StartServerTimeout("在指定时间{}秒内未能启动appium server，请手动检查".format("10"))
    unittest.main()