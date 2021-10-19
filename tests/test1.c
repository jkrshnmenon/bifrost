#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	if (argc > 1)
		printf("Welcome %s\n", argv[1]);
	else
		printf("Welcome");
	puts("Helloworld");
	return 0;
}
