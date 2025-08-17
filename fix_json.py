import chardet

# Step 1: Detect encoding
with open("data.json", "rb") as f:
    raw = f.read()
    result = chardet.detect(raw)
    encoding = result["encoding"]
    print("Detected encoding:", encoding)

# Step 2: Convert to UTF-8
with open("data.json", "r", encoding=encoding, errors="ignore") as f:
    content = f.read()

with open("data_clean.json", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ File converted to UTF-8 -> data_clean.json")
