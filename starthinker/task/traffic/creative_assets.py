###########################################################################
#
#  Copyright 2017 Google Inc.
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
"""Handles creation and updates of creative assets.

"""

import os
import json
from apiclient import http

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.store import store
from starthinker.util.storage import object_download


class CreativeAssetDAO(BaseDAO):
  """Creative asset data access object.

  Inherits from BaseDAO and implements ad specific logic for creating and
  updating ads.
  """

  def __init__(self, auth, profile_id, gc_project):
    """Initializes CreativeAssetDAO with profile id and authentication scheme."""
    super(CreativeAssetDAO, self).__init__(auth, profile_id)

    self._entity = 'CREATIVE_ASSET'
    self._service = self.service.creativeAssets()
    self.gc_project = gc_project
    self._list_name = ''
    self._id_field = FieldMap.CREATIVE_ASSET_ID
    self._search_field = None
    self.auth = auth

    self._parent_filter_name = None
    self._parent_filter_field_name = None

  def pre_fetch(self, feed):
    """Pre-fetches all required items to be update into the cache.

    This increases performance for update operations.

    Args:
      feed: List of feed items to retrieve
    """
    pass

  def _process_update(self, item, feed_item):
    """Handles updates to the creative asset object.

    Since creative assets are read only in DCM, there is nothing to do here,
    this method is mandatory as it is invoked by the BaseDAO class.

    Args:
      item: The creative asset DCM object being updated.
      feed_item: The feed item representing the creative asset from the
        Bulkdozer feed.
    """
    pass

  def _insert(self, new_item, feed_item):
    """Handles the upload of creative assets to DCM and the creation of the associated entity.

    This method makes a call to the DCM API to create a new entity.

    Args:
      new_item: The item to insert into DCM.
      feed_item: The feed item representing the creative asset from the
        Bulkdozer feed.

    Returns:
      The newly created item in DCM.
    """
    local_file = os.path.join('/tmp', feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None))

    self._download_from_gcs(
        feed_item.get(FieldMap.CREATIVE_ASSET_BUCKET_NAME, None),
        feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None),
        local_file,
        auth=self.auth)

    media = http.MediaFileUpload(local_file)

    if not media.mimetype():
      mimetype = 'application/zip' if asset_type == 'HTML' else 'application/octet-stream'
      media = http.MediaFileUpload(asset_file, mimetype)

    result = self._retry(
        self._service.insert(
            profileId=self.profile_id,
            advertiserId=feed_item.get(FieldMap.ADVERTISER_ID, None),
            media_body=media,
            body=new_item))

    os.remove(local_file)

    return result

  def _get(self, feed_item):
    """Retrieves an item from DCM or the local cache.

    Args:
      feed_item: The feed item representing the creative asset from the
        Bulkdozer feed.

    Returns:
      Instance of the DCM object either from the API or from the local cache.
    """
    result = store.get(self._entity, feed_item.get(FieldMap.CREATIVE_ASSET_ID, None))

    if not result:
      result = {
          'id': feed_item.get(FieldMap.CREATIVE_ASSET_ID, None),
          'assetIdentifier': {
              'name': feed_item.get(FieldMap.CREATIVE_ASSET_NAME, None),
              'type': feed_item.get(FieldMap.CREATIVE_TYPE, None)
          }
      }

      store.set(self._entity, [feed_item.get(FieldMap.CREATIVE_ASSET_ID, None)], result)

    return result

  def _update(self, item, feed_item):
    """Performs an update in DCM.

    Since this method is not allowed for creative assets because those cannot be
    updated, this method reimplements _update from BaseDAO but doesn't do
    anything to prevent an error.

    Args:
      item: The item to update in DCM.
      feed_item: The feed item representing the creative asset in the Bulkdozer
        feed.
    """
    pass

  def _process_new(self, feed_item):
    """Creates a new creative asset DCM object from a feed item representing a creative asset from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the creative asset from the Bulkdozer
        feed.

    Returns:
      A creative asset object ready to be inserted in DCM through the API.

    """
    return {
        'assetIdentifier': {
            'name': feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None),
            'type': feed_item.get(FieldMap.CREATIVE_TYPE, None)
        }
    }

  def _post_process(self, feed_item, item):
    """Maps ids and names of related entities so they can be updated in the Bulkdozer feed.

    When Bulkdozer is done processing an item, it writes back the updated names
    and ids of related objects, this method makes sure those are updated in the
    creative asset feed.

    Args:
      feed_item: Feed item representing the creative asset from the Bulkdozer
        feed.
      item: The DCM creative asset being updated or created.
    """
    if item['assetIdentifier']['name']:
      feed_item[FieldMap.CREATIVE_ASSET_NAME] = item['assetIdentifier']['name']

  def _download_from_gcs(self, bucket, object_name, local_file, auth='user'):
    """Downloads assets from Google Cloud Storage locally to be uploaded to DCM.

    Args:
      bucket: Name of the Google Cloud bucket where the asset is located.
      object_name: Name of the object in Google Cloud within the specified
        bucket.
      local_file: The full physical path to a non existing local file where the
        object should be saved.
      auth: Authentication scheme to use to access Cloud Storage.
    """
    object_download(self.gc_project, bucket, object_name, local_file, auth=auth)

  def get_identifier(self, association, feed):
    asset_ids = (association.get(FieldMap.CREATIVE_ASSET_ID, None), store.translate(self._entity, association[FieldMap.CREATIVE_ASSET_ID]))

    for creative_asset in feed.feed:
      if str(creative_asset[FieldMap.CREATIVE_ASSET_ID]) in asset_ids:
        return {
            'name': creative_asset.get(FieldMap.CREATIVE_ASSET_NAME, None),
            'type': creative_asset.get(FieldMap.CREATIVE_TYPE, None)
        }

    return None
