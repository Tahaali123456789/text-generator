import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# Title for the app
st.title("Text Generation with rhymes-ai/Aria")

# Load the model and tokenizer
@st.cache_resource
def load_model():
    model = AutoModelForCausalLM.from_pretrained("rhymes-ai/Aria", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained("rhymes-ai/Aria", trust_remote_code=True)
    return model, tokenizer

model, tokenizer = load_model()

# Text input box for the user
input_text = st.text_input("Enter text to generate continuation:")

# Generate button
if st.button("Generate"):
    if input_text:
        with st.spinner("Generating..."):
            # Tokenize the input
            inputs = tokenizer(input_text, return_tensors="pt")

            # Generate output
            outputs = model.generate(**inputs)

            # Decode the generated tokens to get the text
            output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Display the output text
            st.subheader("Generated Text:")
            st.write(output_text)
    else:
        st.warning("Please enter some text.")
