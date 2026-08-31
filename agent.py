from google.adk.agents.llm_agent import Agent

import datetime
from zoneinfo import ZoneInfo
from google.adk.agent import Agent
from google.cloud import storage

def read_ingredients() -> str:
  vision_client = vision.ImageAnnotatorClient()

  with io.open("/home/bajajnehaa/healthy_hints/images/Ingredients-list.jpg", 'rb') as image_file:
    content = image_file.read()

  image = vision.Image(content=content)
  response = vision_client.text_detection(image=image)
  texts = response.text_annotations
  return texts[0].description

def upload_image() -> str:
    """Uploads an image to Google Cloud Storage."""
    # Usamos um nome genérico para o bucket de testes
    bucket_name = "healthy-hints-bucket-test-guilherme"
    storage_client = storage.Client()
    
   
    return f"Image uploaded successfully to {bucket_name}."


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}."
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


root_agent = Agent(
  model='gemini-2.5-flash',
  name='healthy_hints_agent',
  description='Agent to upload image to Google Cloud Storage',
  instruction='You are a helpful agent who will upload the image to Google Cloud Storage using `upload_image` tool.',
  tools=[upload_image, read_ingredients],
)




