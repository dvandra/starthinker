###########################################################################
# 
#  Copyright 2018 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################


"""Command line to run all tests or list all runnable tests.

Meant to speed up an automate testing of StarThinker.

To get list: python test/helper.py --list -u [credentials] -s [credentials] -p [project_id]

"""


import os
import sys
import re
import argparse
import subprocess

from starthinker.config import UI_ROOT, UI_SERVICE, UI_PROJECT

UI_CLIENT = os.environ.get('STARTHINKER_CLIENT_INSTALLED', 'MISSING RUN deploy.sh TO SET')
UI_USER = os.environ.get('STARTHINKER_USER', 'MISSING RUN deploy.sh TO SET')

RE_TEST = re.compile(r'test.*\.json')

if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--list', help='list tests.', action='store_true')
  args = parser.parse_args()

  for root, dirs, files in os.walk(UI_ROOT + '/starthinker/'):
    for filename in files:
      if RE_TEST.match(filename) and '/project/' not in root:

        if args.list:
          print '%s/%s' % (root, filename)

        else:
          command = 'python %s/starthinker/all/run.py %s/%s -c %s -u %s -s %s -p %s --force' % (
            UI_ROOT,
            root,
            filename,
            UI_CLIENT,
            UI_USER,
            UI_SERVICE,
            UI_PROJECT
          )

          print ''
          print ''
          print '----------------------------------------'
          print ' TEST: ', command
          print '----------------------------------------'
          print ''

          subprocess.call(command, shell=True, stderr=subprocess.STDOUT)
