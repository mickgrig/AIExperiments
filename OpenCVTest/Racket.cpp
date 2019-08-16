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
	pos_y(area.height / 2), len(2 * ball.radius), area(_area), step(0), target_y(0),
	linear(false)
{
}

void Racket::draw(const Mat & image) const
{
	auto begpt = Point2d(area.width, top());
	auto endpt = Point2d(area.width, bottom());
	line(image, begpt, endpt, Scalar(0, 255, 0), 10);
	circle(image, Point2d(area.width, target_y), 3, Scalar(0, 0, 255), -1); //точка притяжения для ракетки
	String racket_est = (linear ? "linear" : "ballistic");
	putText(image, String("Racket mode: ") + racket_est, Point(10, 90), FONT_HERSHEY_SIMPLEX, 0.7, Scalar(255, 255, 255));
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
	//estimate_target_linear(delta_ms);
	estimate_target_ballistic(delta_ms);
}

void Racket::estimate_target_linear(unsigned int delta_ms)
{
	if (ball_snapshots.size() > 1)
	{
		auto pt1 = ball_snapshots.front();
		auto pt2 = ball_snapshots.back();
		auto delta_y = (area.width - pt2.x) * (pt2.y - pt1.y) / (pt2.x - pt1.x);
		target_y = pt2.y + delta_y;
		auto diff = pt2.x - pt1.x;
		auto dx = (pt2.x - pt1.x) / ball_snapshots.size();
		auto rest_x = area.width - pt2.x;
		auto step_count = (rest_x / (2 * dx));
		step = (target_y - pos_y) / step_count;
	}
}

void Racket::estimate_target_ballistic(unsigned int delta_ms)
{
	if (ball_snapshots.size() > 2)
	{
		auto pt1 = ball_snapshots.front();
		auto pt2 = ball_snapshots[ball_snapshots.size() / 2];
		auto pt3 = ball_snapshots.back();

		auto x1 = pt1.x;
		auto y1 = pt1.y;
		auto x2 = pt2.x;
		auto y2 = pt2.y;
		auto x3 = pt3.x;
		auto y3 = pt3.y;

		//y = ax^2 + bx + c
		//a = ((y3-y1)(x2-x1) - (y2-y1)(x3-x1)) / ((x3^2 - x1^2)(x2-x1)-(x2^2-x1^2)(x3-x1))
		//b = (y2 - y1 - a(x2^2-x1^2)) / (x2 - x1)
		//c = y1 - (ax1^2 + bx1)

		auto a = ((y3 - y1) * (x2 - x1) - (y2 - y1) * (x3 - x1)) / ((pow(x3, 2) - pow(x1, 2)) * (x2 - x1) - (pow(x2, 2) - pow(x1, 2)) * (x3 - x1));
		auto b = (y2 - y1 - a * (pow(x2, 2) - pow(x1, 2))) / (x2 - x1);
		auto c = y1 - (a * pow(x1, 2) + b * x1);

		auto xval = area.width;
		target_y = a * pow(xval, 2) + b * xval + c;
		
		//auto delta_y = (area.width - pt2.x) * (pt2.y - pt1.y) / (pt2.x - pt1.x);
		//target_y = pt2.y + delta_y;
		//auto diff = pt2.x - pt1.x;
		auto dx = (pt3.x - pt1.x) / ball_snapshots.size();
		auto rest_x = area.width - pt3.x;
		auto step_count = (rest_x / (2 * dx));
		step = (target_y - pos_y) / step_count;
	}
}