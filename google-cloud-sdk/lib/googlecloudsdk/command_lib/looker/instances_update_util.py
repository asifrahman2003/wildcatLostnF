# -*- coding: utf-8 -*- #
# Copyright 2023 Google LLC. All Rights Reserved.
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
"""Utility for updating Looker instances.

This utily is primarily used for modifying request hooks for update requests for
Looker instances. See go/gcloud-creating-commands#request-hooks for more
details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.core.console import console_io


def _WarnForAdminSettingsUpdate():
  """Adds prompt that warns about allowed email domains update."""
  message = 'Change to instance allowed email domain requested. '
  message += (
      'Updating the allowed email domains from cli means the value provided'
      ' will be considered as the entire list and not an amendment to the'
      ' existing list of allowed email domains.'
  )
  console_io.PromptContinue(
      message=message,
      prompt_string='Do you want to proceed with update?',
      cancel_on_no=True,
  )


def _WarnForPscAllowedVpcsUpdate():
  """Adds prompt that warns about allowed vpcs update."""
  message = (
      'Change to instance PSC allowed Virtual Private Cloud networks'
      ' requested. '
  )
  message += (
      'Updating the allowed VPC networks from cli means the value provided'
      ' will be considered as the entire list and not an amendment to the'
      ' existing list of allowed vpcs.'
  )
  console_io.PromptContinue(
      message=message,
      prompt_string='Do you want to proceed with update?',
      cancel_on_no=True,
  )


def _WarnForPscAllowedVpcsRemovalUpdate():
  """Adds prompt that warns about allowed vpcs removal."""
  message = 'Removal of instance PSC allowed vpcs requested. '

  console_io.PromptContinue(
      message=message,
      prompt_string='Do you want to proceed with removal of PSC allowed vpcs?',
      cancel_on_no=True,
  )


def _WarnForPscServiceAttachmentsUpdate():
  """Adds prompt that warns about service attachments update."""
  message = 'Change to instance PSC service attachments requested. '
  message += (
      'Updating the PSC service attachments from cli means the value provided'
      ' will be considered as the entire list and not an amendment to the'
      ' existing list of PSC service attachments'
  )
  console_io.PromptContinue(
      message=message,
      prompt_string='Do you want to proceed with update?',
      cancel_on_no=True,
  )


def _WarnForPscServiceAttachmentsRemovalUpdate():
  """Adds prompt that warns about service attachments removal."""
  message = 'Removal of instance PSC service attachments requested. '

  console_io.PromptContinue(
      message=message,
      prompt_string=(
          'Do you want to proceed with removal of service attachments?'
      ),
      cancel_on_no=True,
  )


def AddFieldToUpdateMask(field, patch_request):
  """Adds fields to the update mask of the patch request.

  Args:
    field: the field of the update mask to patch request for Looker instances.
    patch_request: the request of the actual update command to be modified

  Returns:
    A patch request object to be sent to the server. The object is an instance
    of UpdateInstanceRequest: http://shortn/_yn9MhWaGJx
  """
  update_mask = patch_request.updateMask
  if update_mask:
    if update_mask.count(field) == 0:
      patch_request.updateMask = '%s,%s' % (update_mask, field)
  else:
    patch_request.updateMask = field
  return patch_request


def ModifyAllowedEmailDomains(unused_instance_ref, args, patch_request):
  """Python hook to modify allowed email domains in looker instance update request."""
  if args.IsSpecified('allowed_email_domains'):
    # Changing allowed email domains means this list will be overwritten in the
    # DB and not amended and users should be warned before proceeding.
    _WarnForAdminSettingsUpdate()
    patch_request.instance.adminSettings.allowedEmailDomains = (
        args.allowed_email_domains
    )
    patch_request = AddFieldToUpdateMask(
        'admin_settings.allowed_email_domains', patch_request
    )
  return patch_request


def UpdateMaintenanceWindow(unused_instance_ref, args, patch_request):
  """Hook to update maintenance window to the update mask of the request."""
  if args.IsSpecified('maintenance_window_day') or args.IsSpecified(
      'maintenance_window_time'
  ):
    patch_request = AddFieldToUpdateMask('maintenance_window', patch_request)
  return patch_request


def UpdateEnablePublicIpAlpha(unused_instance_ref, args, patch_request):
  """Hook to update public IP to the update mask of the request for alpha."""
  if args.IsSpecified('enable_public_ip'):
    patch_request = AddFieldToUpdateMask('enable_public_ip', patch_request)
  return patch_request


def UpdatePublicIPEnabled(unused_instance_ref, args, patch_request):
  """Hook to update public IP to the update mask of the request fo GA."""
  if args.IsSpecified('public_ip_enabled'):
    patch_request = AddFieldToUpdateMask('public_ip_enabled', patch_request)
  return patch_request


def UpdateOauthClient(unused_instance_ref, args, patch_request):
  """Hook to update Oauth configs to the update mask of the request."""
  if args.IsSpecified('oauth_client_id') and args.IsSpecified(
      'oauth_client_secret'
  ):
    patch_request = AddFieldToUpdateMask(
        'oauth_config.client_id', patch_request
    )
    patch_request = AddFieldToUpdateMask(
        'oauth_config.client_secret', patch_request
    )

  return patch_request


def UpdateDenyMaintenancePeriod(unused_instance_ref, args, patch_request):
  """Hook to update deny maintenance period to the update mask of the request."""
  if (
      args.IsSpecified('deny_maintenance_period_start_date')
      or args.IsSpecified('deny_maintenance_period_end_date')
      or args.IsSpecified('deny_maintenance_period_time')
  ):
    patch_request = AddFieldToUpdateMask(
        'deny_maintenance_period', patch_request
    )
  return patch_request


def UpdateUserMetadata(unused_instance_ref, args, patch_request):
  """Hook to update deny user metadata to the update mask of the request."""
  if (
      args.IsSpecified('add_viewer_users')
      or args.IsSpecified('add_standard_users')
      or args.IsSpecified('add_developer_users')
  ):
    patch_request = AddFieldToUpdateMask('user_metadata', patch_request)
  return patch_request


def UpdateCustomDomain(unused_instance_ref, args, patch_request):
  """Hook to update custom domain to the update mask of the request."""
  if args.IsSpecified('custom_domain'):
    patch_request = AddFieldToUpdateMask('custom_domain', patch_request)
  return patch_request


def UpdatePscAllowedVpcs(unused_instance_ref, args, patch_request):
  """Hook to update psc confing allowed vpcs to the update mask of the request."""
  if args.IsSpecified('psc_allowed_vpcs'):
    # Changing allowed email domains means this list will be overwritten in the
    # DB and not amended and users should be warned before proceeding.
    _WarnForPscAllowedVpcsUpdate()
    patch_request.instance.pscConfig.allowedVpcs = args.psc_allowed_vpcs
    patch_request = AddFieldToUpdateMask(
        'psc_config.allowed_vpcs', patch_request
    )
  elif args.IsSpecified('clear_psc_allowed_vpcs'):
    _WarnForPscAllowedVpcsRemovalUpdate()
    patch_request = AddFieldToUpdateMask(
        'psc_config.allowed_vpcs', patch_request
    )
  return patch_request


def UpdatePscServiceAttachments(unused_instance_ref, args, patch_request):
  """Hook to update psc confing service attachments to the update mask of the request."""
  if args.IsSpecified('psc_service_attachment'):
    _WarnForPscServiceAttachmentsUpdate()
    patch_request = AddFieldToUpdateMask(
        'psc_config.service_attachments', patch_request
    )
  elif args.IsSpecified('clear_psc_service_attachments'):
    _WarnForPscServiceAttachmentsRemovalUpdate()
    patch_request = AddFieldToUpdateMask(
        'psc_config.service_attachments', patch_request
    )
  return patch_request


def UpdateGeminiAiConfig(unused_instance_ref, args, patch_request):
  """Hook to update gemini enabled to the update mask of the request."""
  if args.IsSpecified('gemini_enabled'):
    patch_request = AddFieldToUpdateMask('gemini_enabled', patch_request)
  if args.IsSpecified('gemini_preview_tester_enabled'):
    patch_request = AddFieldToUpdateMask(
        'gemini_ai_config.trusted_tester', patch_request
    )
  if args.IsSpecified('gemini_prompt_log_enabled'):
    patch_request = AddFieldToUpdateMask(
        'gemini_ai_config.prompt_logging', patch_request
    )
  return patch_request
