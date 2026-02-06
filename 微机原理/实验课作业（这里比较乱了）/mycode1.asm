DATA SEGMENT     
     START_DATA DB 17H,42H,21H,
                DB 36H,43H,65H,21H,02H,
                DB 07H,65H,65H,23H,54H,87H,25H,
                DB 43H,43H,65H,04H,65H     
     TARGET_DATA DB 20 DUP(0)
DATA ENDS

CODE SEGMENT 
     ASSUME CS:CODE, DS:DATA

START:
     MOV AX,DATA        ; 将数据段地址加载到AX
     MOV DS,AX          ; 将AX的值移动到DS
     
     MOV CX,20          ; 设置CX为20，用于计数
     MOV SI,OFFSET START_DATA ; 源地址偏移量
     MOV DI,1000H       ; 目标地址偏移量
     
LOOP_1:
     MOV AL,[SI]        ; 将SI指向的内存单元内容移动到AL
     MOV [DI],AL        ; 将AL的内容移动到DI指向的内存单元
     INC SI             ; SI加1
     INC DI             ; DI加1
     LOOP LOOP_1        ; 循环，直到CX减为0

     MOV CX,20          ; 重置CX为20
     MOV SI,1000H       ; 源地址偏移量1000H
     MOV DI,3000H       ; 目标地址偏移量3000H
     
CHECK:
     MOV AL,[SI]        ; 将SI指向的内存单元内容移动到AL
     CMP AL,50         ; 比较AL和50
     JBE NEXT           ; 如果AL <= 50，则跳转到NEXT
     MOV [DI],AL        ; 如果AL > 50，将AL的内容移动到DI指向的内存单元
     INC DI             ; DI加1

NEXT:
     INC SI             ; SI加1
     LOOP CHECK         ; 循环，直到CX减为0

     MOV AH,4CH         ; DOS中断，程序结束
     INT 21H  

CODE ENDS
END START
