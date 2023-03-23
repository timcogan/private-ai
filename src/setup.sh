# We will keep the Signal and AI CLIs here
mkdir tools
cd tools

# Setup the large language model (LLM)
bash ../src/setup-ai.sh

# Setup the Signal CLI for messaging
bash ../src/setup-signal.sh
