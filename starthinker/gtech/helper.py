###########################################################################
# 
#  Copyright 2019 Google Inc.
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


"""Evaluate the validity of a json file. Helps in debugging recipes.

Print the line and character position of any errors in the given json file.

Arguments

  file - path to JSON file to be evaluated

Example 

  python project/helper.py project/sample.json

"""


import argparse

from starthinker.util.project import get_project


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('file', help='A JSON file.')
  parser.add_argument('--debug', '-d', help='Debug mode, do not scrub newlines.', action='store_true')
  args = parser.parse_args()

  try:
    project = get_project(args.file, debug=args.debug)
    print 'JSON OK:', args.file
  except Exception, e:
    print 'JSON ERROR:', args.file, str(e)
