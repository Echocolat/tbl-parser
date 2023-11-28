### .tbl (Super Mario RPG Remake) <-> json converter

##### Credits

Agix for their Python2 [NetBinaryFormatterParser](https://github.com/agix/NetBinaryFormatterParser) which played a gigantic role in this project.

##### How to use .tbl -> .json

Open a terminal in the root folder (`tbl parser`), and write `.\parse.py -i [INPUTFILE]` where `[INPUTFILE]` is the location of the .tbl file you want to convert. Alternatively, drag said .tbl file in `parse.exe` in the `executable` folder.

##### How to use .json -> .tbl

Open a terminal in the root folder (`tbl parser`), and write `.\reserialize.py -i [INPUTFILE]` where `[INPUTFILE]` is the location of the .json file you want to convert. Alternatively, drag said .json file in `reserialize.exe` in the `executable` folder.