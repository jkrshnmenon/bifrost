#include <stdio.h>
#include <stdlib.h>

int foo(int x) {
	if ( x % 2 == 0) 
		puts("Even");
	else
		puts("Odd");
	return 0;
}

int main(int argc, char **argv) {
	if (argc > 1)
		printf("Welcome %s\n", argv[1]);
	else
		printf("Welcome");
	foo(argc);
	return 0;
}
