from io import BytesIO
from flask import Flask, jsonify, request
from diffusers import StableDiffusionXLPipeline
import torch
import base64
import time

app = Flask(__name__)

pipe = None


def load_pipeline():
    global pipe
    if pipe is None:
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "etri-vilab/koala-700m-llava-cap",
            torch_dtype=torch.float16
        )
        # With this setup, we reduce the memory requirement to 15.6GB while reducing the inference latency at the same time.
        # pipe.vae = AutoencoderTiny.from_pretrained("madebyollin/taesdxl", torch_dtype=torch.float16)
        pipe.to("cuda")

def process_image(**kwargs):
    load_pipeline()
    images = pipe(**kwargs).images

    torch.cuda.empty_cache()
    return images

@app.route('/api/v1/text-to-image/', methods=['POST'])
def text_to_image():
    try:
        if request.method == 'POST':
            data = request.get_json()
            prompt = data.get('prompt')
            negative_prompt = data.get('negative_prompt', '')
            num_inference_steps = data.get('num_inference_steps', 41)
            width = data.get('width', 1024)
            height = data.get('height', 1024)
            start = time.time() 
            images = process_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                width=width,
                height=height
                )
            end = time.time()
            print("ELAPSED TIME LOADING IMAGE", end - start)

            # Convert image to base64 string
            img_strs = []
            for image in images:
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                img_strs.append(img_str)
            return jsonify({"images": img_strs})
    except Exception as e:
        print("ERROR", str(e))
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
