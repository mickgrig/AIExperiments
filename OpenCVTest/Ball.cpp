#include "stdafx.h"
#include <opencv2\opencv.hpp>
#include "Area.h"
#include "Ball.h"
#include "InitConditions.h"

using namespace cv;

Ball::Ball(const Area & area) : radius(20), linear(false)
{
	start_init(area);
}
void Ball::start_init(const Area & area)
{
	center.x = 0;
	center.y = area.height / 2;
}
bool Ball::move(const InitConditions & init_cond, const Area & area, unsigned int msec_delta)
{
	if (linear)
		return linear_move(init_cond, area, msec_delta);
	else
		return ballistic_move(init_cond, area, msec_delta);
}

bool Ball::linear_move(const InitConditions & init_cond, const Area & area, unsigned int msec_delta)
{
	bool out = false;
	double distance = ((double)init_cond.pix_per_sec / 1000.) * msec_delta;
	auto init_x = center.x;
	auto init_y = center.y;
	double delta_x = distance * cos(init_cond.angle);
	double delta_y = distance * sin(init_cond.angle);
	center.x += delta_x;
	center.y += delta_y;
	if (out_of_area(area))
	{
		start_init(area);
		out = true;
	}
	return out;
}

bool Ball::ballistic_move(const InitConditions & init_cond, const Area & area, unsigned int msec_delta)
{
	bool out = false;

	auto angle = -init_cond.angle;
	auto vel = init_cond.pix_per_sec;
	auto x_vel = init_cond.pix_per_sec * cos(angle);
	auto y_vel = init_cond.pix_per_sec * sin(angle);
	double delta_x = (x_vel / 1000.) * msec_delta;
	center.x += delta_x;

	auto g = 150;
	////double delta_y = (1 + sin(angle) / cos(angle)) * delta_x + (pow(vel, 2) / g) * log(1 - (g*delta_x) / (pow(vel, 2)*cos(angle)) );
	//auto delta_y = center.x * tan(angle) - g*pow(center.x, 2) / (2 * pow(vel, 2) * pow(cos(angle), 2));
	////double delta_y = -g * pow(delta_x, 2) / (2 * pow(vel, 2));

	
	auto temp = (y_vel / x_vel) * 100 - (g / (2 * pow(vel, 2))) * pow(100, 2);
	auto delta_y = (y_vel / x_vel) * center.x - (g / (2 * pow(vel, 2))) * pow(center.x, 2);

	auto hmax = pow(vel, 2) * pow(sin(angle), 2) / (2 * g);
	auto L = (pow(vel, 2) * sin(2 * angle)) / g;
	//auto x_norm = center.x / area.width;
	//auto y_norm = 0.02 - pow(x_norm, 2);
	//auto delta_y = y_norm * area.height;

	center.y = area.height / 2 - delta_y;

	if (out_of_area(area))
	{
		start_init(area);
		out = true;
	}
	return out;
}

bool Ball::out_of_area(const Area & area) const
{
	return center.x > area.width || center.y > area.height || center.y < 0;
}

void Ball::draw(const Mat & image) const
{
	circle(image, center, radius, Scalar(0, 0, 255), -1);
	String ball_traj = ( linear ? "linear" : "ballistic" );
	putText(image, String("Ball mode: ") + ball_traj + String("(\'b\' to toggle)"), Point(10, 60), FONT_HERSHEY_SIMPLEX, 0.7, Scalar(255, 255, 255));
}