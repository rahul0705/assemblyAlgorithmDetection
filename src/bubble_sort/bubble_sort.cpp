#include <iostream>

using namespace std;

int find(int * ARRAY, const int SIZE, int num);
void bubbleSort(int * ARRAY, const int SIZE);

int main(int argc, char* argv[])
{
	const int SIZE = 100;
	int * ARRAY = new int[SIZE];

	for(int i = 0; i < SIZE; i++){
		ARRAY[SIZE-i-1] = i;
	}

	/*for(int i = 0; i < SIZE; i++){
		cout << ARRAY[i] << endl;
	}

	cout << endl;*/

	//int a = find(ARRAY, SIZE, 64);

	bubbleSort(ARRAY, SIZE);
	
	/*for(int i = 0; i < SIZE; i++){
		cout << ARRAY[i] << endl;
	}*/

	//system("pause");

	return 0;
}

int find(int * ARRAY, const int SIZE, int num){
	for(int i = 0; i < SIZE; i++){
		if(ARRAY[i] == num){
			return i;
		}
	}

	return -1;
}

void bubbleSort(int * ARRAY, const int SIZE){
	for(int i = 0; i < SIZE - 1; i++){
		for(int j = 1; j < SIZE; j++){
			if(ARRAY[j-1] > ARRAY[j]){
				int temp = ARRAY[j-1];
				ARRAY[j-1] = ARRAY[j];
				ARRAY[j] = temp;
			}
		}
	}
}