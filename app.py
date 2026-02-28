import gradio as gr
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

def predict(area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning):
    payload = {
        "area": float(area),
        "bedrooms": int(bedrooms),
        "bathrooms": int(bathrooms),
        "stories": int(stories),
        "mainroad": bool(mainroad == "Yes"),
        "guestroom": bool(guestroom == "Yes"),
        "basement": bool(basement == "Yes"),
        "hotwaterheating": bool(hotwaterheating == "Yes"),
        "airconditioning": bool(airconditioning == "Yes")
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        price = data.get("predicted_price", 0)
        return f"### Estimated Price: ${price:,.2f}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to API: {e}"

# Build the Gradio interface
with gr.Blocks(title="House Price Estimator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏡 House Price Estimator")
    gr.Markdown("Enter the details of a house below to get an estimated market price based on our Machine Learning model.")
    
    with gr.Row():
        with gr.Column():
            area = gr.Number(label="Area (sq ft)", value=5000)
            bedrooms = gr.Slider(minimum=1, maximum=10, step=1, label="Bedrooms", value=3)
            bathrooms = gr.Slider(minimum=1, maximum=5, step=1, label="Bathrooms", value=2)
            stories = gr.Slider(minimum=1, maximum=5, step=1, label="Stories", value=2)
        
        with gr.Column():
            mainroad = gr.Radio(["Yes", "No"], label="Main Road Access", value="Yes")
            guestroom = gr.Radio(["Yes", "No"], label="Guest Room", value="No")
            basement = gr.Radio(["Yes", "No"], label="Basement", value="No")
            hotwaterheating = gr.Radio(["Yes", "No"], label="Hot Water Heating", value="No")
            airconditioning = gr.Radio(["Yes", "No"], label="Air Conditioning", value="Yes")

    predict_btn = gr.Button("Predict Price", variant="primary")
    output = gr.Markdown(label="Prediction Result")
    
    predict_btn.click(
        fn=predict,
        inputs=[area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
