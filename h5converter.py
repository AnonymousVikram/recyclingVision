# Import keras2onnx and onnx
import onnx
import keras2onnx
import tensorflow as tf
 
# Load the keras model
model = tf.keras.models.load_model('/Users/anonymousvikram/Downloads/model18.h5')
 
# Convert it into onnx
onnx_model = keras2onnx.convert_keras(model, model.name)
 
# Save the model as flower.onnx
onnx.save_model(onnx_model, 'kerasModel.onnx')