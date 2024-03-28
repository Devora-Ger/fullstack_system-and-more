#include <iostream>
#include <string>

bool validHeightInput(float h) {
	return (h >= 2);
}

bool validWidthInput(float w) {
	return (w > 0);
}

void takeDimensionsTower(float& h, float& w) {
	std::cout << "Enter the height of the tower" << std::endl;
	std::cin >> h;
	while (false == validHeightInput(h)) {
		std::cout << "Enter height greater then 2 or equale" << std::endl;
		std::cin >> h;
	}

	std::cout << "Enter the width of the tower" << std::endl;
	std::cin >> w;
	while (false == validHeightInput(w)) {
		std::cout << "Enter width greater then 0" << std::endl;
		std::cin >> w;
	}
}

float calcEreaRectangle(float h, float w) {
	return h * w;
}

float calcPerimeterRectangle(float h, float w) {
	return 2*h + 2*w;
}

float calcSideOfIsoscelesTriangle(float h, float w) {
	float d = w * 1.0 / 2;
	return sqrt(h * h + d * d);
}

float calcPerimeterTriangle(float h, float w) {
	return calcSideOfIsoscelesTriangle(h, w) * 2 + w;
}

//the function work with ints, it take the lower value of a number! write in the readme
//Write in the readme that the case w==2*h included by the conditen  w%2 == 0
void printTriangle(int h, int w) {
	if (0 == w % 2 || w > 2 * h) {
		std::cout << "The triangle cannot be printed" << std::endl;
		return;
	}
	
	int numOfLines = h - 2;
	int starsPerLine = (w - 2) / 2;
	std::string stars = "***";
	std::string spaces;
	for (int i = 0; i < w / 2; i++) {
		spaces.append(" ");
	}

	//Print the first line
	std::cout << spaces;
	std::cout << "*" << std::endl;

	spaces.erase(0,1);
	//Adding lines to the top of the pyramid (if needed)
	for (int j = 0; j < numOfLines % starsPerLine; j++) {
		std::cout << spaces << stars << std::endl;
	}

	for (int i = 0; i < starsPerLine; i++) {
		
		for (int j = 0; j < numOfLines / starsPerLine;j++) {
			std::cout <<spaces << stars << std::endl;
		}
		spaces.erase(0,1);
		stars.append("**");
	}
	
	//Print the last line
	std::cout << stars << std::endl;
}

void createRectangleTower() {
	float height;
	float width;
	takeDimensionsTower(height, width);
	if (height == width || 5 == abs(height - width)) {
		std::cout << "Erea rectangle: " << calcEreaRectangle(height, width) << std::endl;
	}
	else {
		std::cout << "Perimeter rectangle: " << calcPerimeterRectangle(height,width) << std::endl;
	}
}

void createTriangleTower() {
	float height;
	float width;
	int choice;
	takeDimensionsTower(height, width);
	std::cout << "Enter your choice:" << std::endl
		<< "1: calculate the perimeter of the triangle" << std::endl
		<< "2: print the triangle" << std::endl;
	std::cin >> choice;
	switch (choice) {
	case 1:
		std::cout << "The primeter of the triangle is: " << calcPerimeterTriangle(height, width) << std::endl;
		break;
	case 2:
		printTriangle(height, width);
		break;
	default:
		std::cout << "Wrong choice" << std::endl;
		//Write in the readme that if we put wrong choich the function stop
	}
}

enum Tower{Rectangle = 1, Triangle};
int main() {

	int choice;
	do {
		std::cout << "Enter your choice" << std::endl
			<< "1: For rectangle tower" << std::endl
			<< "2: For triangle tower" << std::endl
			<< "3: Exit the program" << std::endl;
		std::cin >> choice;
		switch(choice){
		case Rectangle:
			createRectangleTower();
			break;
		case Triangle:
			createTriangleTower();
			break;
		default:
			if (3 != choice) {
				std::cout << "Enter a number between 1-3" << std::endl;
			}
		}

	} while (3 != choice);

	return 0;
}