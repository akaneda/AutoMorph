#!/usr/bin/python
"""
writeLatexFile.py
"""

def writeLatexFile(u3dFile,media9Path,outputFileNameBase,outputFilePath,focusedPath,sfPath):
    """
    """
    import os
    
    volFilePath = os.path.join(sfPath,outputFileNameBase,outputFileNameBase+'_volumes.csv')
    volFile = open(volFilePath,'r')
    volLines = volFile.readlines()[0].split('\r')
    values = volLines[1].split(',')
    width = values[-1]
    length = values[-2]
    gridSize = values[-3]
    # Build label image path
    labelPath = os.path.join(focusedPath,'final','z.stacks',outputFileNameBase,'label')
    # Remove periods from image name if present
    if '.' in outputFileNameBase:
    	newFileNameBase = outputFileNameBase.replace('.','_')
    	rgbPathIn = os.path.join(sfPath,outputFileNameBase,outputFileNameBase + '_focused_rgb')
    	rgbPathOut = os.path.join(sfPath,outputFileNameBase,newFileNameBase + '_focused_rgb')
    else:
        rgbPath = os.path.join(sfPath,outputFileNameBase,outputFileNameBase + '_focused_rgb')
    # Convert image types from .tif to '.png' using an external call to ImageMagick
    imLabelCommand = 'convert ' + labelPath + '.tif ' + labelPath + '.png'
    os.system(imLabelCommand)
    imRGBCommand = 'convert ' + rgbPathIn + '.tif ' + rgbPathOut + '.png'
    os.system(imRGBCommand)
    
    latexFile = open(outputFilePath,'w')
    
    latexText1 = """\documentclass{article}
\usepackage{"""

    latexText2 = """}
\usepackage[colorlinks=true]{hyperref}
\usepackage{siunitx}

\setlength{\\voffset}{-0.75in}
\setlength{\headsep}{5pt}
\setlength{\intextsep}{5pt}
\setlength{\\textfloatsep}{-1pt}
\setlength{\\textheight}{650pt}

\\begin{document}
\pagestyle{empty}

\\begin{figure}[t]
	\centerline{\includegraphics[scale=0.5]{"""

    latexText3 = """}}
\end{figure}

\\begin{center}
	\framebox{Length: \SI{""" 
	
    latexText4 = """}{\micro\metre} - Width: \SI{"""

    latexText5 = """}{\micro\metre} - Grid Size: \SI{"""

    latexText6 = """}{\micro\metre}}
\end{center}

\centerline{\includemedia[
label="""

    latexText7 = """,
width=1\linewidth,height=1\linewidth,
playbutton=none,
activate=pageopen,
3Dlights=CAD,
3Daac=7,
3Droll=0,
3Dc2c=-4 -2 5,
3Droo=85,
3Dcoo=6 4 0
]{}{"""
    latexText8 = """}}

\\begin{figure}[b]
	\centerline{\includegraphics[scale=0.2]{"""
 
    latexText9 = """}}
\end{figure}

\end{document}"""

    latexTextFinal = ''.join([latexText1,os.path.join(media9Path,'media9'),latexText2,labelPath,latexText3,length,latexText4,width,latexText5,gridSize,latexText6,u3dFile,latexText7,u3dFile,latexText8,rgbPathOut,latexText9])
    latexFile.write(latexTextFinal)
    latexFile.close()