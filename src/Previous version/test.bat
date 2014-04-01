:: Old code
::wispernetprep.cmd "%~n1.azw3" autotitle 
:: New code
wispernetprep_sa.cmd -t auto -s auto "%~n1.azw3" 
pause
move "%~n1.processed.azw3" "%~n1.azw3"
