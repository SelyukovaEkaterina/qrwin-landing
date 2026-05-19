# Image Generation Skill — HydraAI API

## Overview

Generate images using HydraAI API with the `hydra-banana-pro` model (based on Gemini 3 Pro Image). The model generates images through the **chat completions** endpoint — not the `/images/generations` endpoint.

## API Details

- **Endpoint:** `POST https://api.hydraai.ru/v1/chat/completions`
- **Auth header:** `Authorization: Bearer sk-hydra-ai-nvrgdrNBUzHLvUS5pG-It78G0VxNyw79PaD-L3ntf26QrWJOOBhhqCVo4eraFRN7`
- **Model ID:** `hydra-banana-pro`

### Available Models

| Model ID | Name | Base |
|---|---|---|
| `hydra-banana-pro` | Hydra Banana Pro | Gemini 3 Pro Image / Gemini 3.1 Flash Image |
| `gemini-3-pro-image` | Nano Banana Pro | Gemini 3 Pro Image |
| `gemini-3.1-flash-image` | Nano Banana 2 | Gemini 3.1 Flash Image |
| `gemini-2.5-flash-image` | Nano Banana | Gemini 2.5 Flash Image |

### Request Format

```bash
curl -s -X POST https://api.hydraai.ru/v1/chat/completions \
  -H "Authorization: Bearer $HYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "hydra-banana-pro",
    "messages": [
      {
        "role": "user",
        "content": "<YOUR PROMPT HERE>"
      }
    ]
  }'
```

### Response Format

The response is a standard chat completion. The image is embedded in `choices[0].message.content` as a Markdown image with base64 data:

```
![image](data:image/png;base64,iVBORw0KG...<BASE64_DATA>...)
```

### Extract and Save the Image

```python
import json, base64, re

with open("response.json", "r") as f:
    data = json.load(f)

content = data["choices"][0]["message"]["content"]
match = re.search(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)', content)
if match:
    ext = match.group(1)
    img_bytes = base64.b64decode(match.group(2))
    with open(f"output.{'jpg' if ext == 'jpeg' else ext}", "wb") as f:
        f.write(img_bytes)
```

## Prompt Tips

### Aspect Ratio

Add at the end of the prompt:

- `Соотношение сторон: 16:9` — widescreen
- `Aspect ratio: 1:1` — square
- `Format: 4:3` — classic
- `9:16` — stories / portrait

### Style Keywords

- `Photorealistic, 4k` — photo realism
- `Oil painting style` — painting
- `Cyberpunk, neon lights` — cyberpunk
- `Anime style` — anime
- `Vector style, white background` — logo / vector

### Detail Level

Be descriptive. Bad: "cat". Good: "Fluffy orange cat sitting on a windowsill, rain outside, cozy atmosphere, soft warm light, photorealistic, 4k. Aspect ratio: 1:1"

## Image Editing (Image-to-Image)

Send an image URL or base64 alongside text instructions:

```bash
curl -s -X POST https://api.hydraai.ru/v1/chat/completions \
  -H "Authorization: Bearer $HYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "hydra-banana-pro",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Make this room cyberpunk style with neon lighting"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://example.com/photo.jpg"
            }
          }
        ]
      }
    ]
  }'
```

## Iterative Editing (Smart History)

Pass previous assistant responses (including base64 images) back in the `messages` array to refine:

```bash
curl -s -X POST https://api.hydraai.ru/v1/chat/completions \
  -H "Authorization: Bearer $HYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "hydra-banana-pro",
    "messages": [
      {
        "role": "user",
        "content": "Draw a cat"
      },
      {
        "role": "assistant",
        "content": "![image](data:image/png;base64,...)"
      },
      {
        "role": "user",
        "content": "Make the sky more blue"
      }
    ]
  }'
```

## Cost & Limits

- **Cost per request:** ~2.5 RUB for `hydra-banana-pro`
- **Generation time:** 15–35 seconds typically
- **Image lifetime (URL format):** 24 hours (base64 is permanent once saved)
- **Docs:** https://docs.hydraai.ru/main_documentation/api_endpoints/
- **Servers:** https://api.hydraai.ru/v1 (main), https://apihydraai.ru/v1 (Russia)

## Full Generation Script (Python)

```python
import requests, base64, re, sys

API_KEY = "sk-hydra-ai-nvrgdrNBUzHLvUS5pG-It78G0VxNyw79PaD-L3ntf26QrWJOOBhhqCVo4eraFRN7"
BASE_URL = "https://api.hydraai.ru/v1"

def generate_image(prompt: str, output_path: str = "output.png", model: str = "hydra-banana-pro"):
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()

    content = data["choices"][0]["message"]["content"]
    usage = data["usage"]
    print(f"Cost: {usage['cost_request']} RUB | Time: {usage['total_time']}s")

    match = re.search(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)', content)
    if match:
        ext = "jpg" if match.group(1) == "jpeg" else match.group(1)
        img_bytes = base64.b64decode(match.group(2))
        out = output_path if output_path.endswith(f".{ext}") else f"{output_path.rsplit('.', 1)[0]}.{ext}"
        with open(out, "wb") as f:
            f.write(img_bytes)
        print(f"Saved: {out} ({len(img_bytes) // 1024} KB)")
        return out
    else:
        print("No image found in response")
        print(content[:300])
        return None

if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "A beautiful sunset over the ocean, photorealistic, 4k. Aspect ratio: 16:9"
    generate_image(prompt)
```
