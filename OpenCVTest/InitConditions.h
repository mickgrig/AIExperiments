#pragma once

#include <random>

struct InitConditions
{
	InitConditions() : angle(-0.26), pix_per_sec(900) {}
	unsigned int pix_per_sec; //
	double angle; // 15 degree = 0.26 radian
	void randomize()
	{
		std::cout << "randomize conditions: ";
		std::random_device rd;
		std::mt19937 mt(rd());
		std::uniform_real_distribution<double> angdist(-0.26, 0);
		angle = angdist(mt);
		std::uniform_int_distribution<unsigned int> veldist(700, 900);
		pix_per_sec = veldist(mt);
		std::cout << "angle = " << angle << ", velocity = " << pix_per_sec << std::endl;
	}
};