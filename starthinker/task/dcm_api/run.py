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

import re

from starthinker.util.project import project
from starthinker.util.google_api import API_DCM
from starthinker.util.data import put_rows, get_rows
from starthinker.util.dcm import get_profile_for_api, id_to_timezone
from starthinker.util.regexp import epoch_to_datetime
from starthinker.task.dcm_api.schema.lookup import DCM_Schema_Lookup

PROFILE_CAMPAIGNS = []
PROFILE_SITES = []
PROFILE_ROLES = []
PROFILE_ADVERTISERS = []
REPORT_DELIVERIES = []
SITE_CONTACTS = []

ACCOUNTS_SCHEMA = [
 { "name":"accountId", "type":"INTEGER" },
 { "name":"name", "type":"STRING" },
 { "name":"active", "type":"BOOLEAN" },
 { "name":"description", "type":"STRING" },
 { "name":"timezone", "type":"STRING" },
 { "name":"currencyId", "type":"INTEGER" },
 { "name":"countryId", "type":"INTEGER" },
 { "name":"locale", "type":"STRING" },
 { "name":"nielsenOcrEnabled", "type":"BOOLEAN" },
 { "name":"shareReportsWithTwitter", "type":"BOOLEAN" },
]

PROFILES_SCHEMA = [
 { "name":"profileId", "type":"INTEGER" },
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"name", "type":"STRING" },
 { "name":"email", "type":"STRING" },
 { "name":"locale", "type":"STRING" },
 { "name":"userRoleId", "type":"INTEGER" },
 { "name":"userAccessType", "type":"STRING" },
 { "name":"active", "type":"BOOLEAN" },
 { "name":"comments", "type":"STRING" },
 { "name":"traffickerType", "type":"STRING" },
]

PROFILE_CAMPAIGNS_SCHEMA = [
 { "name":"profileId", "type":"INTEGER" },
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"campaignId", "type":"INTEGER" },
]

PROFILE_SITES_SCHEMA = [
 { "name":"profileId", "type":"INTEGER" },
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"siteId", "type":"INTEGER" },
]

PROFILE_ROLES_SCHEMA = [
 { "name":"profileId", "type":"INTEGER" },
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"roleId", "type":"INTEGER" },
]

PROFILE_ADVERTISERS_SCHEMA = [
 { "name":"profileId", "type":"INTEGER" },
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"advertiserId", "type":"INTEGER" },
]

ADVERTISERS_SCHEMA = [
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"advertiserId", "type":"INTEGER" },
 { "name":"advertiserGroupId", "type":"INTEGER" },
 { "name":"name", "type":"STRING" },
 { "name":"status", "type":"STRING" },
 { "name":"defaultEmail", "type":"STRING" },
 { "name":"clickThroughUrlSuffix", "type":"STRING" },
 { "name":"defaultClickThroughEventTagId", "type":"INTEGER" },
 { "name":"suspended", "type":"BOOLEAN" },
 { "name":"floodlightConfigurationId", "type":"INTEGER" },
 { "name":"originalFloodlightConfigurationId", "type":"INTEGER" },
]

CAMPAIGNS_SCHEMA = [
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"advertiserId", "type":"INTEGER" },
 { "name":"advertiserGroupId", "type":"INTEGER" },
 { "name":"campaignId", "type":"INTEGER" },
 { "name":"name", "type":"STRING" },
 { "name":"archived", "type":"BOOLEAN" },
 { "name":"startDate", "type":"DATE" },
 { "name":"endDate", "type":"DATE" },
 { "name":"comment", "type":"STRING" },
 { "name":"createInfo_time", "type":"STRING" },
 { "name":"lastModifiedInfo_time", "type":"TIMESTAMP" },
 { "name":"externalId", "type":"STRING" },
 { "name":"defaultLandingPageId", "type":"STRING" },
 { "name":"adBlockingConfiguration_enabled", "type":"BOOLEAN" },
 { "name":"adBlockingConfiguration_overrideClickThroughUrl", "type":"STRING" },
 { "name":"adBlockingConfiguration_clickThroughUrl", "type":"STRING" },
 { "name":"adBlockingConfiguration_creativeBundleId", "type":"STRING" },
 { "name":"nielsenOcrEnabled", "type":"BOOLEAN" },
]

