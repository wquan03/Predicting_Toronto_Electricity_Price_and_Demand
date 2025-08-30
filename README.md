# Prediction Model for Toronto Electricity Price and Demand
## Introduction:
This is a repository that intends to develop a machine learning model to predict Toronto Electricity Price and Demand utilizing Weather, Electricity Supply Data, etc. 

## Repository Structure:
* Dev:
  * Demand
  * Market Price
  * Post Analysis
  * Supply
  * Weather
  * utilities
* Input & Output
  * Input
    * This folder contains all raw data sources.
  * Output
    * This folder contains all processed data, as well as prediction model related outputs. 

* The 'Dev' folder contains all Python scripts and notebooks for the project. This includes data source collection, data source processing, data normalization, and model construction.
  * The 'Demand' folder contains all Python scripts and notebooks handling demand-related data.
  * The 'Market Price' folder contains all Python scripts and notebooks handling price-related data.
  * The 'Post Analysis' folder contains all Python scripts and notebooks related to the model itself.
  * The 'Supply' folder contains all Python scripts and notebooks handling supply-related data.
  * The 'Weather' folder contains all Python scripts and notebooks handling weather-related data.
  * The 'utilities' folder contains all Python scripts that serve as helper functions, providing more readable code.
* The 'Input & Output' contains all the data used for this project.
  * The 'Input' folder contains all raw data sources.
    * The 'Demand' folder contains all raw data related to demand.
    * The 'Market Price' folder contains all raw data related to price.
    * The 'Population' folder contains all raw data related to population.
    * The 'Post Analysis' folder contains all raw data related to the model.
    * The 'Supply' folder contains all raw data related to supply.
    * The 'Weather' folder contains all raw data related to weather. 
  * The 'Output' contains all processed data, as well as prediction model related outputs. 
    * The 'Demand' folder contains all processed data related to demand.
    * The 'Market Price' folder contains all processed data related to price.
    * The 'Population' folder contains all processed data related to population.
    * The 'Post Analysis' folder contains all processed data related to the model.
    * The 'Supply' folder contains all processed data related to supply.
    * The 'Weather' folder contains all processed data related to weather. 

## How to run:
The model is created and trained under \Dev\Post Analysis\Prediction Model\neural_network.ipynb.
Simply edit the input parameter to make a prediction. 

To start from the beginning, below is the execution workflow:
* generate_ontario_demand_time_series.ipynb
* generate_gas_price_time_series.ipynb
* generate_toronto_price_time_series.ipynb
* generate_ontario_supply_time_series.ipynb
* generate_toronto_weather_time_series.ipynb
* generate_all_field_sheet.ipynb
* neural_network.ipynb

## Potential Future Development:
While the current model works great with prediction on Toronto Electricity Demand, the overall performance for Toronto Electricity Price is lacking. This can be an area to consider improving in the future. I suspect with the fundemantal difference between demand and price, it would require exploring a new feature set for Toronto Electricity Price. The correlation between the current feature set with the Toronto Electricity Price is low. 

Another potential improvement is the cleanliness of the code. While I try to develop code in a more readable and reusable way, it is inevitable that there could be room for improvement. 
