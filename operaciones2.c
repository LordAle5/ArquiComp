#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BUFFER_SIZE 2048

int procesar_archivo_io() {
    FILE *fp = fopen("notas_alumnos.csv", "r");
    if (!fp) return 0;
    char buffer[BUFFER_SIZE];
    if (!fgets(buffer, BUFFER_SIZE, fp)) { fclose(fp); return 0; } 
    int contador = 0;
    while (fgets(buffer, BUFFER_SIZE, fp)) {
        contador++;
       
        volatile int x = 0;
        for(int i=0; buffer[i] != '\0'; i++) x += buffer[i];
    }
    fclose(fp);
    return contador;
}