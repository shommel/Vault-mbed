
.DEFAULT_GOAL := default

# Dependencies
MBED_DEPS = f469_lvgl_driver BSP_DISCO_F469NI lvgl-mbed mbed-os QSPI_DISCO_F469NI tiny_lvgl_gui uBitcoin
GIT_SUBMODULES = nanopb
NANOPB_SOURCES = pb.h pb_common.c pb_common.h pb_decode.c pb_decode.h pb_encode.c pb_encode.h

# Source files
PROTOFILES = messages-common.proto messages-bitcoin.proto messages-management.proto messages.proto

# Munge some paths
MBED_DEPS_DOTLIBFILES = $(addsuffix .lib, $(MBED_DEPS))
PROTOBUF_BASENAMES = $(basename $(PROTOFILES))
PROTOBUF_TARGET_SOURCEFILES = $(addprefix src/protobuf/, $(addsuffix .pb.c, $(basename $(PROTOFILES))) $(addsuffix .pb.h, $(basename $(PROTOFILES))))
GIT_SUBMODULE_DEPS = $(addsuffix /.git, $(GIT_SUBMODULES))
NANOPB_DEPS = $(addprefix src/nanopb/, $(NANOPB_SOURCES))

# The file that make should build, in the end
TARGET = BUILD/DISCO_F469NI/GCC_ARM/Vault-mbed.bin

virtualenv:
	virtualenv -p python3 virtualenv
	. virtualenv/bin/activate; pip install -Ur requirements.txt

deps: $(MBED_DEPS) $(PROTOBUF_TARGET_SOURCEFILES)

default: $(GIT_SUBMODULE_DEPS) $(MBED_DEPS) $(TARGET)

$(GIT_SUBMODULE_DEPS) $(NANOPB_DEPS): .gitmodules
	git submodule init
	git submodule update
	cd src/nanopb; ln -s $(addprefix ../../nanopb/, $(NANOPB_SOURCES)) .

$(TARGET): $(MBED_DEPS) $(PROTOBUF_TARGET_SOURCEFILES) $(NANOPB_DEPS)
	mbed compile

$(MBED_DEPS): $(MBED_DEPS_DOTLIBFILES)
	mbed deploy

src/protobuf/%.pb.h src/protobuf/%.pb.c: src/%.proto virtualenv $(GIT_SUBMODULE_DEPS)
	. virtualenv/bin/activate; \
	cd src; protoc --plugin=protoc-gen-nanopb=../nanopb/generator/protoc-gen-nanopb --nanopb_out=protobuf $(notdir $<)

clean:
	rm -rf $(MBED_DEPS) $(PROTOBUF_TARGET_SOURCEFILES) $(GIT_SUBMODULES)/* $(GIT_SUBMODULES)/.[a-z0-9]* __pycache__ BUILD virtualenv *.pyc src/nanopb/*

test: $(NANOPB_DEPS)
	echo $(GIT_SUBMODULE_DEPS)
