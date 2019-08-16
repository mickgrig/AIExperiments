// OpenCVTest.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <opencv2\opencv.hpp>
#include "Area.h"
#include "Ball.h"
#include "Racket.h"
#include "InitConditions.h"

using namespace cv;
using namespace std;

void draw(const Area & area, const Ball & ball, const Racket & racket, const Mat & image)
{
	//Mat image = Mat::zeros(area.height, area.width, CV_8UC3);

	ball.draw(image);
	racket.draw(image);
	area.draw(image);
	putText(image, String("\'Esc\' to exit"), Point(10, 30), FONT_HERSHEY_SIMPLEX, 0.7, Scalar(255, 255, 255));
	//imshow("Catching ball", image);
}

shared_ptr<Point2d> observe(const Mat & image, const Area & area)
{
	shared_ptr<Point2d> ball_center_ptr;
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	auto height = image.size.p[0];
	auto width = image.size.p[1];
	Mat grayimage = Mat::zeros(height, width, CV_8UC1);
	cvtColor(image, grayimage, COLOR_BGR2GRAY);

	auto subimage = grayimage.colRange(area.observe_x1 + 10, area.observe_x2 - 10);
	findContours(subimage, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

	if (!contours.empty())
	{
		auto contour = contours.front();
		vector<unsigned int> xvals, yvals;
		for (auto pt : contour)
		{
			xvals.push_back(pt.x);
			yvals.push_back(pt.y);
		}
		sort(xvals.begin(), xvals.end());
		sort(yvals.begin(), yvals.end());
		auto xmid = xvals[xvals.size()-1] + area.observe_x1 + 10;
		auto ymid = yvals[yvals.size() / 2];
		ball_center_ptr.reset(new Point2d(xmid, ymid));
	}
	return ball_center_ptr;
}

int _tmain(int argc, _TCHAR* argv[])
{
	//namedWindow("Win");
	Area area;
	Ball ball(area);
	Racket racket(area, ball);
	InitConditions initCond;
	while (true)
	{
		auto msec_delta = 25;
		auto retcode = waitKey(msec_delta);
		if (retcode == 27) //Escape to exit
			break;
		if (retcode == 98) //"b"
			ball.toggle_mode();
		if (retcode == 114) //"r"
			racket.toggle_mode();
		Mat image = Mat::zeros(area.height, area.width, CV_8UC3);
		draw(area, ball, racket, image);
		if (auto out_of_area = ball.move(initCond, area, msec_delta))
			initCond.randomize();

		auto ball_center_ptr = observe(image, area);

		if (ball_center_ptr)
			circle(image, *ball_center_ptr, 3, Scalar(128, 0, 128), -1);

		racket.observed(ball_center_ptr, msec_delta);
		racket.move(area);

		imshow("Catching ball", image);
	}
	return 0;
}

