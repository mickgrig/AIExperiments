#include "stdafx.h"
#include <opencv2\opencv.hpp>
#include "Racket.h"
#include "Area.h"
#include "Ball.h"
#include <opencv2\highgui.hpp>
#include <opencv2\imgproc\imgproc.hpp>

using namespace cv;
using namespace std;

Racket::Racket(const Area & _area, const Ball & ball) : 
	pos_y(area.height / 2), len(2 * ball.radius), area(_area), step(0), target_y(0)
{
}

void Racket::draw(const Mat & image) const
{
	auto begpt = Point2d(area.width, top());
	auto endpt = Point2d(area.width, bottom());
	line(image, begpt, endpt, Scalar(0, 255, 0), 10);
	circle(image, Point2d(area.width, target_y), 3, Scalar(0, 0, 255), -1);
}

void Racket::move(const Area & area)
{
	if (top() + step >= 0 && bottom() + step <= area.height)
	{
		if (pos_y < target_y && pos_y + step <= target_y ||
			pos_y > target_y && pos_y + step >= target_y)
			pos_y += step;
	}
}

double Racket::top() const
{
	return pos_y - len / 2;
}

double Racket::bottom() const
{
	return pos_y + len / 2;
}

void Racket::observed(shared_ptr<Point2d> ball_center_ptr, unsigned int delta_ms)
{
	if (ball_center_ptr)
		ball_snapshots.push_back(*ball_center_ptr);
	else
	{
		if (!ball_snapshots.empty())
		{
			estimate_target(delta_ms);
			ball_snapshots.clear();
		}
	}
}

void Racket::estimate_target(unsigned int delta_ms)
{
	if (ball_snapshots.size() > 1)
	{
		auto pt1 = ball_snapshots.front();
		auto pt2 = ball_snapshots.back();
		auto delta_y = (area.width - pt2.x) * (pt2.y - pt1.y) / (pt2.x - pt1.x);
		target_y = pt2.y + delta_y;
		auto dx = (pt2.x - pt1.x) / ball_snapshots.size();
		auto rest_x = area.width - pt2.x;
		auto step_count = (rest_x / dx) - 3;
		step = (target_y - pos_y) / step_count;
	}
}