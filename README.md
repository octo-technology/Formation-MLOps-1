What is this?
-------------
At this step : 
- Your notebook is clean and running
- You have a few documented functions

What is the goal ?
-------------------
The goal at this step is to extract your functions in a `.py` file.

You will then be able to reuse those functions in other notebooks. 

To do that : 
- Create a `src` folder
- Create a `feature_engineering.py` file in this folder
- Cut from notebook and paste in `.py` file the code of your functions
- Make sure you have all needed `import`
- To use functions in notebook add :
```python
import sys
sys.path.append("../src/")
from feature_engineering import *
```

When I'm done ?
---------------
When you are done, please wait for the rest of the group.

For the next step of the practical work, you can either 
keep on working on the code as it is, or checkout branch `3_extract_code_into_source`

To checkout branch `3_extract_code_into_source` you need to either commit 
or stash your changes : 
```
git stash
git checkout 3_extract_code_into_source
```