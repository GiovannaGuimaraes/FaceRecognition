
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){

	int i;
	for(i = 1; i < argc; i++){
		printf("processing %s...\n", argv[i]);

		FILE *fp = fopen(argv[i], "rw+");
		int j;
		char var[255];
		for(i = 0; i < count; i++){
			fscanf("[^\n]%s", &var);
			fseek(fp, SEEK_CUR, 12);
		}
		fclose(fp);
	}


	return 0;
}