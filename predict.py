import requests
import hashlib
import datetime
import os
import time
import logging
from llava.conversation import (default_conversation, conv_templates,
                                   SeparatorStyle)
import json

logger = logging.getLogger(__name__)

def simple_http_bot(state, model_selector, temperature, top_p, max_new_tokens):
    start_tstamp = time.time()
    model_name = model_selector


    controller_url = "localhost:10000"
    ret = requests.post(controller_url + "/get_worker_address", json={"model": model_name})
    worker_addr = ret.json().get("address", "")

    if not worker_addr:
        return "No available worker. Please try again later."

    prompt = state.get_prompt()
    all_images = state.get_images(return_pil=True)
    all_image_hash = [hashlib.md5(image.tobytes()).hexdigest() for image in all_images]
    for image, hash in zip(all_images, all_image_hash):
        t = datetime.datetime.now()
        filename = os.path.join("LOGDIR", "serve_images", f"{t.year}-{t.month:02d}-{t.day:02d}", f"{hash}.jpg")
        if not os.path.isfile(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            image.save(filename)

    pload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": float(temperature),
        "top_p": float(top_p),
        "max_new_tokens": min(int(max_new_tokens), 1536),
        "stop": state.sep if state.sep_style in [SeparatorStyle.SINGLE, SeparatorStyle.MPT] else state.sep2,
        "images": f'List of {len(state.get_images())} images: {all_image_hash}',
    }
    logger.info(f"==== request ====\n{pload}")

    pload['images'] = state.get_images()
    state.messages[-1][-1] = "▌"

    try:
        response = requests.post(worker_addr + "/worker_generate_stream", headers={}, json=pload, stream=True, timeout=10)
        for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
            if chunk:
                data = json.loads(chunk.decode())
                if data["error_code"] == 0:
                    output = data["text"][len(prompt):].strip()
                    state.messages[-1][-1] = output + "▌"
                else:
                    output = data["text"] + f" (error_code: {data['error_code']})"
                    state.messages[-1][-1] = output
                    return output
                time.sleep(0.03)
    except requests.exceptions.RequestException:
        state.messages[-1][-1] = "Server error. Please try again later."
        return "Server error. Please try again later."

    state.messages[-1][-1] = state.messages[-1][-1][:-1]
    finish_tstamp = time.time()
    logger.info(f"{output}")
    return output

if __name__ == "__main__":
    {'model': 'llava-v1.5-7b', 'prompt': "A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image>\nExplain 1 by 1 all the elements in this image ASSISTANT:", 'temperature': 0.2, 'top_p': 0.7, 'max_new_tokens': 512, 'stop': '</s>', 'images': "List of 1 images: ['b939abf2c4553ce07e642170aee3a3d7']"}
    simple_http_bot()