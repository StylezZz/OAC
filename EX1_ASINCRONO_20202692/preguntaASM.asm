    global productoASM
    section .text
productoASM:
;rdi = arreglo
;rsi = tamaño
;xmm0 = tope

;Variables
mov r8, 0 ; menorQue =0
mov r9, 0 ; mayorQue =0
mov rdx,0 ; contador =0 

for:
    cmp rdx, rsi ; contador<tamaño
    jge finFor
    movss xmm1, [rdi] 
    ucomiss xmm0, xmm1 ; tope<arreglo[contador]
    jae menorQue
    ucomiss xmm1,xmm0 ; arreglo[contador]<tope
    jae mayorQue
siguiente:
    add rdi, 4
    inc rdx; contador++
    jmp for

mayorQue:
    inc r9 ; mayorQue++
    jmp siguiente 


menorQue:
    inc r8 ; menorQue++
    jmp siguiente



finFor:
    mov rax, r8
    mov rbx, r9
    mul rbx
    ret

