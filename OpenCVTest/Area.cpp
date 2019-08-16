#include "stdafx.h"
#include <opencv2\opencv.hpp>
#include "Area.h"
#include "Ball.h"

using namespace cv;

void Area::draw(const Mat & image) const
{
	line(image, Point(observe_x1, 0), Point(observe_x1, height), Scalar(128, 128, 128), 10);
	line(image, Point(observe_x2, 0), Point(observe_x2, height), Scalar(128, 128, 128), 10);
}
bool Area::into_observe(const Ball & ball) const
{
	return ball.center.x >= observe_x1 && ball.center.x <= observe_x2;
}