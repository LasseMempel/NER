# preload_model.py
print("📥 Pre-downloading GLiNER model...")

from gliner import GLiNER

# Download and save model locally
model = GLiNER.from_pretrained("knowledgator/gliner-x-large")
model.save_pretrained("/app/gliner_model")

print("✅ Model saved to /app/gliner_model")