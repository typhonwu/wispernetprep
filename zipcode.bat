ebook-convert %1 "%~n1_embed.epub" 

sigil "%~n1_embed.epub"

set /p class=Enter calibre class name:

if [%2]==[] (goto mdef) else goto mspec
:mspec 
python.exe "%~dp0embednm.py" -e "%~n1_embed.epub" -m %2 -c %class%
goto pass
:mdef
python.exe "%~dp0embednm.py" -e "%~n1_embed.epub" -c %class%
:pass

:: convert to mobi
kindlegen "%~n1_embed.epub" -locale en -o "%~n1.mobi"
:: extract azw3
python.exe "%~dp0\lib\kindleunpack.py" -s "%~n1.mobi" "%~n1"
:: copy mobi8-*.azw3 file into current directory
copy ".\%~n1\*.azw?" ".\"
:: check if old  file *.azw3 exists and delete it
if exist "%~n1.azw3" del "%~n1.azw3"
:: rename mobi8-*.azw3 file
call renazw3 "mobi8-%~n1.azw3" 
:: remove intermediate file
del "%~n1_embed.epub"
del "%~n1.mobi"
:: remove directory with unpacked files
rmdir "%~n1" /s /q

call wispernetprep.cmd -s auto -t auto -p bottom -i "%~n1.azw3"
move /y "%~n1.processed.azw3" "%~n1.azw3"
