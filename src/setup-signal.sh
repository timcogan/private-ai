# Install the Java Development Kit to run the Signal CLI
sudo apt install -y openjdk-17-jdk

# Rust and other dependencies
# must be installed to build the libsignal library
curl https://sh.rustup.rs -sSf | sh -s -- -y
sudo apt install -y clang libclang-dev cmake

# Build the libsignal.so, required by signal-cli
git clone https://github.com/signalapp/libsignal.git
cd libsignal
cargo build -p libsignal-jni
LIB_SIGNAL_PATH=libsignal/target/debug/libsignal_jni.so
cd ..

SIGNAL_CLI_VERSION=0.11.7
SIGNAL_CLI_URL=https://github.com/AsamK/signal-cli/releases/download/v$SIGNAL_CLI_VERSION/signal-cli-$SIGNAL_CLI_VERSION-Linux.tar.gz
SIGNAL_CLI_LIB=signal-cli/signal-cli-$SIGNAL_CLI_VERSION/lib
mkdir signal-cli
cd signal-cli
curl -L -o signal-cli-$SIGNAL_CLI_VERSION.tar.gz $SIGNAL_CLI_URL
tar -xzf signal-cli-$SIGNAL_CLI_VERSION.tar.gz
cd ..
cp $LIB_SIGNAL_PATH $SIGNAL_CLI_LIB
cd $SIGNAL_CLI_LIB
zip signal-cli-*.jar libsignal_jni.so

echo ""
echo "---------------------------------------------------------------------"
echo ""
echo "Now you must register the number your server will send messages with."
echo ""
echo "./tools/signal-cli/signal-cli-$SIGNAL_CLI_VERSION/bin/signal-cli -a +1XXXYYYZZZZ register"
echo ""
echo "Once you've done this, run 'make'"
