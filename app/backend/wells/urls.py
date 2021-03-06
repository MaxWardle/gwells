"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from django.conf.urls import url
from django.views.decorators.cache import never_cache

from gwells.urls import api_path_prefix
from . import views
from . import views_v2

urlpatterns = [

    # API endpoints
    # Submissions for a well
    url(api_path_prefix() + r'/wells/(?P<well_tag_number>[0-9]+)/edit$',
        never_cache(views.WellStaffEditDetail.as_view()), name='well-edit-details'),


    url(api_path_prefix() + r'/wells/(?P<well_id>[0-9]+)/history$',
        never_cache(views.WellHistory.as_view()), name='well-history'),

    # Submissions for a well
    url(api_path_prefix() + r'/wells/(?P<well_id>[0-9]+)/submissions$',
        never_cache(views.WellSubmissionsListAPIView.as_view()), name='submissions-by-well'),

    # Well
    url(api_path_prefix() + r'/wells/(?P<well_tag_number>[0-9]+)$',
        never_cache(views.WellDetail.as_view()), name='well-detail'),

    # Well tag search
    url(api_path_prefix() + r'/wells/tags$',
        never_cache(views.WellTagSearchAPIView.as_view()), name='well-tag-search'),

    # Well screen search
    # returns information about well screens for a range of wells provided in ?wells=123,124,125 etc.
    url(api_path_prefix() + r'/wells/screens$',
        never_cache(views.WellScreens.as_view()), name='well-screens'),

    # Well lithology search
    # returns information about well lithology for a range of wells provided in ?wells=123,124,125 etc.
    url(api_path_prefix() + r'/wells/lithology$',
        never_cache(views.WellLithology.as_view()), name='well-lithology'),

    # Well tag search
    url(r'api/v1/wells/locations$',
        never_cache(views.WellLocationListV1APIView.as_view()), name='well-locations-v1'),

    url(r'api/v2/wells/locations$',
        never_cache(views_v2.WellLocationListV2APIView.as_view()), name='well-locations-v2'),

    # Documents (well records)
    url(api_path_prefix() + r'/wells/(?P<tag>[0-9]+)/files$',
        never_cache(views.ListFiles.as_view()), name='file-list'),

    # Extract files
    url(api_path_prefix() + r'/wells/extracts$', views.ListExtracts.as_view(), name='extract-list'),

    # Document Uploading (well records)
    url(api_path_prefix() + r'/wells/(?P<tag>[0-9]+)/presigned_put_url$',
        never_cache(views.PreSignedDocumentKey.as_view()), name='well-pre-signed-url'),

    # Document Uploading (well records)
    url(api_path_prefix() + r'/wells/(?P<tag>[0-9]+)/delete_document$',
        never_cache(views.DeleteWellDocument.as_view()), name='well-delete-document'),

    # Well list
    url(api_path_prefix() + r'/wells$',
        never_cache(views.WellListAPIView.as_view()), name='well-list'),

    # Well search export
    url(api_path_prefix() + r'/wells/export$',
        never_cache(views.WellExportListAPIView.as_view()), name='well-export'),

    # GeoJSON well endpoint for DataBC.
    url(api_path_prefix() + r'/gis/wells$',
        views.well_geojson, name='well-geojson'),

    # GeoJSON lithology endpoint for DataBC.
    url(api_path_prefix() + r'/gis/lithology$',
        views.lithology_geojson, name='well-lithology-geojson'),

    # Well Licensing status endpoint from e-Licensing.
    url(api_path_prefix() + r'/wells/licensing$',
        views.well_licensing, name='well-licensing')
]
