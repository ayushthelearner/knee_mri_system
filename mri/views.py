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
model = tf.keras.models.load_model('models/cnn_model.h5')  # Update this path to where you saved your model


# def upload_image(request):
    
    
    
    


#     if request.method == 'POST':
#         form = MRIImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             mri_image = form.save()
#             mri_image.user = request.user  # Assign the logged-in user


#             # Get the file path of the uploaded image from the 'image' field
#             image_path = mri_image.image.path  # Ensure this is the correct path for your uploaded images
#             print(f"Image path: {image_path}")
            
#             try:
#                 # Load and preprocess the image
#                 img = Image.open(image_path)
#                 img = img.convert('L')  # Convert to grayscale (1 channel)
#                 img = img.resize((93, 1))  # Resize to 93x1 to match the input shape
#                 img_array = np.array(img).flatten()  # Flatten the image to a 1D array
#                 img_array = img_array / 255.0  # Normalize the image values
#                 img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (shape: [1, 93])

#                 # Pass the image to the model for prediction
#                 result = model.predict(img_array)  # This will return the predicted result
#                 print(f"Prediction result: {result}")

#                 # Optionally, map the result to a human-readable format
#                 predicted_class = np.argmax(result, axis=-1)  # For classification models
#                 mri_image.result = f"Analysis Result: Class {predicted_class[0]}"  # Update the result field
#                 mri_image.save()

#                 # Redirect to the result page with the result
#                 return redirect('result', pk=mri_image.pk)
#             except Exception as e:
#                 # Handle any image processing or prediction errors
#                 print(f"Error processing image: {e}")
#                 mri_image.result = f"Error processing image: {e}"
#                 mri_image.save()
#                 return redirect('result', pk=mri_image.pk)

#     else:
#         form = MRIImageForm()

#     return render(request, 'upload.html', {'form': form})



# this


import cv2

# Model is already globally loaded like:
model = tf.keras.models.load_model('models/cnn_model.h5')

def preprocess_image_for_cnn(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found or cannot be read.")
    
    img = cv2.resize(img, (64, 64))
    img = img / 255.0  # Normalize
    img = img.reshape(1, 64, 64, 1)  # CNN expects 4D input: (batch, height, width, channels)
    return img

def upload_image(request):
    if request.method == 'POST':
        form = MRIImageForm(request.POST, request.FILES)
        if form.is_valid():
            mri_image = form.save(commit=False)
            mri_image.user = request.user
            mri_image.save()

            image_path = mri_image.image.path
            print(f"Image path: {image_path}")

            try:
                # Preprocess and predict
                img_array = preprocess_image_for_cnn(image_path)
                result = model.predict(img_array)
                print(f"Prediction result: {result}")

                predicted_class = np.argmax(result, axis=-1)
                mri_image.result = f"Analysis Result: Class {predicted_class[0]}"
                mri_image.save()

                return redirect('result', pk=mri_image.pk)

            except Exception as e:
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






# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth.hashers import make_password
# from .forms import CustomUserCreationForm

# this 

# def user_register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = make_password(form.cleaned_data['password'])  # Hash password
#             user.save()
#             messages.success(request, "User registered successfully. Please log in.")
#             return redirect('user_login')  # Redirect to login page
#     else:
#         form =CustomUserCreationForm()

#     return render(request, 'user_register.html', {'form': form})

# this


# def user_register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'User registered successfully. Please log in.')
#             return redirect('user_login')  # Replace 'user_login' with your actual login URL name
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'user_register.html', {'form': form})



# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages

# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             # messages.success(request, "Login successful.")
            
#             storage = messages.get_messages(request)
#             storage.used = True
#             return redirect('home')  # Redirect to dashboard after login
#         else:
#             messages.error(request, "Invalid username or password.")
    
#     return render(request, 'user_login.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser  # Use CustomUser instead of User
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Ensure password is hashed
            user.save()
            messages.success(request, 'User registered successfully. Please log in.')
            return redirect('user_login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'user_login.html')


from django.http import HttpResponseRedirect
from django.urls import reverse

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')  # Redirect to login page
    
    # return HttpResponseRedirect(reverse("user_login"))




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Hospital
from .forms import HospitalForm

@login_required
def dashboard(request):
    hospital = Hospital.objects.filter(user=request.user).first()  # Fetch the user's hospital

    if request.method == "POST":
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.user = request.user  # Assign the logged-in user
            hospital.save()
            return redirect('dashboard')  # Refresh page after saving
    else:
        form = HospitalForm(instance=hospital)

    return render(request, 'dashboard.html', {'hospital': hospital, 'form': form})


@login_required
def update_hospital(request):
    hospital = Hospital.objects.filter(user=request.user).first()

    if not hospital:
        return redirect('dashboard')  # Redirect if no hospital exists

    if request.method == "POST":
        form = HospitalForm(request.POST, request.FILES, instance=hospital)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect after updating
    else:
        form = HospitalForm(instance=hospital)

    return render(request, 'update_hospital.html', {'form': form})



from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def delete_hospital(request):
    hospital = get_object_or_404(Hospital, user=request.user)
    
    if request.method == "POST":
        hospital.delete()
        messages.success(request, "Hospital deleted successfully.")
        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def register_hospital(request):
    if request.method == "POST":
        form = HospitalForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.user = request.user  # Assign current user
            hospital.save()
            return redirect('dashboard')  # Redirect to dashboard after registering
    else:
        form = HospitalForm()

    return render(request, 'register_hospital.html', {'form': form})




from django.contrib.auth import logout

# def home(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')  # Send logged-in users to dashboard
    
#     logout(request)  # Force logout on first visit
#     return redirect('user_login')  # Send them to login page




def home(request):
    return render(request, 'home.html')  # Make sure your template is named 'home.html'



@login_required
def mri_history(request):
    mri_images = MRIImage.objects.filter(user=request.user).order_by('-uploaded_at')  # Fetch only current user's images
    return render(request, 'mri_history.html', {'mri_images': mri_images})
