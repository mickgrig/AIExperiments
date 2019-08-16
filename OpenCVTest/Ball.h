#pragma once

struct InitConditions;
struct Ball
{
public:
	Ball(const Area &);
	void start_init(const Area &);
	bool move(const InitConditions &, const Area & area, unsigned int msec_delta);

	void draw(const cv::Mat & image) const;
	const unsigned int radius;
	cv::Point2d center;
	bool is_linear() const { return linear; }
	void toggle_mode() { linear = !linear; }

private:
	bool linear; //true - линейная траектория, false - баллистическая
	bool out_of_area(const Area &) const;
	bool linear_move(const InitConditions &, const Area & area, unsigned int msec_delta);
	bool ballistic_move(const InitConditions &, const Area & area, unsigned int msec_delta);
};