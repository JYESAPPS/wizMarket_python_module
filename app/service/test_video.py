import os
import time
from google import genai
from google.genai import types

def generate_video_test(prompt: str, aspect_ratio: str = "16:9"):
    try:
        try:
            # key = os.getenv("GENAI_API_KEY")
            key = "AIzaSyCkv_7ZwGTxAMDKiOa5lcB5j9-3J0XWoPA"
            client = genai.Client(api_key=key)
            print(f"⏳ Generating video with aspect_ratio: {aspect_ratio}")

            operation = client.models.generate_videos(
                model="veo-2.0-generate-001",
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    person_generation="allow_adult",  # 또는 "allow_adult"
                    aspect_ratio=aspect_ratio,        # "16:9" or "9:16"
                    numberOfVideos=2,
                    durationSeconds=8
                ),
            )

            # ✅ 비동기 작업 완료 대기
            while not operation.done:
                print("⏳ Waiting for video generation to complete...")
                time.sleep(20)
                operation = client.operations.get(operation)

            # ✅ 결과 처리
            video_paths = []
            for n, generated_video in enumerate(operation.response.generated_videos):
                filename = f"video{n}.mp4"
                client.files.download(file=generated_video.video)
                generated_video.video.save(filename)
                print(f"✅ 비디오 저장 완료: {filename}")
                video_paths.append(filename)

            return {"videos": video_paths}

        except Exception as e:
            error_msg = f"🚨 비디오 생성 중 오류 발생 (내부): {str(e)}"
            print(error_msg)
            return {"error": error_msg}

    except Exception as e:
        return {"error": f"비디오 생성 중 외부 오류 발생: {e}"}


if __name__=="__main__":
    generate_video_test("Pixar-style 3D animated illustration of a young woman and a young man same height, softly waved platinum blonde hair and expressive brown eyes standing in side profile beside a man in a softly lit living room. they are emotionally discussing their disagreements.")