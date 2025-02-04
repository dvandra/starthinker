#!/usr/bin/env python

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

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

REQUIREMENTS = [
  'google-cloud-core==0.24.1',
  'google-cloud-bigquery==0.25.0',
  'google-cloud-storage==1.2.0',
  'google-cloud-pubsub',
  'google-auth',
  'google-auth-httplib2',
  'google-api-python-client',
  'oauth2client',
  'httplib2',
  'jsonpickle',
  'pysftp',
  'pytz',
  'tzlocal',
  'TwitterAPI',
  'python-dateutil',
  'django==1.11',
  'pandas',
  'psutil',
]

#TEST_REQUIREMENTS = []

setup(
  name='starthinker',
  version='0.0.8',
  description="StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components.",
  long_description="StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components. To make it easier for partners and clients to work with some of our advertsing solutions, the gTech team has open sourced this framework as a reference implementation.  Our goal is to make managing data workflows using Google Cloud as fast and re-usable as possible, allowing teams to focus on building advertising solutions.",
  author="Paul Kenjora & Mauricio Desidario",
  author_email='kenjora@google.com',
  url='https://github.com/google/starthinker',
  packages=find_packages(),
  package_dir={'starthinker':
               'starthinker'},
  include_package_data=True,
  install_requires=REQUIREMENTS,
  license="Apache License, Version 2.0",
  zip_safe=False,
  keywords='starthinker',
  classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache License',
      'Natural Language :: English',
      "Programming Language :: Python :: 2",
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
  ],
  #test_suite='tests',
  #tests_require=TEST_REQUIREMENTS,
)
