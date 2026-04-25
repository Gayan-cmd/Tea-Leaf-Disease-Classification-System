# 🍃 Tea Leaf Disease Classification System

A deep learning-based image classification system for identifying diseases in tea leaves. This project compares two state-of-the-art CNN architectures — **ResNet50** and **VGG16** — to classify tea leaf images into three disease categories.


## 🔍 Overview

Tea leaf diseases cause significant losses in tea production worldwide. Early and accurate detection is critical for timely treatment and crop protection. This project applies **transfer learning** with pretrained CNN models to automate disease classification from leaf images, reducing reliance on manual expert inspection.

Two convolutional neural network architectures are benchmarked:

| Model     | Pretrained On | Parameters |
|-----------|---------------|------------|
| ResNet50  | ImageNet      | ~25M       |
| VGG16     | ImageNet      | ~138M      |

---

## 🌿 Dataset

The dataset consists of **368 labeled tea leaf images** organized into **3 disease categories**:

| Class        | Description                                      |
|--------------|--------------------------------------------------|
| `algal_leaf` | Caused by *Cephaleuros virescens* — produces orange-red spots |
| `brown_blight`| A fungal disease causing brownish leaf lesions  |
| `white_spot` | Causes white circular spots on the leaf surface  |

### Data Split (Stratified)

| Split      | Count | Proportion |
|------------|-------|------------|
| Training   | 220   | 60%        |
| Validation | 74    | 20%        |
| Test       | 74    | 20%        |

### Data Augmentation (Training Only)

To improve generalization, the following augmentations were applied during training:

- Random horizontal flip (p=0.5)
- Random vertical flip (p=0.2)
- Random rotation (±20°)
- Color jitter (brightness, contrast, saturation)
- Resize to 224×224
- Normalized using **ImageNet mean & std** (`[0.485, 0.456, 0.406]`, `[0.229, 0.224, 0.225]`)

---

## 🧠 Models

Both models use **pretrained ImageNet weights** and are fine-tuned for the 3-class tea leaf disease classification task.

### ResNet50
- Deep residual network with skip connections
- 50 layers deep


### VGG16
- Classic deep convolutional network with 16 layers
- Simple sequential architecture


## 📝 License

This project is developed for academic purposes as part of a Deep Learning assignment.
