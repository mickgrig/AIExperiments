#include "stdafx.h"
#include <opencv2\opencv.hpp>
#include "Area.h"
#include "Ball.h"
#include "InitConditions.h"

using namespace cv;

Ball::Ball(const Area & area) : radius(20)
{
	start_init(area);
}
void Ball::start_init(const Area & area)
{
	center.x = 0;
	center.y = area.height / 2;
}
bool Ball::move(const InitConditions & initCond, const Area & area, unsigned int msec_delta)
{
	bool out_of_area = false;
	double distance = ((double)initCond.pix_per_sec / 1000.) * msec_delta;
	auto init_x = center.x;
	auto init_y = center.y;
	auto tempval = distance * sin(initCond.angle);
	double delta_x = distance * cos(initCond.angle);
	double delta_y = distance * sin(initCond.angle);
	center.x += delta_x;
	center.y += delta_y;
	if (center.x > area.width || center.y > area.height || center.y < 0)
	{
		start_init(area);
		out_of_area = true;
	}
	return out_of_area;
}

void Ball::draw(const Mat & image) const
{
	circle(image, center, radius, Scalar(0, 0, 255), -1);
}