extern int productoASM(float *arreglo,int cantidad,int tope);
int producto1(float *arreglo, int cantidad,float tope){
    int mayorQue=0,menorQue=0;
    for(int i=0;i<cantidad;i++){
        if(arreglo[i]<tope){
            menorQue++;
        }else if(arreglo[i]>tope){
            mayorQue++;
        }
    }
    return mayorQue*menorQue;
}