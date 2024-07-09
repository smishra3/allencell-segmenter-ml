from typing import Optional
from xml.etree import ElementTree

import requests

from allencell_ml_segmenter.utils.s3 import AvailableModels
from allencell_ml_segmenter.utils.s3.s3_request_exception import (
    S3RequestException,
)

# Enable Model Downloads on plugin
ENABLE_MODEL_DOWNLOADS = True
# Endpoint for prod bucket
BUCKET_ENDPOINT = (
    "https://production-aics-ml-segmenter-models.s3.us-west-2.amazonaws.com"
)
# Endpoint for stg bucket
STG_BUCKET_ENDPOINT = ""


class S3ModelDownloader:
    def __init__(self, staging=False, test_url: Optional[str] = None):
        if test_url:
            self._bucket_endpoint = test_url
        else:
            self._bucket_endpoint = (
                STG_BUCKET_ENDPOINT if staging else BUCKET_ENDPOINT
            )

    def get_available_models(self) -> dict[str, AvailableModels]:
        """
        Get a dict of the filenames of available models on s3.

        Uses a http request to get all available models on s3. This function assumes all models will be in .zip files
        (and ignores all files that are not zip files). Any errors with the request throws a S3RequestException.

        Returns dictionary containing model name keys, and AvailableModels values.
        """
        # request parameter to list all objects in bucket
        req_params: str = "list-type=2"

        response = requests.get(f"{self._bucket_endpoint}?{req_params}")

        if response.status_code == 200:
            # parse XML response
            model_names: list[str] = (
                self._parse_s3_xml_filelist_for_model_names(
                    response.content, ".//Contents"
                )
            )
            # Create List of available Models
            available_models_dict: dict[str, AvailableModels] = {}
            for model_name in model_names:
                available_models_dict[model_name.split(".")[0]] = (
                    AvailableModels(model_name, self._bucket_endpoint)
                )
            return available_models_dict
        else:
            # handle request errors
            raise S3RequestException(
                f"S3 Download failed with status code {response.status_code}. {response.text}"
            )

    def _parse_s3_xml_filelist_for_model_names(
        self, response: bytes, key: str
    ) -> list[str]:
        """
        Parse XML response from s3 containing list of available objects for model names.
        Returns list of available models (which are .zip files) from s3's XML response.
        """
        # parse XML response
        xml_root = ElementTree.fromstring(response)
        # extract s3 object names
        available: list[str] = []
        all_key_matches: list[str] = [
            xml_content.find("Key").text
            for xml_content in xml_root.findall(key)
        ]
        for model_name in all_key_matches:
            # S3 allows duplicate files- ensure we have unique names for all models on s3.
            if model_name in available:
                raise ValueError(
                    f"S3 bucket {self._bucket_endpoint} contains duplicate models for name: {model_name}"
                )
            # append file name if it is a zip file- these are models stored on s3
            if model_name.endswith(".zip"):
                available.append(model_name)
        return available

    def get_bucket_endpoint(self) -> str:
        return self._bucket_endpoint
