#pragma once

struct Ball;
struct Area
{
	Area() : width(1600), height(900), observe_x1(width / 3), observe_x2(2 * width / 3) {}
	unsigned int width, height;
	unsigned int observe_x1, observe_x2;
	void draw(const cv::Mat & image) const;
	bool into_observe(const Ball &) const;
};