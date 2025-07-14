from google import genai
from google.genai import types
import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import PIL.Image


key = os.getenv("IMAGEN3_API_SECRET")
client = genai.Client(api_key=key)


text_input = ('Draw it in Ghibli style',)

image = PIL.Image.open("C:/Users/jyes_semin/Desktop/Data/image/test.jpg")


response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=[text_input, image],
    config=types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    image = Image.open(BytesIO((part.inline_data.data)))
    image.show()
    image.save("C:/Users/jyes_semin/Desktop/Data/image/test_g.png")  # ✅ 저장 추가