import sounddevice as sd
import librosa
import numpy as np
import pickle

# Fungsi untuk merekam audio dari mikrofon
def record_audio(duration=4, sr=22050):
    print("Recording... Speak now!")
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()  # Tunggu hingga rekaman selesai
    print("Recording complete.")
    return audio.flatten(), sr

# Fungsi untuk memuat model yang telah disimpan
def load_saved_model(model_path="voice_recognition_model.pkl"):
    with open(model_path, "rb") as file:
        data = pickle.load(file)
    return data["model"], data["label_encoder"], data["scaler"]

# Fungsi untuk prediksi speaker dari audio input
def predict_audio_from_mic(model, label_encoder, scaler, n_mfcc=13, duration=3):
    try:
        # Rekam audio dari mikrofon
        y, sr = record_audio(duration=duration)
        
        # Ekstraksi fitur MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        features = np.mean(mfcc.T, axis=0)
        
        # Standardisasi fitur
        features_scaled = scaler.transform([features])
        
        # Prediksi speaker
        prediction = model.predict(features_scaled)
        probabilities = model.predict_proba(features_scaled)

        # Decode label
        predicted_label = label_encoder.inverse_transform(prediction)[0]
        confidence = np.max(probabilities) * 100

        return predicted_label, confidence
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None, None

if __name__ == "__main__":
    # Path ke model yang disimpan
    model_path = "voice_recognition_model.pkl"
    
    # Muat model, label encoder, dan scaler
    print("Loading saved model...")
    model, label_encoder, scaler = load_saved_model(model_path)

    # Prediksi suara dari mikrofon
    print("Ready to recognize voice from microphone...")
    predicted_label, confidence = predict_audio_from_mic(model, label_encoder, scaler)

    if predicted_label:
        print(f"Predicted Speaker: {predicted_label}")
        print(f"Confidence: {confidence:.2f}%")
    else:
        print("Failed to predict speaker.")