# Clone alpaca.cpp
git clone https://github.com/antimatter15/alpaca.cpp.git

# Build alpaca.cpp
cd alpaca.cpp && make

# Download model
mkdir models
cd models
mkdir "7B"
cd "7B"
curl -L -o ggml-model-q4_0.bin https://huggingface.co/Pi3141/alpaca-7B-ggml/resolve/main/ggml-model-q4_0.bin
