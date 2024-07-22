from typing import Any, Tuple
from flask import Flask, request, jsonify, send_from_directory

import tensorflow as tf

tf.get_logger().setLevel('ERROR')


def pad_resize_image(image: tf.Tensor,
                     dims: Tuple[int, int]) -> tf.Tensor:
    """
    Resize image with padding

    Parameters
    ----------
    image : tf.Tensor
        Image to resize
    dims : Tuple[int, int]
        Dimensions of resized image

    Returns
    -------
    image : tf.Tensor
        Resized image
    """
    image = tf.image.resize(
        image,
        dims,
        preserve_aspect_ratio=True
    )

    shape = tf.shape(image)

    sxd = dims[1] - shape[1]
    syd = dims[0] - shape[0]

    sx = tf.cast(
        sxd / 2,
        dtype=tf.int32
    )
    sy = tf.cast(
        syd / 2,
        dtype=tf.int32
    )

    paddings = tf.convert_to_tensor([
        [sy, syd - sy],
        [sx, sxd - sx],
        [0, 0]
    ])

    image = tf.pad(
        image,
        paddings,
        mode='CONSTANT',
        constant_values=128
    )

    return image


def preprocess_for_evaluation(image: tf.Tensor,
                              image_size: int,
                              dtype: tf.dtypes.DType) -> tf.Tensor:
    """
    Preprocess image for evaluation

    Parameters
    ----------
    image : tf.Tensor
        Image to be preprocessed
    image_size : int
        Height/Width of image to be resized to
    dtype : tf.dtypes.DType
        Dtype of image to be used

    Returns
    -------
    image : tf.Tensor
        Image ready for evaluation
    """
    image = pad_resize_image(
        image,
        [image_size, image_size]
    )

    image = tf.cast(image, dtype)

    image -= 128
    image /= 128

    return image

model = tf.saved_model.load('./saved_model')
def predict(image_b64):

    image = tf.io.decode_base64(image_b64)
    image = tf.io.decode_jpeg(image, channels=3)

    image = preprocess_for_evaluation(
        image,
        480,
        tf.float16
    )

    image = tf.reshape(image, -1)

    preds = model([image])
    return tf.get_static_value(preds[0])[0]


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
