# QR-Code-Angle-Calculator

This project was created during my internship. I was in the AI team and we are responsible for the motion of logistics robot. The robot moves by scanning QR codes on the ground and finds its path. To create the dataset for neural networks, this util program calculates the angle of any Qr Code from images.
---
There two util program for this purpose.
# 1.Auto Angle Calculator
Finds QR code and detects edges of it. By using cordinate of edges of Qr code, calculates angle.
![Angle Calculator2](https://user-images.githubusercontent.com/54181614/63369035-d0a53500-c387-11e9-8f51-6635657f3f84.PNG)
# 2. Angle Labelling Program
Auto Angle Calculator calculates angle with +1,-1 degree error. Angle Labelling Program is for more sensitive calculation and created by using Tkinter Library of Python for GUI. User labels the bottom of qr code, program calculates and saves as txt file.
![Angle Calculator](https://user-images.githubusercontent.com/54181614/63369495-c899c500-c388-11e9-8489-0e7c2648aac4.PNG)
