#pragma once

struct InitConditions;
struct Ball
{
	Ball(const Area &);
	void start_init(const Area &);
	bool move(const InitConditions &, const Area & area, unsigned int msec_delta);

	void draw(const cv::Mat & image) const;
	const unsigned int radius;
	cv::Point2d center;

private:
	bool out_of_area(const Area &) const;
	bool linear_move(const InitConditions &, const Area & area, unsigned int msec_delta);
	bool ballistic_move(const InitConditions &, const Area & area, unsigned int msec_delta);
};