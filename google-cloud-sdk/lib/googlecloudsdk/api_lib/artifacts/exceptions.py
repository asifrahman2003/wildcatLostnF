# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
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
"""Wrapper for user-visible raised exception."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.core import exceptions
import six


class InvalidInputValueError(exceptions.Error):
  """Raised when the given input value is invalid."""


class UnsupportedLocationError(exceptions.Error):
  """Raised when the given location is invalid."""


class ArtifactRegistryError(exceptions.Error):
  """Generic Artifact Registry error."""


class InvalidGoModuleError(exceptions.Error):
  """Raised when the Go module source code cannot be packaged into a go.zip."""


class DirectoryNotExistError(ArtifactRegistryError):
  """Raised when a directory does not exist."""


class PathNotDirectoryError(ArtifactRegistryError):
  """Raised when a path is not a directory."""


class NoJsonKeyCredentialsError(ArtifactRegistryError):
  """Raised when no JSON key credentials are found."""

  def __init__(self, cause):
    super().__init__(
        "JSON key credentials not found: {}".format(six.text_type(cause))
    )


class NoDefaultCredentialsError(ArtifactRegistryError):
  """Raised when no JSON key credentials are found."""

  def __init__(self, cause):
    super().__init__(
        "Application default credentials not found: {}".format(
            six.text_type(cause)
        )
    )


class NoUserCredentialsError(ArtifactRegistryError):
  """Raised when no JSON key credentials are found."""

  def __init__(self, cause):
    super().__init__(
        "User credentials not found: {}".format(six.text_type(cause))
    )


class NoCredentialsError(ArtifactRegistryError):
  """Raised when no credentials are found."""

  def __init__(self, json_key_err, adc_err, user_creds_err):
    super().__init__(
        "No credentials found. Details: {}".format(
            "; ".join(
                six.text_type(e)
                for e in [json_key_err, adc_err, user_creds_err]
            )
        )
    )
