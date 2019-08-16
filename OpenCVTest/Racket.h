#pragma once

struct Area;
struct Ball;
struct Racket
{
public:
	Racket(const Area &, const Ball &);
	void draw(const cv::Mat &) const;
	void move(const Area &);
	void observed(std::shared_ptr<cv::Point2d> ball_center_ptr, unsigned int delta_ms);
	std::vector<cv::Point2d> ball_snapshots;
	void toggle_mode() { linear = !linear; }
	
private:
	const Area & area;
	double target_y, pos_y;
	double len;
	double step;
	bool linear; //true - линейна€ интерпол€ци€, false - баллистическа€ интерпол€ци€
	double top() const;
	double bottom() const;
	void estimate_target(unsigned int delta_ms);
	void estimate_target_linear(unsigned int delta_ms);
	void estimate_target_ballistic(unsigned int delta_ms);
};