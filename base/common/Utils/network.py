#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright YYYY-     CompanyName
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Author: FirstName LastName <email@company.com>

import SSHLibrary
from robot.api import logger
import subprocess
import time
import re
from Utils.test_env import TestEnv


class Network(object):
    def __init__(self,host=None,username=None,password=None,port=None,alias=None,timeout=3):
        env = TestEnv()
        config = env.get_env_config('Json Name')
        self.testinput_ip = config.get('data') if host is None else host
        self.testinput_port = config.get('port_info') if port is None else port
        self.testinput_user = config.get('username') if username is None else username
        self.testinput_pw = config.get('passwd') if password is None else password
        self.ssh_testinput = SSHLibrary.SSHLibrary(loglevel="INFO",timeout=timeout)
        self.promote = '[>#]'
        self.alias = alias or "other_value"
    
    def set_testinput_info(self, ip, port, user, pwd , alias='default_value',promote='#'):
        self.testinput_ip = ip
        self.testinput_port = port
        self.testinput_user = user
        self.testinput_pw = pwd
        self.alias = alias
        self.promote = promote
    
    def __del__(self):
        try:
            self.ssh_testinput.close_all_connections()
        except:
            pass 
    
    def _login_testinput_cli(self,alias=None):
        alias = alias or self.alias
        self.ssh_testinput.open_connection(host=self.testinput_ip,port=self.testinput_port,alias=alias)
        try:
            self.ssh_testinput.login(self.testinput_user,self.testinput_pw)
            logger.info("Login into testinput with alias {0}".format(alias))
        except:
            logger.error("SSH Login {0} failed".format(self.testinput_ip))

    def login_testinput_cli(self,alias):
        conn = self.ssh_testinput.get_connection(alias)
        if conn.index is not None:
            self.ssh_testinput.switch_connection(alias)
            try:
                self.ssh_testinput.start_command("ls")
            except:
                logger.debug("SSH seesion is breaked")
                self._login_testinput_cli(alias)
        else:
            self._login_testinput_cli(alias)

    def __get_ping_by_cmd__(self,host,srcaddr = None):
        ret = False
        if srcaddr == None:
            cmd_ping = 'ping {0}'.format(host)
        else:
            cmd_ping = 'ping -S {0} {1}'.format(srcaddr, host)
        try:
            sub = subprocess.Popen(cmd_ping,stderr=subprocess.STDOUT,shell=True,stdout=subprocess.PIPE)
            ot = sub.communicate(timeout=5)[0]
            cmd_r = ot.decode("gbk", errors='replace').encode().decode('utf-8', errors='replace')
        except:
            cmd_r = ''
        if 'TTL=' in cmd_r:
            ret = True
        return ret,''
        
    def get_ping_status(self,host,srcaddr=None,timeout=60):
        end = timeout // 10 + 5
        for i in range(0,end):
            st = self.__get_ping_by_cmd__(host, srcaddr)[0]
            if i == end - 1:
                return False
        return st

    def check_ping(self, host, exp=True, srcaddr=None, timeout=60):
        ret = None
        end = timeout // 3 + 1
        for i in range(0,end):
            st = self.__get_ping_by_cmd__(host, srcaddr)[0]
            if st == exp:
                ret = True
                logger.info("check ping ({0}) success [{1}].".format(host,exp))
                break
            elif i == end - 1:
                ret = False
                msg = "check ping ({0}) fail [{1}].".format(host,exp)
                logger.error(msg)
                raise AssertionError(msg)
             
            time.sleep(3)
        return ret      

    def send_ssh_command(self,command,alias=None,ret=True):
        """Send SSH Command to SSH session

        :param command: command line. eg: CompanyName_info.sh
        :param alias: default is testinput_cli, if you want another alias please specia
        :param ret: default is True to return string.
        :return: string, or None depend on `ret` parameter

        Example:
        self.send_ssh_command('processName -W',ret=False)

        Example:
        | Send SSH Command   |  processName -W        | ret=${False}   |
        | ${s}=              |  Send SSH Command    |  CompanyName_info  |
        """

        alias = alias or self.alias
        self.login_testinput_cli(alias)
        if ret == True:
            self.ssh_testinput.set_client_configuration(timeout='3 seconds')
            self.ssh_testinput.start_command(command)
            return self.ssh_testinput.read_command_output()
        else:
            self.ssh_testinput.set_client_configuration(timeout='120 seconds')
            self.ssh_testinput.write(command)
            return None
    
    def get_session_output(self,stopflag=True,alias=None):
        """ Return the output by alias which you have used send_ssh_command without return

        :param stopflag: defaul is True, Flag to whether stop here to collect the logs with this session
        :param alias: Alias name for ssh seesion which you want to get the output.
        
        Example:
        self.send_ssh_command('processName -W',ret=False)
        time.sleep(5)
        s =  self.get_session_output(stopflag=False)

        Example:
        | Send SSH Command   |  processName -W        | ret=${False} |
        | Sleep              |  5s                  |
        | ${s}=              |  Get Session Output  |
        | ${s}=              |  Get Session Output  | stopflag=${False}
        """
        alias = alias or self.alias
        conn = self.ssh_testinput.get_connection(alias)
        if conn.index is None:
            logger.info("There is no output for this session {0}".format(alias))
            return ''
        else:
            if stopflag == True:
                self.ssh_testinput.write(chr(int(3))) # Ctrl + c
                return self.ssh_testinput.read_until(self.promote,'INFO')
            else:
                return self.ssh_testinput.read("DEBUG")
    
    def get_ssh_file(self,source,destination="."):
        """Downloads file(s) from the remote machine to the local machine.

        ``source`` is a path on the remote machine. Both absolute paths and
        paths relative to the current working directory are supported.
        If the source contains wildcards explained in `glob patterns`,
        all files matching it are downloaded. In this case ``destination``
        must always be a directory.

        ``destination`` is the target path on the local machine. Both
        absolute paths and paths relative to the current working directory
        are supported.
        """
        self._login_testinput_cli()
        return self.ssh_testinput.get_file(source,destination)
    
    def get_ssh_directory(self, source, destination='.', recursive=False):
        """Downloads a directory, including its content, from the remote machine to the local machine.

        ``source`` is a path on the remote machine. Both absolute paths and
        paths relative to the current working directory are supported.

        ``destination`` is the target path on the local machine.  Both
        absolute paths and paths relative to the current working directory
        are supported.

        ``recursive`` specifies whether to recursively download all
        subdirectories inside ``source``. Subdirectories are downloaded if
        the argument value evaluates to true (see `Boolean arguments`)."""
        self._login_testinput_cli()
        return self.ssh_testinput.get_directory(source,destination,recursive)
    
    def put_ssh_file(self, source, destination='.', mode='0744', newline=''):
        """Uploads file(s) from the local machine to the remote machine.

        ``source`` is the path on the local machine. Both absolute paths and
        paths relative to the current working directory are supported.
        If the source contains wildcards explained in `glob patterns`,
        all files matching it are uploaded. In this case ``destination``
        must always be a directory.

        ``destination`` is the target path on the remote machine. Both
        absolute paths and paths relative to the current working directory
        are supported.

        ``mode`` can be used to set the target file permission.
        Numeric values are accepted. The default value is ``0744``
        (``-rwxr--r--``).

        ``newline`` can be used to force the line break characters that are
        written to the remote files. Valid values are ``LF`` and ``CRLF``."""
        self._login_testinput_cli()
        return self.ssh_testinput.put_file(source,destination,mode,newline)

    def put_ssh_directory(self, source, destination='.', mode='0744', newline='',
                      recursive=False):
        """Uploads a directory, including its content, from the local machine to the remote machine.

        ``source`` is the path on the local machine. Both absolute paths and
        paths relative to the current working directory are supported.

        ``destination`` is the target path on the remote machine. Both
        absolute paths and paths relative to the current working directory
        are supported.

        ``mode`` can be used to set the target file permission.
        Numeric values are accepted. The default value is ``0744``
        (``-rwxr--r--``).

        ``newline`` can be used to force the line break characters that are
        written to the remote files. Valid values are ``LF`` and ``CRLF``.

        ``recursive`` specifies whether to recursively upload all
        subdirectories inside ``source``. Subdirectories are uploaded if the
        argument value evaluates to true (see `Boolean arguments`)."""
        self._login_testinput_cli()
        return self.ssh_testinput.put_directory(source,destination,mode,newline,recursive)

    @property
    def ssh_object(self):
        """ Return the SSH object to invoke more function if you needed
        pelase check page for more function which provide by:
        [https://github.com/robotframework/SSHLibrary]
        :return: ssh object
        """
        self._login_testinput_cli()
        return self.ssh_testinput
    
if __name__ == '__main__':
    x = Network()

    # s = x.send_ssh_command('CompanyNameinfo.sh')
    # print(s)

    # x.send_ssh_command('top',ret=False)
    # time.sleep(5)
    # s =  x.get_session_output()
    # print(s)

    # x.send_ssh_command('processName -W',ret=False)
    # time.sleep(5)
    # s =  x.get_session_output(stopflag=False)
    # print(s)

    # print(x.ssh_object)

    s = x.check_ping("10.22.33.44")
    print(s)
              
