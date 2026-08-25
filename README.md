# Wan 3.0 API — Python Wrapper

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square)](https://muapi.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

A focused Python SDK and MCP server for the [Wan 3.0 API on MuAPI](https://muapi.ai/wan-3). It supports text-to-video, image-to-video, multimodal reference-to-video (up to 10 reference images, 5 reference videos, and 5 reference audios), synchronized audio, file upload, and asynchronous job polling.

<p align="center"><a href="https://youtu.be/T4Oddw74O44"><img src="https://i.ytimg.com/vi/T4Oddw74O44/maxresdefault.jpg" width="720"></a></p>
<p align="center"><a href="https://youtu.be/T4Oddw74O44"><b>▶ Watch: How to Access Wan 3.0 API - Best Uncensored Alternative to Seedance 2 </b></a></p>

## Related Projects

- [Wan 3 on MuAPI](https://muapi.ai/wan-3) — Model landing page for Wan video-generation workflows.
- [MuAPI video-generation docs](https://muapi.ai/docs/video-generation) — Unified API request and polling patterns.
- [awesome-ai-video-models](https://github.com/Anil-matcha/awesome-ai-video-models) — compare AI video models by API, price, and speed.
- [Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — open-source AI media studio for image and video workflows.
- [Seedance-2-API](https://github.com/Anil-matcha/Seedance-2-API) — Python SDK for ByteDance Seedance video generation.
- [Veo-4-API](https://github.com/Anil-matcha/Veo-4-API) — Python SDK for Google Veo AI video generation.
- [Flux-3-Dev-API](https://github.com/Anil-matcha/Flux-3-Dev-API) — Python SDK for FLUX 3 image and video generation.
- [Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills) — agent-ready skills for automated media workflows.
- [muapi-cli](https://github.com/SamurAIGPT/muapi-cli) — command-line access to MuAPI image, video, and audio models.
- [wan-3.0-comfyui](https://github.com/Anil-matcha/wan-3.0-comfyui) — ComfyUI custom nodes for Wan 3.0 text-to-image, image edit, text-to-video, and image-to-video via MuAPI.
- [Wan-3.0-Prime-API](https://github.com/Anil-matcha/Wan-3.0-Prime-API) — Higher-fidelity Wan 3.0 Prime tier Python SDK and MCP server, same request shape as this repo.

## Install

```bash
git clone https://github.com/Anil-matcha/Wan-3.0-API.git
cd Wan-3.0-API
pip install -r requirements.txt
cp .env.example .env
```

Set `MUAPI_API_KEY` in `.env`. Set `WAN_API_BASE_URL` only if you use a compatible provider other than the default MuAPI base URL.

## Quick start

```python
from wan_api import WanAPI

api = WanAPI()
job = api.text_to_video(
    "A cinematic tracking shot of a red fox crossing a snowy forest at sunrise",
    resolution="720p",
    aspect_ratio="16:9",
    duration=5,
)

result = api.wait_for_completion(job["request_id"])
print(result)
```

## Image to video

```python
job = api.image_to_video(
    prompt="The subject turns toward camera as a gentle breeze moves their hair.",
    image_url="https://example.com/reference.jpg",
    aspect_ratio="9:16",
    duration=5,
)
```

## Reference to video

```python
job = api.reference_to_video(
    prompt="The person from the reference image walks into the room shown in the reference video.",
    images_list=["https://example.com/character.jpg"],
    videos_list=["https://example.com/room.mp4"],
    resolution="720p",
    duration=5,
)
```

## API surface

| Method | Purpose |
| --- | --- |
| `text_to_video()` | Create a video with synchronized audio from a text prompt. |
| `image_to_video()` | Animate a source image, with optional end-frame guidance via `last_image`. |
| `reference_to_video()` | Condition a video on up to 10 reference images, 5 reference videos, and 5 reference audios. |
| `upload_file()` | Upload a local reference file. |
| `get_result()` / `wait_for_completion()` | Retrieve an asynchronous job's output. |

Every method also accepts `resolution` (`480p`, `720p`, `1080p`), `duration` (2-30 seconds), `thinking_mode` (deeper reasoning for complex prompts), `enable_audio`, and `seed`.

## MCP server

Expose Wan tools to MCP-capable clients:

```bash
python mcp_server.py
```

The server provides `text_to_video`, `image_to_video`, `reference_to_video`, and `get_task_status` tools.

## Endpoint compatibility

The client uses the `wan3.0-text-to-video`, `wan3.0-image-to-video`, and `wan3.0-reference-to-video` paths beneath `WAN_API_BASE_URL`. If your provider names its endpoints differently, pass that provider's compatible base URL or adapt the small client module before use.

## License

[MIT](LICENSE)