SITES_SCHEMA = [
 { "name":"accountId", "type":"INTEGER" }, 
 { "name":"subaccountId", "type":"INTEGER" }, 
 { "name":"directorySiteId", "type":"INTEGER" },
 { "name":"siteId", "type":"INTEGER" }, 
 { "name":"name", "type":"STRING" },
 { "name":"keyName", "type":"STRING" },
 { "name":"approved", "type":"BOOLEAN" },
 { "name":"orientation", "type":"STRING" },
 { "name":"siteSettings_disableNewCookie", "type":"BOOLEAN" },
 { "name":"siteSettings_activeViewOptOut", "type":"BOOLEAN" },
 { "name":"siteSettings_adBlockingOptOut", "type":"BOOLEAN" },
 { "name":"siteSettings_videoActiveViewOptOutTemplate", "type":"BOOLEAN" },
 { "name":"siteSettings_vpaidAdapterChoiceTemplate", "type":"STRING" },
 { "name":"siteSettings_tagSetting_additionalKeyValues", "type":"STRING" },
 { "name":"siteSettings_tagSetting_includeClickTracking", "type":"BOOLEAN" },
 { "name":"siteSettings_tagSetting_includeClickThroughUrls", "type":"BOOLEAN" },
 { "name":"siteSettings_tagSetting_keywordOption", "type":"STRING" },
]

SITE_CONTACTS_SCHEMA = [
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"directorySiteId", "type":"INTEGER" },
 { "name":"siteId", "type":"INTEGER" },
 { "name":"contactId", "type":"INTEGER" },
 { "name":"email", "type":"STRING" },
 { "name":"firstName", "type":"STRING" },
 { "name":"lastName", "type":"STRING" },
 { "name":"title", "type":"STRING" },
 { "name":"address", "type":"STRING" },
 { "name":"phone", "type":"STRING" },
 { "name":"contactType", "type":"STRING" },
]

ROLES_SCHEMA = [
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"roleId", "type":"INTEGER" },
 { "name":"role_name", "type":"STRING" },
 { "name":"role_defaultUserRole", "type":"BOOLEAN" },
 { "name":"permission_name", "type":"STRING" },
 { "name":"permission_availability", "type":"STRING" },
]

SUBACCOUNTS_SCHEMA = [
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"name", "type":"STRING" },
]

REPORTS_SCHEMA = [
 { "name":"profileId", "type":"INTEGER" },
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"reportId", "type":"INTEGER" },
 { "name":"name", "type":"STRING" },
 { "name":"type", "type":"STRING" },
 { "name":"format", "type":"STRING" },
 { "name":"lastModifiedTime", "type":"TIMESTAMP" },
 { "name":"criteria_startDate", "type":"DATE" },
 { "name":"criteria_endDate", "type":"DATE" },
 { "name":"criteria_relativeDateRange", "type":"STRING" },
 { "name":"schedule_active", "type":"BOOLEAN" },
 { "name":"schedule_startDate", "type":"DATE" },
 { "name":"schedule_expirationDate", "type":"DATE" },
 { "name":"schedule_runsOnDayOfMonth", "type":"STRING" },
 { "name":"schedule_repeats", "type":"STRING" },
 { "name":"schedule_every", "type":"STRING" },
 { "name":"schedule_repeatsOnWeekDays", "type":"STRING" },
]

REPORT_DELIVERIES_SCHEMA = [
 { "name":"profileId", "type":"INTEGER" },
 { "name":"accountId", "type":"INTEGER" },
 { "name":"subaccountId", "type":"INTEGER" },
 { "name":"reportId", "type":"INTEGER" },
 { "name":"emailOwner", "type":"STRING" },
 { "name":"emailOwnerDeliveryType", "type":"STRING" },
 { "name":"message", "type":"STRING" },
 { "name":"email", "type":"STRING" },
 { "name":"deliveryType", "type":"STRING" },
]


RE_DATETIME = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}[ T]\d{2}:\d{2}:\d{2}\.?\d+Z')
def bigquery_clean(struct):
  if isinstance(struct, dict):
    for key, value in struct.items():
      if isinstance(value, basestring) and RE_DATETIME.match(value):
        struct[key] =  struct[key].replace('.000Z', '.0000')
      else:
        bigquery_clean(value)
  elif isinstance(struct, list):
    for index, value in enumerate(struct):
      if isinstance(value, basestring) and RE_DATETIME.match(value):
        struct[index] = struct[index].replace('.000Z', '.0000')
      else:
        bigquery_clean(value)
  return  struct


def row_clean(structs):
  for struct in structs:
    yield bigquery_clean(struct) 


def get_accounts(accounts):
  if project.verbose: print 'DCM Accounts'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'id':account_id }
    account = API_DCM("user").accounts().get(**kwargs).execute()
    yield [
      account['id'],
      account['name'],
      account['active'],
      account['description'],
      id_to_timezone(account['reportsConfiguration']['reportGenerationTimeZoneId']),
      account.get('currencyId'),
      account.get('countryId'),
      account['locale'],
      account['nielsenOcrEnabled'],
      account['shareReportsWithTwitter'],
    ]


