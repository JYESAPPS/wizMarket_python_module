import base64
import os, asyncio
import httpx

AILAB_FILTER_URL = "https://www.ailabapi.com/api/image/effects/ai-anime-generator"
AILAB_QUERY_URL  = "https://www.ailabapi.com/api/common/query-async-task-result"
AILAB_COLORIZE_URL = "https://www.ailabapi.com/api/image/effects/image-colorization" 

# aiLab Tools 필터 API
async def filter_image(image_bytes: bytes, filename: str, content_type: str = "image/png",
                       index: int = 0, api_key: str | None = None) -> tuple[bytes, str]:
    """
    AILabTools 'AI Cartoon Generator' 적용 (index=0 -> Vintage Comic).
    return: (image_bytes, mime_type)
    """
    key = api_key or os.getenv("AILAB_API_KEY")
    if not key:
        raise RuntimeError("AILAB_API_KEY not set")

    headers = {"ailabapi-api-key": key}
    data    = {"task_type": "async", "index": str(index)}
    files   = {"image": (filename or "upload.png",
                         image_bytes,
                         content_type or "application/octet-stream")}

    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1) 작업 생성
        r = await client.post(AILAB_FILTER_URL, headers=headers, data=data, files=files)
        j = r.json()
        if j.get("error_code") != 0 or not j.get("task_id"):
            raise RuntimeError(f"AILab create error: {j}")
        task_id = j["task_id"]

        # 2) 결과 폴링 (최대 약 20초)
        result_url = None
        for _ in range(10):
            q = await client.get(AILAB_QUERY_URL, headers=headers, params={"task_id": task_id})
            qj = q.json()
            if qj.get("error_code") == 0 and qj.get("task_status") == 2:
                result_url = (qj.get("data") or {}).get("result_url")
                break
            await asyncio.sleep(2)

        if not result_url:
            raise RuntimeError("AILab timeout")

        # 3) 결과 이미지 다운로드
        img = await client.get(result_url)
        return img.content, img.headers.get("content-type", "image/png")

# 채색 API
async def color_image(image_bytes: bytes, filename: str, content_type: str = "image/png",
                         api_key: str | None = None) -> tuple[bytes, str]:
    """
    AILabTools 'AI Photo Colorize' 적용.
    응답 본문에 base64 'image' 가 들어오므로 디코딩 후 바이너리 반환.
    return: (image_bytes, mime_type)
    """
    key = api_key or os.getenv("AILAB_API_KEY")
    if not key:
        raise RuntimeError("AILAB_API_KEY not set")

    headers = {"ailabapi-api-key": key}
    files = {"image": (filename or "upload.png",
                       image_bytes,
                       content_type or "application/octet-stream")}

    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(AILAB_COLORIZE_URL, headers=headers, files=files)
        r.raise_for_status()
        j = r.json()
        if j.get("error_code") != 0 or not j.get("image"):
            raise RuntimeError(f"AILab colorize error: {j}")

        try:
            img_bytes = base64.b64decode(j["image"])
        except Exception as e:
            raise RuntimeError(f"Failed to decode base64 image: {e}")

        # 문서에 출력 MIME이 명시되지 않음 → PNG로 저장 권장
        return img_bytes, "image/png"


# 실행
if __name__ == "__main__":
    import argparse, asyncio, os, mimetypes, os.path as op

    parser = argparse.ArgumentParser(description="Run AILabTools locally (CMD env only)")
    parser.add_argument("--mode", choices=["filter", "color"], default="filter",
                        help="filter: AI Cartoon (index 사용), color: AI Photo Color")
    parser.add_argument("--inp", required=True, help="input image path")
    parser.add_argument("--out", default="out.png", help="output image path")
    parser.add_argument("--index", type=int, default=0,
                        help="(filter 전용) style index (0=Vintage Comic)")
    args = parser.parse_args()

    # CMD에서: set AILAB_API_KEY=YOUR_KEY
    api_key = os.getenv("AILAB_API_KEY")
    if not api_key:
        raise SystemExit(
            "AILAB_API_KEY not set.\n"
            "Run in CMD (not PowerShell):\n"
            '  set AILAB_API_KEY=YOUR_KEY\n'
            '  python app\\service\\ailab_api.py --mode filter --inp "C:\\path\\img.jpg" --out out.png --index 0'
        )

    with open(args.inp, "rb") as f:
        img_bytes = f.read()
    mime = mimetypes.guess_type(args.inp)[0] or "image/jpeg"

    async def _run():
        if args.mode == "filter":
            out_bytes, out_mime = await filter_image(
                image_bytes=img_bytes,
                filename=op.basename(args.inp),
                content_type=mime,
                index=args.index,
                api_key=api_key,
            )
        else:  # color
            out_bytes, out_mime = await color_image(
                image_bytes=img_bytes,
                filename=op.basename(args.inp),
                content_type=mime,
                api_key=api_key,
            )
        with open(args.out, "wb") as g:
            g.write(out_bytes)
        print(f"✓ saved: {args.out} ({out_mime})")

    asyncio.run(_run())
