from io import BytesIO
from flask import Flask, jsonify, request
from flask_cors import CORS
from diffusers import StableDiffusionXLPipeline
import torch
import base64
import time
from threading import Lock

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

pipe = None
lock = Lock()


def load_pipeline():
    global pipe
    if pipe is None:
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "etri-vilab/koala-700m-llava-cap", torch_dtype=torch.float16
        )
        pipe.to("cuda")


@app.route("/api/v1/text-to-image/", methods=["POST"])
def text_to_image():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    prompt = data.get("prompt")
    negative_prompt = data.get("negative_prompt", "")
    num_inference_steps = data.get("num_inference_steps", "41")
    width = data.get("width", "1024")
    height = data.get("height", "1024")

    try:
        with lock:
            load_pipeline()
            start = time.time()
            images = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=int(num_inference_steps),
                width=int(width),
                height=int(height),
            ).images[0]
            torch.cuda.empty_cache()
            end = time.time()
            print("ELAPSED TIME LOADING IMAGE", end - start)

            # Convert image to base64 string
            buffered = BytesIO()
            images.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return jsonify(
                {
                    "status": "success",
                    "output": img_str,
                }
            )
    except Exception as e:
        print("ERROR", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
