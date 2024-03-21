from io import BytesIO
from flask import Flask, jsonify, request
from diffusers import StableDiffusionXLPipeline
import torch
import base64

app = Flask(__name__)


@app.route('/api/v1/text-to-image/', methods=['GET', 'POST'])
def text_to_image():
    try:
        pipe = StableDiffusionXLPipeline.from_pretrained("etri-vilab/koala-700m-llava-cap", torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        if request.method == 'POST':
            prompt = request.get_json()['prompt']
            image = pipe(prompt=prompt, width=1024, height=1024).images[0]

            # Convert image to base64 string
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return jsonify({"image": img_str})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "Method not allowed"}), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
