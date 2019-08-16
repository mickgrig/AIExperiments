#pragma once

#include <random>

struct InitConditions
{
	InitConditions() : angle(0), pix_per_sec(350) {}
	unsigned int pix_per_sec; // 250 - 550
	double angle; // +- 7.5 degree (+- 0.13 radian)
	void randomize()
	{
		std::cout << "randomize conditions: ";
		std::random_device rd;
		std::mt19937 mt(rd());
		std::uniform_real_distribution<double> angdist(-0.13, 0.13);
		angle = angdist(mt);
		std::uniform_int_distribution<unsigned int> veldist(250, 550);
		pix_per_sec = veldist(mt);
		std::cout << "angle = " << angle << ", velocity = " << pix_per_sec << std::endl;
	}
};