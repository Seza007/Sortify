import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
import os

# Define paths
model_dir = "/home/sesha/Documents/bot/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model"
output_path = "/home/sesha/Documents/bot/ssd_mobilenet_v2_320x320_coco17_tpu-8/frozen_inference_graph.pb"

# Load the model
model = tf.saved_model.load(model_dir)

# Get the inference function
concrete_func = model.signatures["serving_default"]

# Convert to a frozen graph
frozen_func = convert_variables_to_constants_v2(concrete_func)
frozen_graph_def = frozen_func.graph.as_graph_def()

# Save the frozen graph
with tf.io.gfile.GFile(output_path, "wb") as f:
    f.write(frozen_graph_def.SerializeToString())

print(f"✅ Frozen inference graph saved at: {output_path}")
