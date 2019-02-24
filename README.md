# Spike-Analysis is the project I done in IMEC. Aiming to pre-process and plot the neuron signal
# Our chip has 1024 channels, you can have your own setting
Launch the code:
(1)Open the terminal.
(2)use the command "cd" to access in the python folder where "NeuronAnalysis" exists.
(3)use the command ""to launch the main code , ig "python NeuronsAnalysis_vKevin.py"
(4)"Set the channle you want to test!" will show up after the previous step is done. Enter an interger of the channel you want to test.
(5)Choose if you want to use default setting by entering "True" or "False" in terminal.
(6)If "False" are entered, input the setting you want:
	Set the channle you want to test!50
	'Import New Data, filter, extract spikes and save the workspace?(answer true or false only):True
	'Load pre-processed data?False
	Saveworkspace of cleaned data?False	
	Raster Plot?Ture
(7)If the wrong input are given, just retry the correct one
	Invalid input please enter True or False!
	Raster Plot?True
	Invert Data?False
	Clean Spike Map Data?False
(8)If any plot is shown, you have to close it to continue the next line.otherwise it will pause it. If you don't want it, add "plt.close()"
  right after each "plt.show()" in the code.
