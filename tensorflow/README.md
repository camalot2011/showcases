# Image Classification with TensorFlow

I performed the image classification analysis on the CIFAR-10 data set. The main file is the `image_classification.ipynb`. The models developed have a gradual increase in the prediction power. The final model with the transfer learning can achieve **86% accuracy** on the test set. All the models are based on the tensorflow in the python. I also applied Keras framework in some of the models. The notebook can be viewed [HERE](https://nbviewer.jupyter.org/github/camalot2011/showcases/blob/master/tensorflow/image_classification.ipynb).

Some key findings are:
- Smallest delta model: using the perceptual formula to calculate the distance. The overall accuracy is poor for this model at only **25.13%**
- Softmax model: continue with the previous model but using the softmax classification instead. Considering the distance with all the 10 typical images increases the accuracy to **28.34%**
- Fully-connected model: the model does have a great improvement over the previous models. The accuracy increases to **39.08 %** on the training set and **41.56 %** on the validation set.
- Convolutional model: the convolutional model does give a great boost in the metics. The accuracy increases to **74.40%** in the training set, and **75.84%** in the validation set.
- Transfer learning model: The transfer learning model using the `GoogLeNet` does a excellent job in predicting the image labels. The accuracy achieves **86.00%** in the training set, and **85.97%** in the validation set!
