ebook-convert %1 "%~n1.azw3"
::chcp 65001
::call wispernetprep.cmd -t "Война денадцатого года" -s 23  "%~n1.azw3"
call wispernetprep.cmd -t auto -s 23  "%~n1.azw3"