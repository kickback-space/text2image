from flask import Flask, jsonify, request
from diffusers import StableDiffusionXLPipeline
import torch

app = Flask(__name__)


@app.route('/api/v1/text-to-image/', methods=['GET', 'POST'])
def text_to_image():
    pipe = StableDiffusionXLPipeline.from_pretrained("etri-vilab/koala-700m-llava-cap", torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    if request.method == 'POST':
        prompt = request.get_json()['prompt']
        image = pipe(prompt=prompt, width=1024, height=1024).images[0]
        return jsonify({"image": image})
    return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
