// file_reading.cpp : Defines the entry point for the console application.
//

#include <SDKDDKVer.h>
#include <Windows.h>
#include <stdio.h>
#include <tchar.h>

int main(int argc, char* argv[])
{
	int sleep_time = 10;
	int loop_count = 60;
	int		shmem_size = 16;  // 16byte
	HANDLE	shmem = INVALID_HANDLE_VALUE;
	HANDLE	mutex = INVALID_HANDLE_VALUE;

	mutex = ::CreateMutex(NULL, FALSE, _T("mutex_sample_name"));

	shmem = ::CreateFileMapping(
		INVALID_HANDLE_VALUE,
		NULL,
		PAGE_READWRITE,
		0,
		shmem_size,
		_T("shared_memory_name")
		);

	char *buf = (char*)::MapViewOfFile(shmem, FILE_MAP_ALL_ACCESS, 0, 0, shmem_size);


	for (unsigned int c = 0; c < loop_count; ++c) {
		// mutex lock
		WaitForSingleObject(mutex, INFINITE);

		// write shared memory
		memset(buf, c, shmem_size);

		printf("write shared memory...c=%d\n", c);

		// mutex unlock
		::ReleaseMutex(mutex);

		::Sleep(sleep_time);
	}

	// release
	::UnmapViewOfFile(buf);
	::CloseHandle(shmem);
	::ReleaseMutex(mutex);

	return 0;
}