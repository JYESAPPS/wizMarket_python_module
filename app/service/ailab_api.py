import os, asyncio
import httpx

AILAB_CREATE_URL = "https://www.ailabapi.com/api/image/effects/ai-anime-generator"
AILAB_QUERY_URL  = "https://www.ailabapi.com/api/common/query-async-task-result"

# aiLab Tools 필터 API
async def filter_image(image_bytes: bytes, filename: str, content_type: str = "image/png",
                       index: int = 0, api_key: str | None = None) -> tuple[bytes, str]:
    """
    AILabTools 'AI Anime Generator' 적용.
    index=0 -> Vintage Comic
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
        r = await client.post(AILAB_CREATE_URL, headers=headers, data=data, files=files)
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


if __name__ == "__main__":
    import argparse, asyncio, os, mimetypes, os.path as op

    parser = argparse.ArgumentParser(description="Run AILabTools anime_effect locally")
    parser.add_argument("--inp", required=True, help="input image path")
    parser.add_argument("--out", default="out.jpg", help="output image path")
    parser.add_argument("--index", type=int, default=0, help="style index (0=Vintage Comic)")
    args = parser.parse_args()

    if not os.getenv("AILAB_API_KEY"):
        raise SystemExit("Set AILAB_API_KEY first (e.g., set AILAB_API_KEY=xxx)")

    with open(args.inp, "rb") as f:
        img_bytes = f.read()

    mime = mimetypes.guess_type(args.inp)[0] or "image/jpeg"

    async def _run():
        out_bytes, out_mime = await filter_image(
            image_bytes=img_bytes,
            filename=op.basename(args.inp),
            content_type=mime,
            index=args.index
        )
        with open(args.out, "wb") as g:
            g.write(out_bytes)
        print(f"✓ saved: {args.out} ({out_mime})")

    asyncio.run(_run())
