@echo off                                                                                                                                                                                                                                                                                                                     
echo filepath is %1 
echo player is %2
cd C:\Users\leit\Desktop\WebpageReview\Akochan
akochan-reviewer.exe -i %1 -a %2 --pt 80,40,0,-80 --no-open
