"""MCP server exposing the Wan 3.0 Python client as agent tools."""

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP
from wan_api import WanAPI

mcp = FastMCP("Wan 3.0 API Server")


def _api() -> WanAPI:
    return WanAPI()


@mcp.tool()
def text_to_video(
    prompt: str, resolution: str = "720p", aspect_ratio: str = "16:9",
    duration: int = 5, thinking_mode: bool = False, enable_audio: bool = True,
    seed: int = -1,
) -> str:
    """Generate a Wan video with synchronized audio from a descriptive text prompt."""
    return json.dumps(
        _api().text_to_video(
            prompt, resolution=resolution, aspect_ratio=aspect_ratio, duration=duration,
            thinking_mode=thinking_mode, enable_audio=enable_audio, seed=seed,
        ),
        indent=2,
    )


@mcp.tool()
def image_to_video(
    prompt: str, image_url: str, last_image: Optional[str] = None,
    resolution: str = "720p", aspect_ratio: str = "16:9", duration: int = 5,
    thinking_mode: bool = False, enable_audio: bool = True, seed: int = -1,
) -> str:
    """Animate a source image URL into a Wan video with synchronized audio."""
    return json.dumps(
        _api().image_to_video(
            prompt, image_url, last_image=last_image, resolution=resolution,
            aspect_ratio=aspect_ratio, duration=duration, thinking_mode=thinking_mode,
            enable_audio=enable_audio, seed=seed,
        ),
        indent=2,
    )


@mcp.tool()
def reference_to_video(
    prompt: str, images_list: Optional[list[str]] = None,
    videos_list: Optional[list[str]] = None, audios_list: Optional[list[str]] = None,
    resolution: str = "720p", aspect_ratio: str = "16:9", duration: int = 5,
    thinking_mode: bool = False, enable_audio: bool = True, seed: int = -1,
) -> str:
    """Generate a Wan video conditioned on up to 10 reference images, 5 reference
    videos, and 5 reference audios."""
    return json.dumps(
        _api().reference_to_video(
            prompt, images_list=images_list, videos_list=videos_list,
            audios_list=audios_list, resolution=resolution, aspect_ratio=aspect_ratio,
            duration=duration, thinking_mode=thinking_mode, enable_audio=enable_audio,
            seed=seed,
        ),
        indent=2,
    )


@mcp.tool()
def get_task_status(request_id: str) -> str:
    """Get the status and outputs for a Wan generation job."""
    return json.dumps(_api().get_result(request_id), indent=2)


if __name__ == "__main__":
    mcp.run()