def get_profiles(accounts):
  if project.verbose: print 'DCM Profiles'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for profile in API_DCM("user", iterate=True, internal=is_superuser).accountUserProfiles().list(**kwargs).execute():
      if long(profile['accountId']) in accounts:

        for campaign in profile.get('campaignFilter', {}).get('objectIds', []):
          PROFILE_CAMPAIGNS.append([
            profile['id'],
            profile['accountId'],
            profile.get('subaccountId'),
            campaign,
          ])

        for site in profile.get('siteFilter', {}).get('objectIds', []):
          PROFILE_SITES.append([
            profile['id'],
            profile['accountId'],
            profile.get('subaccountId'),
            site,
          ])

        for role in profile.get('userRoleFilter', {}).get('objectIds', []):
          PROFILE_ROLES.append([
            profile['id'],
            profile['accountId'],
            profile.get('subaccountId'),
            role,
          ])

        for advertiser in profile.get('advertiserFilter', {}).get('objectIds', []):
          PROFILE_ADVERTISERS.append([
            profile['id'],
            profile['accountId'],
            profile.get('subaccountId'),
            advertiser,
          ])

        yield [
          profile['id'],
          profile['accountId'],
          profile.get('subaccountId'),
          profile['name'],
          profile['email'],
          profile.get('locale'),
          profile.get('userRoleId'),
          profile.get('userAccessType'),
          profile['active'],
          profile.get('comments', ''),
          profile.get('traffickerType'),
        ]


def get_subaccounts(accounts):

  if project.verbose: print 'DCM SubAccounts'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for subaccount in API_DCM("user", iterate=True, internal=is_superuser).subaccounts().list(**kwargs).execute():
      if long(subaccount['accountId']) in accounts: 
        yield [
          subaccount['accountId'],
          subaccount['id'],
          subaccount['name'],
       ]


def get_advertisers(accounts):

  if project.verbose: print 'DCM Advertisers'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for advertiser in API_DCM("user", iterate=True, internal=is_superuser).advertisers().list(**kwargs).execute():
      if long(advertiser['accountId']) in accounts: 
        yield [
          advertiser['accountId'],
          advertiser.get('subaccountId'),
          advertiser['id'],
          advertiser.get('advertiserGroupId'),
          advertiser['name'],
          advertiser['status'],
          advertiser.get('defaultEmail'),
          advertiser.get('clickThroughUrlSuffix'),
          advertiser.get('defaultClickThroughEventTagId'),
          advertiser['suspended'],
          advertiser['floodlightConfigurationId'],
          advertiser['originalFloodlightConfigurationId'],
       ]


def get_campaigns(accounts):

  if project.verbose: print 'DCM Campaigns'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for campaign in API_DCM("user", iterate=True, internal=is_superuser).campaigns().list(**kwargs).execute():
      if long(campaign['accountId']) in accounts: 

        yield [
          campaign['accountId'],
          campaign.get('subaccountId'),
          campaign['advertiserId'],
          campaign.get('advertiserGroupId'),
          campaign['id'],
          campaign['name'],
          campaign['archived'],
          campaign['startDate'],
          campaign['endDate'],
          campaign.get('comment', ''),
          epoch_to_datetime(campaign['createInfo']['time'], 1000),
          epoch_to_datetime(campaign['lastModifiedInfo']['time'], 1000),
          campaign.get('externalId'),
          campaign['defaultLandingPageId'],
          campaign['adBlockingConfiguration']['enabled'],
          campaign['adBlockingConfiguration']['overrideClickThroughUrl'],
          campaign['adBlockingConfiguration'].get('clickThroughUrl'),
          campaign['adBlockingConfiguration'].get('creativeBundleId'),
          campaign['nielsenOcrEnabled'],
       ]


def get_ads(accounts):

  if project.verbose: print 'DCM Ads'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for ad in API_DCM("user", iterate=True, internal=is_superuser).ads().list(**kwargs).execute():
      yield ad
      break

def get_creatives(accounts):

  if project.verbose: print 'DCM Ads'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for ad in API_DCM("user", iterate=True, internal=is_superuser).creatives().list(**kwargs).execute():
      yield ad


