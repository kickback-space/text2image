from io import BytesIO
from flask import Flask, jsonify, request
from diffusers import StableDiffusionXLPipeline
import torch
import base64
import time

app = Flask(__name__)

pipe = None


if pipe is None:
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "etri-vilab/koala-700m-llava-cap",
        torch_dtype=torch.float16
    )
    # With this setup, we reduce the memory requirement to 15.6GB while reducing the inference latency at the same time.
    # pipe.vae = AutoencoderTiny.from_pretrained("madebyollin/taesdxl", torch_dtype=torch.float16)
    pipe.to("cuda")

def process_image(prompt: str):
    image = pipe(prompt=prompt, width=1024, height=1024).images[0]
    return image

@app.route('/api/v1/text-to-image/', methods=['POST'])
def text_to_image():
    try:
        if request.method == 'POST':
            prompt = request.get_json()['prompt']
            start = time.time() 
            image = process_image(prompt)
            end = time.time()
            print("ELAPSED TIME LOADING PROCESSING IMAGE", end - start)

            # Convert image to base64 string 
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return jsonify({"image": img_str})
    except Exception as e:
        print("ERROR", str(e))
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
