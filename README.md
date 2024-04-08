# This project, conducted by third-year students at UCL, compares haptic feedback and spatial audio in collaborative mixed reality


This repository consists of the work done my **COMP0031 Group 9** consisting of **Gauri Desai, Aryan Agarwal, Chidinma Ezeji, Taha Chowdhury, Molly Zhu, Chaitu Nookala, Nandini Chavda and Zihan Zhu**.

Please refer to the *group report* also submitted with this repository on details of the project's research process. This README serves as an indicator of where everything is and how the work is structured.

## General Structure

This is structured as a **Unity project** which can be opened with version **v2022.3.17f1**, if you wish to examine the project in the editor, please install this version and the entire repository, Unity will automatically populate the project with user-side files.

There are numerous packages that are required to be installed into a local instance of the project in order to run it. These include

- XR interaction toolkit
- Ubiq - refer to UCL Ubiq for more details
- Android Build Support

## Where everything is

### Supplementary materials

In the **root** of the repository there is a file named **project_supplementary_material.pdf**, which much of the supplementary documents used throughout the project, such as **risk assessment, participation information sheets, pre-experiment surveys, etc**. Please refer to each individual documented as referenced in the report

### Unity Assets

Most of the Unity project files and assets are in the **Assets** folder, however here are where some specific important files are.

**Scenes -** in *Assets/Scenes*, mainly used scenes *spatial maze.unity* and *haptics maze.unity*
**ROVR scripts -** Scripts to use the ROVR *wizzdish* are in *Assets/ROVR*
**Living birds assets/scripts -** In *Assets/living birds*
**Ubiq package -** In *Assets/samples/Ubiq* 
**All other important Scripts -** In *Assets/scripts*

Other supplementary assets can be found in other directories in the *Assets* folder.

### Log Files and scripts

All data logging was done internally and stored in **'Assets/Logs/TraverseData'**, refer to the report to the report to understand the format of each log file. Also in **Assets/Logs** Contains all statistical analysis scripts as *python* files. All these scripts were used in our statistical analysis and data plotting for analysing results and discussing conclusions made from the logs.




