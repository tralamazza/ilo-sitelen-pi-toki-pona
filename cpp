scp -r *.* pi@ilo-sitelen.local:~/docs/TPTERMINAL/
DATE=$(date +%y-%m-%d)
echo $DATE
mkdir lipu/$DATE
scp -r pi@ilo-sitelen.local:~/docs/TPTERMINAL/lipu/*.txt lipu/$DATE/
