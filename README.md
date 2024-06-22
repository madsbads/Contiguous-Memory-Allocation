## Contiguous-Memory-Allocation

###### Execution guide 
- Start program wiht initial memory of 1MB
`python3 main.py 1048576`
- Status report
`allocator> STAT`
- Request 100 KB for P1 using first-fit
`allocator> RQ P1 100000 F`
- Request 200 KB for P2 using best-fit
`allocator> RQ P2 200000 B`
- Request 300 KB for P3 using worst-fit
- Release block of memory (P2)
`allocator > RL P2`
- Request 150 KB for P4 using worst-fit
`allocator> RQ P4 150000 W`
- Compact the memory to combine free spaces
`allocator> C`
- End program 
`allocator> X`