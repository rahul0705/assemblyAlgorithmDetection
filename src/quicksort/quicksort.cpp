#include <stdio.h>
#include <stdlib.h>
#include <cstdlib>
#include <unistd.h>
#include <stdio.h>
#include <iostream>

using namespace std;

void quickSort(int *arr, int elements);

int main()
{
	int x[] = {31,28,31,98,78,34,9264,27506,3624,2,6,8,4,3859};
	quickSort(x,14);
}

void quickSort(int *arr, int elements) {

  #define  MAX_LEVELS  300

  int  piv, beg[MAX_LEVELS], end[MAX_LEVELS], i=0, L, R, swap ;

  beg[0]=0; end[0]=elements;
  while (i>=0) {
    L=beg[i]; R=end[i]-1;
    if (L<R) {
      piv=arr[L];
      while (L<R) {
        while (arr[R]>=piv && L<R) R--; if (L<R) arr[L++]=arr[R];
        while (arr[L]<=piv && L<R) L++; if (L<R) arr[R--]=arr[L]; }
      arr[L]=piv; beg[i+1]=L+1; end[i+1]=end[i]; end[i++]=L;
      if (end[i]-beg[i]>end[i-1]-beg[i-1]) {
        swap=beg[i]; beg[i]=beg[i-1]; beg[i-1]=swap;
        swap=end[i]; end[i]=end[i-1]; end[i-1]=swap; }}
    else {
      i--; }}}
