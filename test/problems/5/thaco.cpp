#include <bits/stdc++.h>
#define FAILSTR "FAIL_STR!"

//ชุดคำสั่งที่ใช้ในการส่งผลตรวจคำตอบ
//กรณีถูกบางส่วน
void pc(double score) {
	std::cout << std::fixed << score << std::endl;
	std::cerr << "translate:partial" << std::endl;
	exit(0);
}

//กรณีผิด
void wa() {
	std::cout << "0.0" << std::endl;
	std::cerr << "translate:wrong" << std::endl;
	exit(0);
}

//กรณีถูก
void ok() {
	std::cout << "1.0" << std::endl;
	std::cerr << "translate:success" << std::endl;
	exit(0);
}

// ชุดคำสั่งอ่าน string จาก stream
std::string readWord(std::istream& in) {
	std::string out;
	if (in >> out) return out;
	else return FAILSTR;
}

// ชุดคำสั่งอ่าน int จาก stream
int readInt(std::istream& in, int mn = INT_MIN, int mx = INT_MAX) {
	int tmp;
	in >> tmp;
	if (tmp < mn || tmp > mx) {
		wa();
	}
	return tmp;
}


int main(int argc, char* argv[]) {
	std::ifstream inf(argv[1]); //อ่าน .in ไฟล์จาก argv ข้อที่ 1
	std::ifstream ans(argv[2]); //อ่าน .sol ไฟล์จาก argv ข้อที่ 2 (ที่เป็นคำตอบที่ถูก)
	std::ifstream ouf(argv[3]); //อ่าน output ที่ Output ออกมาในข้อที่ 3

	int num = readInt(ouf);
	if (num == 0) {
		wa();
	}
	else if (num == 100) {
		ok();
	}
	else if (num == 69) {
		std::cout << "NOICE" << std::endl;
		ok();
	}
	else if (num == 37) {
		while (true);
	}
	else if (num > 100) {
		return 1;
	}
	else {
		pc((double)num / 100.0);
	}
}