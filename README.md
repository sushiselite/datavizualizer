# datavizualizer
Open source webapp that currently allows users to interactively clean their dataset and generate visuals for their data. (Limited Functionality)

It currently supports very basic functionality and is a work in progress. Feel free to add suggestions through the 'Issues' tab.

It currently is not being hosted anywhere. To run it and test it yourself:

1. Download the latest tag from the ['releases'](https://github.com/sushiselite/datavizualizer/releases) section.
   
   Alternatively, clone the repository by running:
   
   ```https://github.com/sushiselite/datavizualizer.git```

3. Install necessary dependencies: (in a virtual environment - optional)
   
   ```pip install requirements.txt```

5. Use your terminal to start dev server at localhost:5000 using
   
   ```python app.py```

# To-Do List (Regularly updated)

Allow users to choose columns using interactive menu (need to figure out whether client side or server side implementation for future free hosting)
Add d3.js/matplotlib as an option to plot with alongside plotly
More interactive dataset features such as sampling by selecting rows/columns on website
Better UX
Dark mode toggle?

# Screenshots:

Landing Page:
![alt text](https://github.com/sushiselite/datavizualizer/blob/main/images/index.png?raw=true)

Data Cleaning:
![alt text](https://github.com/sushiselite/datavizualizer/blob/main/images/clean1.png?raw=true)
![alt text](https://github.com/sushiselite/datavizualizer/blob/main/images/clean2.png?raw=true)

Visualization and Summary:
![alt text](https://github.com/sushiselite/datavizualizer/blob/main/images/data1.png?raw=true)
![alt text](https://github.com/sushiselite/datavizualizer/blob/main/images/data2.png?raw=true)
