#include <iostream>
#include <fstream>
using namespace std;

int main() {
	ofstream f("test.bin");
	f << "hello\n";
	uint32_t a = 65536 + 1;
	uint64_t b = 1 | (1 << 8) | (2 << 16);
	f.write((char*)&a, sizeof(a));
	f.write((char*)&b, sizeof(b));
	float f1 = 3;
	double d = 1.5;
	f.write((char*)&f1, sizeof(float));
	f.write((char*)&d, sizeof(double));
	return 0;
}
