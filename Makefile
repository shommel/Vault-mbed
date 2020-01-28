
.DEFAULT_GOAL := default

# Source files
MBED_DEPS_DOTLIBFILES = f469_lvgl_driver.lib BSP_DISCO_F469NI.lib lvgl-mbed.lib mbed-os.lib QSPI_DISCO_F469NI.lib tiny_lvgl_gui.lib uBitcoin.lib
PROTOBUF_SOURCES = messages-common.proto messages-bitcoin.proto
GIT_SUBMODULES = nanopb

MBED_DEPS = $(basename $(MBED_DEPS_DOTLIBFILES))
PROTOBUF_BASENAMES = $(basename $(PROTOBUF_SOURCES))
PROTOBUF_TARGET_SOURCEFILES = $(addsuffix .pb.c, $(basename $(PROTOBUF_SOURCES))) $(addsuffix .pb.h, $(basename $(PROTOBUF_SOURCES)))
GIT_SUBMODULE_DEPS = $(addsuffix /.git, $(GIT_SUBMODULES))

TARGET = BUILD/DISCO_F469NI/GCC_ARM/Vault-mbed.bin

virtualenv:
	virtualenv -p python3 virtualenv
	. virtualenv/bin/activate; pip install -Ur requirements.txt

VIRTUALENV_ACTIVATE = source

deps: $(MBED_DEPS) $(PROTOBUF_TARGET_SOURCEFILES)

default: $(GIT_SUBMODULE_DEPS) $(MBED_DEPS) $(TARGET)

$(GIT_SUBMODULE_DEPS): .gitmodules
	git submodule init
	git submodule update

$(TARGET): $(MBED_DEPS) $(PROTOBUF_TARGET_SOURCEFILES)
	mbed compile

$(MBED_DEPS): $(MBED_DEPS_DOTLIBFILES)
	mbed deploy

%.pb.h %.pb.c: %.proto virtualenv $(GIT_SUBMODULE_DEPS)
	. virtualenv/bin/activate; \
	protoc --plugin=protoc-gen-nanopb=nanopb/generator/protoc-gen-nanopb --nanopb_out=. $<

clean:
	rm -rf $(MBED_DEPS) $(PROTOBUF_TARGET_SOURCEFILES) __pycache__ BUILD virtualenv

test:
	echo -n $(GIT_SUBMODULE_DEPS)
