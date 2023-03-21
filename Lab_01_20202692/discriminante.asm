section .data
    mensaje db "Ingresar los numeros:"
    mensajeLenght equ $-mensaje
    mensajeDiscriminante db "La solucion es: "
    mensajeDiscriminanteLenght equ $-mensajeDiscriminante
    a dq 0
    b dq 0
    c dq 0
    discriminante dq 0
    espacio dq " "
    saltoDeLinea dq 10
    

section .text   
    global _start

_start:
    ;Leer los numeros a,b y c
    mov rax, 1
    mov rdi, 1
    mov rsi, mensaje
    mov rdx, mensajeLenght
    syscall

    mov rax, 0
    mov rdi, 0
    mov rsi, a
    mov rdx, 4
    syscall
    
    ;Leer el espacio
    mov rax, 0
    mov rdi, 0
    mov rsi, espacio
    mov rdx, 1
    syscall

    mov rax, 0
    mov rdi, 0
    mov rsi, b
    mov rdx, 4
    syscall

    ;Leer el espacio
    mov rax, 0
    mov rdi, 0
    mov rsi, espacio
    mov rdx, 1
    syscall

    mov rax, 0
    mov rdi, 0
    mov rsi, c
    mov rdx, 4
    syscall



    ;Calcular el discriminante de derecha a izquiera
    mov rax, [a]
    mov rbx, [c]
    mul rbx
    ;Mover un registro con el valor de 4
    mov rcx, 4
    mul rcx
    ;Con todo lo de arriba hacemos 4ac, pero se debe almacenar en otro sitio para que no se cambie el valor de rax
    mov rcx, rax

    ;Para el b*b
    mov rax, [b]
    mov rbx, [b]
    mul rbx
    mov rbx, rax

    ;Restar el b*b - 4ac
    sub rbx, rcx
    ;Almacenar el valor del discriminante en la variable discriminante
    mov [discriminante], rbx
    
    ;Mostrar el discriminante 
    mov rax, 1
    mov rdi, 1
    mov rsi, mensajeDiscriminante
    mov rdx, mensajeDiscriminanteLenght
    syscall

    ;Imprimir el valor del discriminante, teniendo en cuenta el código ASCII
    mov rax, 1
    mov rdi, 1
    mov rsi, [discriminante]
    mov rdx, 4
    syscall



    ;Terminar el programa
    mov rax, 60
    mov rdi, 0
    syscall



