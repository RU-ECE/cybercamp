#include <iostream>
#include <iomanip>
#include <bitset>
using namespace std;
void print2s_complement(int8_t a) {
  bitset<8> b;
	int8_t tmp = -a;
	b = a;
	cout << int(a) << "\t binary=" << b << "\t negated=" << int(tmp);
	b = tmp;
	cout << "\t in binary " << b << '\n';
}

int main() {
	print2s_complement(11);
	print2s_complement(-17);
	print2s_complement(127);
	print2s_complement(-128);
}