def get_sites(accounts):

  if project.verbose: print 'DCM Sites'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for site in API_DCM("user", iterate=True, internal=is_superuser).sites().list(**kwargs).execute():
      if long(site['accountId']) in accounts: 

        for contact in site.get('siteContacts', []):
          SITE_CONTACTS.append([
            site['accountId'],
            site.get('subaccountId'),
            site.get('directorySiteId'),
            site['id'],
            contact['id'],
            contact['email'],
            contact.get('firstName', ''),
            contact.get('lastName', ''),
            contact.get('title', ''),
            contact.get('address', ''),
            contact.get('phone', ''),
            contact['contactType'],
          ])

        yield [
          site['accountId'],
          site.get('subaccountId'),
          site.get('directorySiteId'),
          site['id'],
          site['name'],
          site['keyName'],
          site['approved'],
          site.get('orientation'),
          site['siteSettings'].get('disableNewCookie'),
          site['siteSettings'].get('activeViewOptOut'),
          site['siteSettings'].get('adBlockingOptOut'),
          site['siteSettings'].get('videoActiveViewOptOutTemplate'),
          site['siteSettings'].get('vpaidAdapterChoiceTemplate'),
          site['siteSettings'].get('tagSetting', {}).get('additionalKeyValues'),
          site['siteSettings'].get('tagSetting', {}).get('includeClickTracking'),
          site['siteSettings'].get('tagSetting', {}).get('includeClickThroughUrls'),
          site['siteSettings'].get('tagSetting', {}).get('keywordOption'),
        ]

def get_roles(accounts):
  if project.verbose: print 'DCM Roles'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for role in API_DCM("user", iterate=True, internal=is_superuser).userRoles().list(**kwargs).execute():
      if long(role['accountId']) in accounts:
        if 'permissions' in role:
          for permission in role['permissions']:
            yield [
              role['accountId'],
              role.get('subaccountId'),
              role['id'],
              role['name'],
              role['defaultUserRole'],
              permission['name'],
              permission['availability'],
            ]
        else:
          yield [
            role['accountId'],
            role.get('subaccountId'),
            role['id'],
            role['name'],
            role['defaultUserRole'],
            None,
            None,
          ]


def get_reports(accounts):

  if project.verbose: print 'DCM Reports'

  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id, 'scope':'ALL' } if is_superuser else { 'profileId':profile_id, 'scope':'ALL' }
    for report in API_DCM("user", iterate=True, internal=is_superuser).reports().list(**kwargs).execute():
      if long(report['accountId']) in accounts:
  
        for delivery in report.get('delivery', {}).get('recipients', []):
          REPORT_DELIVERIES.append((
            report['ownerProfileId'],
            report['accountId'],
            report.get('subaccountId'),
            report['id'],
            report['delivery']['emailOwner'],
            report['delivery'].get('emailOwnerDeliveryType'),
            report['delivery'].get('message', ''),
            delivery['email'],
            delivery['deliveryType'],
          ))
 
        yield [
          report['ownerProfileId'],
          report['accountId'],
          report.get('subaccountId'),
          report['id'],
          report['name'],
          report['type'],
          report.get('format'),
          epoch_to_datetime(report.get('lastModifiedTime'), 1000),
          report.get('criteria', {}).get('startDate'),
          report.get('criteria', {}).get('endDate'),
          report.get('criteria', {}).get('relativeDateRange'),
          report.get('schedule', {}).get('active'),
          report.get('schedule', {}).get('startDate'),
          report.get('schedule', {}).get('expirationDate'),
          report.get('schedule', {}).get('runsOnDayOfMonth'),
          report.get('schedule', {}).get('repeats'),
          report.get('schedule', {}).get('every'),
          ','.join(report.get('schedule', {}).get('repeatsOnWeekDays', [])),
        ]


def put_json(kind, schema, row_format='CSV'):

  out = {}

  if 'dataset' in project.task['out']:
    out["bigquery"] = {
      "dataset": project.task['out']['dataset'],
      "table": kind,
      "schema": schema,
      "skip_rows": 0,
      "format":row_format,
    }

  if 'sheet' in project.task:
    out["sheets"] = {
      "url":project.task['out']['sheet'],
      "tab":kind,
      "range":"A1:A1",
      "delete": True
    }

  return out


def dcm_api_list(endpoint):
  accounts = set(get_rows("user", project.task['accounts']))
  for account_id in accounts:
    is_superuser, profile_id = get_profile_for_api(project.task['auth'], account_id)
    kwargs = { 'profileId':profile_id, 'accountId':account_id } if is_superuser else { 'profileId':profile_id }
    for item in API_DCM(project.task['auth'], iterate=True, internal=is_superuser).function(endpoint).list(**kwargs).execute():
      yield item
      break

