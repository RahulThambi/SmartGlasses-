
import cv2
import time
import pyttsx3
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize image captioning model
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def predict_step(image):
    pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds[0]

def capture_image():
    cap = cv2.VideoCapture(0)  # 0 for default camera
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    else:
        print("Error: Could not capture image.")
        return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def describe_scene():
    image = capture_image()
    if image is not None:
        description = predict_step(image)
        print(f"Scene description: {description}")
        speak(f"I see {description}")
    else:
        speak("Sorry, I couldn't capture an image to describe.")

def main():
    print("Starting scene description.")
    speak("Starting scene description.")
    
    describe_scene()
    print("Stopping scene description.")
    speak("Stopping scene description.")

if __name__ == "__main__":
    main()