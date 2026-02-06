DATA SEGMENT
    CHAR DB 26 DUP(0)
DATA ENDS

CODE SEGMENT
    ASSUME CS:CODE, DS:DATA
START:
    MOV AX,DATA      ; 初始化数据段
    MOV DS,AX
    MOV CX,26        ; 计数器 CX 初始化为 26
    MOV AL,'A'       ; 初始化 AL 为 'A'
    MOV SI,OFFSET CHAR ; SI 指向 CHAR 的偏移地址
CIRCLE:
    MOV [SI],AL      ; 将 AL 的值存入 [SI] 指向的内存
    INC SI           ; SI 加 1
    INC AL           ; AL 加 1
    LOOP CIRCLE      ; 循环直到 CX 减为 0
    
    MOV AH, 4CH      ; 装入功能号 4CH（程序结束）
    INT 21H          ; 调用 DOS 功能
    
CODE ENDS
END START