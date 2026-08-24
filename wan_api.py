"""A small Python client for the Wan 3.0 video generation API."""

import os
import time
from typing import Any, Dict, Iterable, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class WanAPI:
    """Submit Wan 3.0 video jobs and retrieve their asynchronous results."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("An API key is required. Set MUAPI_API_KEY or pass api_key.")
        self.base_url = (base_url or os.getenv("WAN_API_BASE_URL") or "https://api.muapi.ai/api/v1").rstrip("/")
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

    def text_to_video(
        self, prompt: str, *, resolution: str = "720p", aspect_ratio: str = "16:9",
        duration: int = 5, thinking_mode: bool = False, enable_audio: bool = True,
        seed: int = -1,
    ) -> Dict[str, Any]:
        """Generate a video with synchronized audio from a text prompt."""
        payload: Dict[str, Any] = {
            "prompt": prompt, "resolution": resolution, "aspect_ratio": aspect_ratio,
            "duration": duration, "thinking_mode": thinking_mode,
            "enable_audio": enable_audio, "seed": seed,
        }
        return self._post("wan3.0-text-to-video", payload)

    def image_to_video(
        self, prompt: str, image_url: str, *, last_image: Optional[str] = None,
        resolution: str = "720p", aspect_ratio: str = "16:9", duration: int = 5,
        thinking_mode: bool = False, enable_audio: bool = True, seed: int = -1,
    ) -> Dict[str, Any]:
        """Animate a source image with a text motion prompt."""
        payload: Dict[str, Any] = {
            "prompt": prompt, "image_url": image_url, "resolution": resolution,
            "aspect_ratio": aspect_ratio, "duration": duration,
            "thinking_mode": thinking_mode, "enable_audio": enable_audio, "seed": seed,
        }
        if last_image:
            payload["last_image"] = last_image
        return self._post("wan3.0-image-to-video", payload)

    def reference_to_video(
        self, prompt: str, *, images_list: Optional[Iterable[str]] = None,
        videos_list: Optional[Iterable[str]] = None, audios_list: Optional[Iterable[str]] = None,
        resolution: str = "720p", aspect_ratio: str = "16:9", duration: int = 5,
        thinking_mode: bool = False, enable_audio: bool = True, seed: int = -1,
    ) -> Dict[str, Any]:
        """Create a video conditioned on up to 10 reference images, 5 reference
        videos, and 5 reference audios. Reference media are identified by their
        order within each array, so the prompt can refer to them by position."""
        payload: Dict[str, Any] = {
            "prompt": prompt, "resolution": resolution, "aspect_ratio": aspect_ratio,
            "duration": duration, "thinking_mode": thinking_mode,
            "enable_audio": enable_audio, "seed": seed,
        }
        if images_list:
            payload["images_list"] = list(images_list)
        if videos_list:
            payload["videos_list"] = list(videos_list)
        if audios_list:
            payload["audios_list"] = list(audios_list)
        return self._post("wan3.0-reference-to-video", payload)

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """Upload a local reference asset for a subsequent generation request."""
        with open(file_path, "rb") as file_data:
            response = requests.post(
                f"{self.base_url}/upload_file", headers={"x-api-key": self.api_key},
                files={"file": file_data}, timeout=120,
            )
        response.raise_for_status()
        return response.json()

    def get_result(self, request_id: str) -> Dict[str, Any]:
        """Retrieve the current state and output of a generation job."""
        response = requests.get(f"{self.base_url}/predictions/{request_id}/result", headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, request_id: str, poll_interval: int = 5, timeout: int = 900) -> Dict[str, Any]:
        """Poll a job until it completes, fails, or reaches the timeout."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.get_result(request_id)
            status = result.get("status", "").lower()
            if status in {"completed", "succeeded", "success"}:
                return result
            if status in {"failed", "error", "cancelled"}:
                raise RuntimeError(f"Wan generation {status}: {result.get('error', result)}")
            time.sleep(poll_interval)
        raise TimeoutError(f"Timed out waiting for Wan job {request_id}.")

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/{path}", json=payload, headers=self.headers, timeout=120)
        response.raise_for_status()
        return response.json()
