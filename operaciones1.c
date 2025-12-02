#include <stdio.h>
#include <limits.h>


double calcular_nota_final(int* labs, int num_labs, int e1, int e2) {
    double suma_labs = 0;
    for(int i = 0; i < num_labs; i++) {
        suma_labs += labs[i];
    }
    double prom_labs = (num_labs > 0) ? (suma_labs / num_labs) : 0.0;
    return (6.0 * prom_labs + 3.0 * e1 + 3.0 * e2) / 10.0;
}

double calcular_media(int* data, int n) {
    if (n == 0) return 0.0;
    long suma = 0;
    for (int i = 0; i < n; i++) {
        suma += data[i];
    }
    return (double)suma / n;
}


int calcular_min(int* data, int n) {
    int min_val = INT_MAX;
    for (int i = 0; i < n; i++) {
        if (data[i] < min_val) min_val = data[i];
    }
    return min_val;
}

int calcular_max(int* data, int n) {
    int max_val = INT_MIN;
    for (int i = 0; i < n; i++) {
        if (data[i] > max_val) max_val = data[i];
    }
    return max_val;
}

int calcular_moda(int* data, int n) {
    int frecuencias[21] = {0};
    for (int i = 0; i < n; i++) {
        if (data[i] >= 0 && data[i] <= 20) frecuencias[data[i]]++;
    }
    int max_freq = -1, moda = -1;
    for (int j = 0; j <= 20; j++) {
        if (frecuencias[j] > max_freq) {
            max_freq = frecuencias[j];
            moda = j;
        }
    }
    return moda;
}