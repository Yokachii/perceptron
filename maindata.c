#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int epoques;
    float accBefore;
    float accAfter;
    int FN;
    int FP;
    int TN;
    int TP;
    float accMax;
    int epoquesMax;
} Data;

typedef struct {
    float *ranges;
    float step;
} Param;

/*

Param

{
    label:"epoque"
    ranges:{10;1000}
    step:10
}

*/

Data *getResults(int epoques, float taux, float ratio, int normalized, int stopWhenTrained){
    FILE *fp;
    char path[1035];
    char commande[256];

    Data *res = malloc(sizeof(Data));
    res->epoques = 0;
    res->accBefore = 0;
    res->accAfter = 0;
    res->FN = 0;
    res->FP = 0;
    res->TN = 0;
    res->TP = 0;

    snprintf(commande, sizeof(commande), "./perceptron ./data/champignons.csv %d %f %f %d %d 0",epoques,taux,ratio,normalized,stopWhenTrained);

    // Ouvre le programme en mode lecture
    fp = popen(commande, "r");
    if (fp == NULL) {
        printf("Erreur lors de l'exécution de la commande.\n");
        return res;
    }

    if (fgets(path, sizeof(path), fp) != NULL) {
        int itemsParsed = sscanf(path, "%d;%f;%f;%d;%d;%d;%d;%d;%f", &res->epoques, &res->accBefore, &res->accAfter, &res->FN, &res->FP, &res->TN, &res->TP, &res->epoquesMax, &res->accMax);

        if (itemsParsed != 9) {
            printf("Attention : tous les champs n'ont pas pu être parsés correctement (reçu : %s)\n", path);
        }
    }

    pclose(fp);

    return res;
}

int main() {

    FILE *csvFile = fopen("resultats_grid_search.csv", "w");
    if (csvFile == NULL) {
        perror("Erreur d'ouverture du fichier CSV");
        return 1;
    }

    fprintf(csvFile, "normalized,ratio,taux,epoques_demandes,epoques_reels,accBefore,accAfter,FN,FP,TN,TP,epoques_max,accMax\n");
    
    float r1[] = {1,500};
    Param *epoques = malloc(sizeof(Param));
    epoques->ranges=r1;
    epoques->step=1;

    float r2[] = {0,0.1};
    Param *taux = malloc(sizeof(Param));
    taux->ranges=r2;
    taux->step=0.01;

    float r3[] = {0.5,1};
    Param *ratio = malloc(sizeof(Param));
    ratio->ranges=r3;
    ratio->step=0.1;

    float r4[] = {0,1};
    Param *normalized = malloc(sizeof(Param));
    normalized->ranges=r4;
    normalized->step=1;

    for(float i = normalized->ranges[0]; i <= normalized->ranges[1]; i += normalized->step) {
        for(float j = ratio->ranges[0]; j <= ratio->ranges[1]; j += ratio->step) {
            for(float k = taux->ranges[0]; k <= taux->ranges[1]; k += taux->step) {
                // for(float l = epoques->ranges[0]; l <= epoques->ranges[1]; l += epoques->step) {

                    int current_epoques = (int)epoques->ranges[1];
                    float current_taux = k;
                    float current_ratio = j;
                    int current_norm = (int)i;

                    Data *res = getResults(current_epoques, current_taux, current_ratio, current_norm, 1);
                    if (res == NULL) continue;

                    // Vérifier si le perceptron s'est arrêté avant la fin
                    int isfullyrun = (current_epoques > res->epoques) ? 0 : 1; 

                    // Affichage console
                    printf("Norm: %d | Ratio: %.1f | Taux: %.2f | Ep: %d/%d | Acc After: %.2f | EpoquesMax : %d | AccMax : %.2f\n", 
                           current_norm, current_ratio, current_taux, res->epoques, current_epoques, res->accAfter, res->epoquesMax, res->accMax);

                    // Stockage dans le fichier CSV
                    fprintf(csvFile, "%d,%.2f,%.2f,%d,%d,%.4f,%.4f,%d,%d,%d,%d,%d,%.4f\n",
                            current_norm, current_ratio, current_taux, current_epoques, 
                            res->epoques, res->accBefore, res->accAfter, 
                            res->FN, res->FP, res->TN, res->TP, res->epoquesMax, res->accMax);

                    free(res);
                // }
            }
        }
    }

    fclose(csvFile);

    free(epoques);
    free(taux);
    free(ratio);
    free(normalized);
    
    return 0;
}