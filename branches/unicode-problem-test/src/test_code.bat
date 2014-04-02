:: just call with book.epub
ebook-convert %1 "%~n1.azw3" 
::chcp 866
call wispernetprep.cmd -t auto -s 22 "%~n1.azw3" 