@project.from_parameters
def dcm_api():
  if project.verbose: print 'DCM'

  if project.task.get('V2', False):

    for endpoint in project.task['endpoints']:
      schema = DCM_Schema_Lookup[endpoint]
      rows = dcm_api_list(endpoint)
      rows = row_clean(rows)
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_%s' % endpoint, schema),
        "DCM_Accounts.csv",
        rows
      )

  else:

    accounts = set(get_rows("user", project.task['accounts']))

    if 'accounts' in project.task['endpoints']:
      # Accounts
      rows = get_accounts(accounts)
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Accounts', ACCOUNTS_SCHEMA),
        "DCM_Accounts.csv",
        rows
      )
  
    if 'profiles' in project.task['endpoints']:
      # Profiles
      rows = get_profiles(accounts)
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Profiles', PROFILES_SCHEMA),
        "DCM_Profiles.csv",
        rows
      )
  
      # Profiles Campaigns
      if project.verbose: print 'DCM Profile Campaigns'
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Profile_Campaigns', PROFILE_CAMPAIGNS_SCHEMA),
        "DCM_Profile_Campaigns.csv",
        PROFILE_CAMPAIGNS
      )
  
      # Profiles Sites
      if project.verbose: print 'DCM Profile Sites'
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Profile_Sites', PROFILE_SITES_SCHEMA),
        "DCM_Profile_Sites.csv",
        PROFILE_SITES
      )
  
      # Profiles Roles
      if project.verbose: print 'DCM Profile Roles'
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Profile_Roles', PROFILE_ROLES_SCHEMA),
        "DCM_Profile_Roles.csv",
        PROFILE_ROLES
      )
  
      # Profiles Advertisers
      if project.verbose: print 'DCM Profile Advertisers'
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Profile_Advertisers', PROFILE_ADVERTISERS_SCHEMA),
        "DCM_Profile_Advertisers.csv",
        PROFILE_ADVERTISERS
      )
  
    if 'subaccounts' in project.task['endpoints']:
      # Subaccounts
      rows = get_subaccounts(accounts)
      put_rows(
        project.task['out']['auth'],
        put_json('CM_SubAccounts', SUBACCOUNTS_SCHEMA),
        "DCM_SubAccounts.csv",
        rows
      )
  
    if 'advertisers' in project.task['endpoints']:
      # Advertisers
      rows = get_advertisers(accounts)
      put_rows(
        project.task['out']['auth'],
        put_json('CM_Advertisers', ADVERTISERS_SCHEMA),
        "DCM_Advertisers.csv",
        rows
      )
  
    if 'campaigns' in project.task['endpoints']:
      # Campaigns 
      rows = get_campaigns(accounts)
      put_rows(
        project.task['out']['auth'],
        put_json('CM_Campaigns', CAMPAIGNS_SCHEMA),
        "DCM_Campaigns.csv",
        rows
      )
  
    if 'ads' in project.task['endpoints']:
      # Ads 
      schema = DCM_Schema_Lookup['ads']
      rows = get_ads(accounts)
      rows = row_clean(rows)
      put_rows(
        project.task['out']['auth'],
        put_json('CM_Ads', schema, 'JSON'),
        "DCM_Ads.csv",
        rows
      )
  
    if 'creatives' in project.task['endpoints']:
      # Creatives 
      rows = get_creatives(accounts)
      put_rows(
        project.task['out']['auth'],
        put_json('CM_Creatives', Creative_Schema),
        "DCM_Creatives.csv",
        rows
      )

    if 'sites' in project.task['endpoints']:
      # Sites 
      rows = get_sites(accounts)
      put_rows(
        project.task['out']['auth'],
        put_json('CM_Sites', SITES_SCHEMA),
        "DCM_Sites.csv",
        rows
      )
  
      # Sites Contacts
      if project.verbose: print 'DCM Site Contacts'
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Site_Contacts', SITE_CONTACTS_SCHEMA),
        "DCM_Site_Contacts.csv",
        SITE_CONTACTS
      )
  
    if 'roles' in project.task['endpoints']:
      # Roles
      rows = get_roles(accounts)
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Roles', ROLES_SCHEMA),
        "DCM_Roles.csv",
        rows
      )
  
    if 'reports' in project.task['endpoints']:
      # Reports
      rows = get_reports(accounts)
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Reports', REPORTS_SCHEMA),
        "DCM_Reports.csv",
        rows
      )
  
      # Reports Deliveries
      if project.verbose: print 'DCM Deliveries'
      put_rows(
        project.task['out']['auth'], 
        put_json('CM_Report_Deliveries', REPORT_DELIVERIES_SCHEMA),
        "DCM_Report_Deliveriess.csv",
        REPORT_DELIVERIES
      )
  
if __name__ == "__main__":
  dcm_api()
