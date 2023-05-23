# .cmp to .pose file converter
A simple Python script that converts CMTool .cmp pose files to .pose, which is the current format used in FFXIV modding tools like Ktisis  and Anamnesis.

Requires Python, any version should work.

---
### Usage
Run it as a normal Python script, passing the .cmp file as an argument. It will save the converted file in the same directory as the original, with the same name but with the .pose extension.
```
python cmp2pose.py <input_file.cmp>
```
Or, if you want to convert all .cmp files in a directory recursively, pass the directory as an argument. It will save the resulting .pose files in the same locations as the original .cmp files.
```
python cmp2pose.py <input_directory>
```
---
### Note
*I shamelessly took the conversion algorithm from the website below and just changed it from JS to Python. So credits for it go to the author of that site
(I couldn't find their name so I can credit them properly, but thank you, whoever you are).
Honestly, if you want a better experience just use their website, it's much more user friendly and has a GUI. I'm just here learning Python.*


### [https://xivposeconverter.netlify.app/](https://xivposeconverter.netlify.app/)
