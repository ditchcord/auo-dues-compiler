# auo-dues-compiler

### Takes in dues spreadsheet and cashnet record and complies dues record

## What is this
- Some people don't send receipt number when they pay on cashnet
- But SLICE cashnet record at least records the names of people who paid
- This program shows you every person who has a cashnet record but no recorded receipt number.

## Additional features
- Immediately see who hasn't paid dues yet
- See if someone paid their dues multiple times
- If transactions from spring semester exist, automatically ignore cashnet data from fall semester

## Obtaining "Dues Tracker"
1. Copy the 3 columns of the Dues Tracker google sheet and paste it into a .txt (DO NOT format as CSV)
2. Call this duestracker-f23.txt or whatever the semester is

## Obtaining "Cashnet Record"
1. Email Student Involvement and Traditions Finance requesting a cashnet record for AUO in PDF format (NOT excel/csv format)
2. Open PDF in chrome or firefox browser and highlight all using command/control+A (DO NOT copy from mac preview pdf viewer)
3. Copy and paste into a .txt - make sure you can see one transaction per line each starting with the date
4. Call this cashnet-f23.txt or whatever the semester is

## Quick start
1. Install Python 3.10 or newer
2. Clone this repository to your device
3. Move/copy your duestracker-xxx.txt and cashnet-xxx.txt to the **private** folder (so that git pushes won't expose ppl's data)
4. Open main.py
5. Type the file name of your dues tracker and cashnet record when prompted
6. See merged data in the console output

## Troubleshooting
After parsing Cashnet Record - if extra words are appended to people's names, 
or dues appearing in non dues payments, add those words to Tokens.tokens in main.py.

Email wellsjason543 at gmail dot com for issues or questions

## External content
- cmu_csps_utils (for 2d list print) by CMU CS Prep School

#

--Copyright notice does not apply to 'cmu_cpcs_utils.py'--

Copyright (c) 2025 Jason H. Wells

MOST RIGHTS RESERVED - DISTRIBUTION PROHIBITED

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to use, modify, or merge the Software on 
their personal computer. The following rights are reserved: To 
publish, distribute, sublicense, and/or sell copies of the 
Software or modified versions of the Software, including 
anything merged with the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.