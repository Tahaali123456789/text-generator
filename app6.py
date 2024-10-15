import streamlit as st
import requests
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor

# Title of the app
st.title("Image and Text Generation with rhymes-ai/Aria")

# Load the model and processor
@st.cache_resource
def load_model():
    model_id_or_path = "rhymes-ai/Aria"
    model = AutoModelForCausalLM.from_pretrained(model_id_or_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
    processor = AutoProcessor.from_pretrained(model_id_or_path, trust_remote_code=True)
    return model, processor

model, processor = load_model()

# User uploads image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Text input from the user
input_text = st.text_input("Enter your question about the image:")

# Process image if uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Generate button
if st.button("Generate Response") and uploaded_file is not None and input_text:
    with st.spinner("Processing..."):
        # Convert user input into messages format
        messages = [
            {
                "role": "user",
                "content": [
                    {"text": None, "type": "image"},
                    {"text": input_text, "type": "text"},
                ],
            }
        ]

        # Apply processor
        text = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(text=text, images=image, return_tensors="pt")
        inputs["pixel_values"] = inputs["pixel_values"].to(model.dtype)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        # Generate model output
        with torch.inference_mode(), torch.cuda.amp.autocast(dtype=torch.bfloat16):
            output = model.generate(
                **inputs,
                max_new_tokens=500,
                stop_strings=["<|im_end|>"],
                tokenizer=processor.tokenizer,
                do_sample=True,
                temperature=0.9,
            )

        # Decode the output
        output_ids = output[0][inputs["input_ids"].shape[1]:]
        result = processor.decode(output_ids, skip_special_tokens=True)

        # Display the result
        st.subheader("Generated Response:")
        st.write(result)
else:
    st.write("Please upload an image and enter a question to generate a response.")
