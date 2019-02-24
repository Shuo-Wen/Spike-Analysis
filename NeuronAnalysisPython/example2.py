import tkinter as tk
import sys
import matplotlib.pyplot as plt

if (LoadData)
	sys.modules[__name__].__dict__.clear()
    Full_Path2 = [path,fileOld];
    print('Data Loaded.');


###################################################################Plot of a selected channel with overlapping spike waveforms
## Convert the spike time index from samples to seconds
#check the size!!!
	ichan = 100;
	spk_idx_T = np.zeros(((len(spk_idx)),(len(spk_idx)),dtype=float);

for i in range(len(spk_idx))
    spk_idx_T[i]=spk_idx[i]/fs

plt.subplot(1,4,1:3)

################################################################### Plot the data waveform ########################################################
plt.plot(time.T,fdata[ichan,:].*1e3)
plt.xlabel('Time, (s)')
plt.ylabel('Voltage, (\muV)');

if (ImportNewData)
    title([sprintf('ch %.f,', ichan), fileNew], 'Interpreter', 'none')
elseif (LoadData)
    clear title;
    title([sprintf('ch %.f,', ichan), fileOld], 'Interpreter', 'none');
end
xlim([0,time(1,end)]);
hold all
% Plot of the spike marker
plot(spk_idx_T{ichan},fdata(ichan,spk_idx{ichan}).*1e3,'or','LineWidth',2)
hold all
plot([0,time(1,end)],[0,0]-thresh(ichan).*1e3)
% Plot the zoomed spike
subplot(1,4,4)
hold all
t_spk_w_T=t_spk_w./fs; % [s]
%figure;
if length(spk_idx{ichan})
    plot(t_spk_w,spk_w{ichan}'.*1e3,'k','linewidth',0.5)
    %hold on;
    plot(t_spk_w,nanmean(spk_w{ichan}).*1e3,'r','linewidth',2)  
    ylabel('Voltage, (\muV)','FontSize',15, 'FontWeight','Bold');
    set(gca,'fontsize',15,'FontWeight','Bold')
end
