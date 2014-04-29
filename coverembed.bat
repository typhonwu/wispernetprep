:: from book.azw3 extract cover file thumbnail_book_EBOK_portrait.jpg and create book.processed.azw3
call wispernetprep.cmd -t auto -s auto -i %1 -p bottom

:: generate book.epub
python.exe "%~dp0\lib\kindleunpack.py" -s "%~n1.azw3" "%~n1"

:: rename book.epub to avoid removal of original epub (if exists)
if exist "%~n1.epub" copy "%~n1.epub" "%~n1_original.epub" 

:: copy mobi8\book.epub file into current directory
copy /y ".\%~n1\mobi8\%~n1.epub" ".\"


:: remove directory with unpacked files
rmdir "%~n1" /s /q

::replace cover in epub
ebook-polish "%~n1.epub" --cover "thumbnail_%~n1_EBOK_portrait.jpg"
::ebook-meta "%~n1.epub" --cover "thumbnail_%~n1_EBOK_portrait.jpg"

:: convert epub to mobi
kindlegen "%~n1_polished.epub" -locale en -o "%~n1.mobi"

::swap cover and thumb offsets, add EBOK to 501, and create book_cover_inside_azw3
python "%~dp0swap_cover.py" "%~n1.mobi" "%~n1_embedded_cover.azw3" 

::clean up intermediate files

del "%~n1.epub"
del "%~n1_polished.epub"
del "%~n1.mobi"



