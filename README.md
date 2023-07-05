## Solar Power Control and Management
<br>
<br>
<p>
The solar power plant is based on the conversion of sunlight into 
electricity. As the use of solar energy has been increased nowadays. Not only 
we save the electricity with the help of a solar power plant but it also contributes 
towards the environment. It converts solar energy into electricity either directly 
using photovoltaics. Nowadays we are using machine learning model. The main 
necessity of Artificial intelligence is data. The past dataset is collected and that 
dataset is used to build a machine learning model. The necessary pre-processing 
techniques are applied like univariate analysis and bivariate analysis are 
implemented. The data is visualised for better understanding of the features and 
based on that a classification model is built by using machine learning algorithm 
and comparison of algorithms are done based on their performance metrics like 
accuracy MAE, MSE, R2
</p>
<br>
<hr>
<h2>Hardware Block Diagram</h2>
<img src="https://github.com/prasath9944/Solar-Power-Control/blob/main/templates/readme_files/Hardware_Block_Diagram.png">
<br>
<p>
  The Temperature, Humidity and Light illuminous is send as input to the model using
DHT11 sensor and LDR sensor. Using MAX232 TTL it connects the pc serial
communication between the model and the controller. The model predicts the power
based on the hardware and user inputs the predicted power is displayed in the LCD
display. It checks whether necessary power is sufficient to drive the solar power or
it needs to change it supply to AC through relay tripping.
</p>
<br>
<hr>
<h2>System Architecture</h2>
<img src="https://github.com/prasath9944/Solar-Power-Control/blob/main/templates/readme_files/System_Architecture.png">
