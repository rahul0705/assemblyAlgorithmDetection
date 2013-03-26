#include <iostream>

using namespace std;

void insertionSort(int * ARRAY, const int SIZE);

int main(int argc, char* argv[])
{
	const int SIZE = 100;
	int * ARRAY = new int[SIZE];

	for(int i = 0; i < SIZE; i++){
		ARRAY[SIZE-i-1] = i;
	}

	for(int i = 0; i < SIZE; i++){
		printf("%d ", ARRAY[i]);
	}

	insertionSort(ARRAY, SIZE);

	for(int i = 0; i < SIZE; i++){
		printf("%d ", ARRAY[i]);
	}

	system("pause");

	return 0;
}

void insertionSort(int * ARRAY, const int SIZE){
	int value = 0;
	int currLoc = 0;


	for(int i = 1; i < SIZE; i++){
		value = ARRAY[i];
		currLoc = i;

		while(currLoc > 0 && value < ARRAY[currLoc - 1]){
			ARRAY[currLoc] = ARRAY[currLoc - 1];
			currLoc--;
		}

		ARRAY[currLoc] = value;
	}

}