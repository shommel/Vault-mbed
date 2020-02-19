#ifndef FS_HANDLER_H
#define FS_HANDLER_H 

// mbed os headers
#include "mbed.h"
#include "BlockDevice.h"
#include "LittleFileSystem.h"

class FSHandler {
	public:

		void fs_init();

		FILE *read(char* path);
		void spend_close(FILE *f);
		int get_size(FILE *f);

};

#endif