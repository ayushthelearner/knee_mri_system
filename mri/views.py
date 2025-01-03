from django.shortcuts import render

# Create your views here.

# from django.shortcuts import render, redirect
# from .forms import MRIImageForm
# from .models import MRIImage

# def upload_image(request):
#     if request.method == 'POST':
#         form = MRIImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             mri_image = form.save()
#             # Call your detection model here
#             mri_image.result = "Analysing with the help of model"  # Replace with actual result
#             mri_image.save()
#             return redirect('result', pk=mri_image.pk)
#     else:
#         form = MRIImageForm()
#     return render(request, 'upload.html', {'form': form})

import tensorflow as tf
import numpy as np
from PIL import Image
from django.shortcuts import render, redirect
from .forms import MRIImageForm
from .models import MRIImage

# Load the model (ensure it's loaded only once to avoid reloading on every request)
model = tf.keras.models.load_model('models/my_model.h5')  # Update this path to where you saved your model

def upload_image(request):
    if request.method == 'POST':
        form = MRIImageForm(request.POST, request.FILES)
        if form.is_valid():
            mri_image = form.save()

            # Get the file path of the uploaded image from the 'image' field
            image_path = mri_image.image.path  # Ensure this is the correct path for your uploaded images
            print(f"Image path: {image_path}")
            
            try:
                # Load and preprocess the image
                img = Image.open(image_path)
                img = img.convert('L')  # Convert to grayscale (1 channel)
                img = img.resize((93, 1))  # Resize to 93x1 to match the input shape
                img_array = np.array(img).flatten()  # Flatten the image to a 1D array
                img_array = img_array / 255.0  # Normalize the image values
                img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (shape: [1, 93])

                # Pass the image to the model for prediction
                result = model.predict(img_array)  # This will return the predicted result
                print(f"Prediction result: {result}")

                # Optionally, map the result to a human-readable format
                predicted_class = np.argmax(result, axis=-1)  # For classification models
                mri_image.result = f"Analysis Result: Class {predicted_class[0]}"  # Update the result field
                mri_image.save()

                # Redirect to the result page with the result
                return redirect('result', pk=mri_image.pk)
            except Exception as e:
                # Handle any image processing or prediction errors
                print(f"Error processing image: {e}")
                mri_image.result = f"Error processing image: {e}"
                mri_image.save()
                return redirect('result', pk=mri_image.pk)

    else:
        form = MRIImageForm()

    return render(request, 'upload.html', {'form': form})







def result(request, pk):
    mri_image = MRIImage.objects.get(pk=pk)
    return render(request, 'result.html', {'mri_image': mri_image})