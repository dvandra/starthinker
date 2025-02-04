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

accountUserProfilesListResponse_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "nextPageToken"
  }, 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "kind"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "subaccountId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "name"
      }, 
      [
        {
          "fields": {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "objectIds"
          }, 
          "type": "RECORD", 
          "name": "objectIds", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "ALL, ASSIGNED, NONE", 
          "name": "status"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "locale"
      }, 
      [
        {
          "fields": {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "objectIds"
          }, 
          "type": "RECORD", 
          "name": "objectIds", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "ALL, ASSIGNED, NONE", 
          "name": "status"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "comments"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "id"
      }, 
      [
        {
          "fields": {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "objectIds"
          }, 
          "type": "RECORD", 
          "name": "objectIds", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "ALL, ASSIGNED, NONE", 
          "name": "status"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }
      ], 
      [
        {
          "fields": {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "objectIds"
          }, 
          "type": "RECORD", 
          "name": "objectIds", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "ALL, ASSIGNED, NONE", 
          "name": "status"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "userRoleId"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "INTERNAL_ADMINISTRATOR, NORMAL_USER, READ_ONLY_SUPER_USER, SUPER_USER", 
        "name": "userAccessType"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "EXTERNAL_TRAFFICKER, INTERNAL_NON_TRAFFICKER, INTERNAL_TRAFFICKER", 
        "name": "traffickerType"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "active", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "", 
        "name": "email"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "accountId"
      }
    ], 
    "type": "RECORD", 
    "name": "accountUserProfiles", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }
]
