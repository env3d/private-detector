import inference
from private_detector.utils.preprocess import preprocess_for_evaluation

from flask import Flask, request, jsonify, send_from_directory

inference.tf.get_logger().setLevel('ERROR')
inference.absl_logging.set_verbosity(inference.absl_logging.ERROR)

model = inference.tf.saved_model.load('./saved_model')
def predict(image_b64):

    image = inference.tf.io.decode_base64(image_b64)
    image = inference.tf.io.decode_jpeg(image, channels=3)

    image = preprocess_for_evaluation(
        image,
        480,
        inference.tf.float16
    )

    image = inference.tf.reshape(image, -1)

    preds = model([image])
    return inference.tf.get_static_value(preds[0])[0]


app = Flask(__name__)
@app.route('/api', methods = ['POST', 'GET'])
def index():
    image64 = request.json['image']
    print(image64)
    prob = {'probability': float(predict(image64))}
    return jsonify(prob)

@app.route("/")
def index_html():
    return send_from_directory('static/', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
