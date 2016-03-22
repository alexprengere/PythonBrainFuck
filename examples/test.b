loop counter
+++++++++
+++++++

>

value to copy
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
<
[ main loop
    >
    [ >+<- ] copy value one cell to the right
    >. print it

    [ <+>- ] copy value back to the left
    <<
    - decrement the loop counter
] repeat
++++++++++. print a newline
