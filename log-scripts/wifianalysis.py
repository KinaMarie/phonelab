import os
import numpy as np
import matplotlib as mpl
from matplotlib.dates import WeekdayLocator, DateFormatter 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime, timedelta
from collections import defaultdict


def analyse(path):
#Define the names and the path of the file where graphs will be stored
        fname1 = os.path.join(path,'wifisignal.pdf')
	fname2 = os.path.join(path,'wifibssid.pdf')
	fname3 = os.path.join(path, 'wifibssid1.pdf')
	fname4 = os.path.join(path,'wifiweekly.pdf')
	fname5 = os.path.join(path,'wifissid.pdf')
        pp1 = PdfPages(fname1)
	pp2 = PdfPages(fname2)
	pp3 = PdfPages(fname3)
	ppp = PdfPages(fname4)
#	pp5 = PdfPages(fname5)
        c = 0
        cmap1 = mpl.cm.autumn
        cmap2 = mpl.cm.winter
	cmap3 = mpl.cm.hsv
#Debug file has a debugging purposes
        debug = open(os.path.join(path,'wificheck.txt'), 'w')
        for root,dirs,files in os.walk(path):
                stats = []
                timestamp = []
                filelist = []
		dictionary = {}
	
		bssid = []
		dict_ = defaultdict(list)
		dict2 = defaultdict(list)
		dict3 = defaultdict(list)
#       print fname
#               print dirs
#               print files
                for name in files:
                        filelist.append(os.path.join(root,name))
                filelist.sort(key=os.path.getmtime)
                for filename in filelist:
                        try:
                                log = open(filename,'r')
                        except IOError:
                                print 'File doesnot exit'
                                break
                        for line in log:
                                data = line.split()
                                n = len(data)
                                if n < 10 or data[0].startswith('01') or data[0].startswith('12'):
#                                               print line + filename
                                        continue
                                else:
                                        tag = data[5]
# when collecting signal strength for given tag
                                        if tag.startswith('PhoneLab-StatusMonitorSignal') and data[6].startswith('Signal_Strength'):
						temp = data[7]
						newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						if len(timestamp) == 0:
                                                        timestamp.append(t)
                                                        stats.append(int(temp))
                                                elif timestamp[-1] < t:
                                                        timestamp.append(t)
                                                        stats.append(int(temp))
                                                elif timestamp[0] > t:
                                                        timestamp.insert(0,t)
                                                        stats.insert(0,int(temp))
                                                else:
                                                        for j in xrange(0,len(timestamp)-2):
                                                                if timestamp[j] < t and timestamp[j+1] > t:
                                                                        timestamp.insert(j+1,t)
                                                                        stats.insert(j+1,int(temp))

# when calculating number of times device connected to a bssid each day
					if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
						#debug.write('SSID: %s   BSSID: %s\n' % (data[7],data[9]))
						newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						key = data[9]
						dict_[key].append(t.date())
						dict2[t.date()].append(key)
						ssid = data[7]
						if len(dict3[ssid]) == 0:
							dict3[ssid].append(key)
						try:
							dict3[ssid].index(key)
						except ValueError:
							dict3[ssid].append(key)
		log.close()
#************ GRAPH PLOTTING SECTION ***********************
		names = []
		for item in dict3:
			names.append(item)
#		print names
#		print dict3
		c = c+1		#c -> figure number, each device will have distinct graph
#Getting device name from the path
                device = root.split('/')

#Graph for wifi signals normalised over each hour
		t = []
                s = []
                temp = 0
                count = 0
#                debug.write('Normalised wifi signals ---> %s\n' % root)
                if len(timestamp) > 0:
                        current = timestamp[0]
                        for i in xrange(1,len(timestamp)-1):
                                if timestamp[i].hour==current.hour:
                                        temp += stats[i]
                                        temp = temp / 2
                                else:
                                        t.append(timestamp[i-1])
                                        s.append(temp)
                                        current = timestamp[i]
#                                       debug.write('%s : %s \n' % (t[-1],s[-1]))
                        t.append(timestamp[i])
                        s.append(temp)

		if len(s) > 0:
			fig1 = figure(c, dpi=10)
			plot(t,s,color=cmap1(0.5),marker='o')
			grid()
			title('Wifi Signals received by %s' % device[-1], fontsize=12)
			xlabel('Time', fontsize=12)
			ylabel('Signal Strength in dB', fontsize=12)
			pp1.savefig(fig1)
			close()
			fig1.clear()

#Graph for plotting number of times a device connected to each BSSID each day
#Step 1 : count number of times bssid appeared for each unique date
			col = np.random.random(len(dict_))	
#			print col
			fig2 = figure(c, dpi=10)
			for item in dict_:
#				debug.write('%s : %s\n' % (item, dict_[item]))
				current = list(dict_[item])
#				print('The list is : %s' % item)
				dates = []
				new_count = []
#				print item
				for i in xrange(0,len(current)):
					if len(dates) == 0 or dates.count(current[i]) == 0:
						dates.append(current[i])
						new_count.append(current.count(dates[-1]))
#					else:
#						index = dates.index(current[i])
#						new_count[index] += 1				
				
				plot(dates,new_count, '--o', label=item)
				grid()
				legend(handlelength=10)
			title('Number of times %s connects to different BSSID' % device[-1])
			xlabel('Time', fontsize=15)
			ylabel('Number of times', fontsize=15)
			pp2.savefig(fig2)
			close()
			fig2.clear()
			
#Graph for visualising total number of connections to access points per device
		debug.write('*************************************')
		if len(dict2) > 0:
			x = []
			y = []
			fig3 = figure(c,dpi=10)
			for item in dict2:
				current = list(dict2[item])
				bssid_count = len(current)
				y.append(bssid_count)
				x.append(item)
			bar(x,y,width=.5, color = cmap1(0.4))
			title('Number of access points %s connects to each day' % device[-1])
			pp3.savefig(fig3)
			close()
			fig3.clear()
#Graph for visualising total number of connections to AP where consecutive connections to same AP are discarded
		if len(dict2) > 0:
			x = []
			y = []
			fig4 = figure(c,dpi=10)
			for item in dict2:
#				print('The list2 is : %s' % dict2[item])
				current = list(dict2[item])
				bssid_count = 0
				debug.write('The list is %s \n' % current)
				for i in xrange(0,len(current)):
					debug.write('%s \n' % current[i])
					if i == 0 or current[i] != current[i-1]:
						bssid_count += 1
				y.append(bssid_count)
				x.append(item)
#				print len(current),bssid_count
			bar(x,y,color = cmap1(0.8))
			title('Visualising possible movement of %s each day----> less height = less movement' % device[-1])
			xlabel('Time', fontsize=15)
			ylabel('Number of connections', fontsize=15)
			pp3.savefig(fig4)
			close()
			


#Graph for visualising connections to access point in a weekly basis
		
			if len(dict2) > 0:
				num = 10
	                        x = []
        	                y = []
#                	        fig4 = figure(c)
#				ax = fig4.add_subplot(111)
                        	for item in dict2:
#                               print('The list2 is : %s' % dict2[item])
	                                current = list(dict2[item])
        	                        bssid_count = 0
                	                debug.write('The list is %s \n' % current)
                        	        for i in xrange(0,len(current)):
                                	        debug.write('%s \n' % current[i])
                                        	if i == 0 or current[i] != current[i-1]:
                                                	bssid_count += 1
	                                
					if len(x) == 0 or item > x[-1]:
						x.append(item)
						y.append(bssid_count)
					elif item < x[0]:
						x.insert(0,item)
						y.insert(0,bssid_count)
					else:
						for n in xrange(len(x)-1,1):
							if item < x[n] and item > x[n-1]:
								x.insert(n,item)
								y.insert(n,bssid_count)
								break
#				print x	
				flag = 0
				col = random()
				for i in xrange(0, len(x)):
					
					if x[i] - x[flag] >= timedelta(days=6):
#						print 'inside the conditional phase'
#						print x[i], x[flag], flag, i
						num += 2
						fig4 = figure(c,dpi=10)
		                                ax = fig4.add_subplot(111)
						m = i+1
#					ax.plot_date(x[flag:m],y[flag:m],'--o')
						ax.bar(x[flag:m],y[flag:m], width=.35, color = cmap2(col))
		                                title('From %s-%s -- %s' % (x[flag],x[i],device[-1]))
        		                        xlabel('Time', fontsize=15)
	              		                ylabel('Number of connections', fontsize=15)
                        		        ax.xaxis.set_major_locator(WeekdayLocator(byweekday = (MO,TH,SA)))
                                		ax.xaxis.set_major_formatter(DateFormatter('%A \n%d %b'))

						m = i+1
#						print x[flag:m]
						flag = i+1
						ppp.savefig(fig4)
						close()
						fig4.clear()

#Graph for visualising contribution of different ssids
		if len(dict2) > 0 and len(dict3) > 0:
                        x = []
                        y = []
			p = []
			stats = defaultdict(list)
#			print 'Length ', len(names)
			num = [0]*len(names)	
			n = 0
                        fig5 = figure(c,dpi=10)
                        for item in dict2:
#                               print('The list2 is : %s' % dict2[item])
                                current = list(dict2[item])
                                
                                for i in xrange(0,len(current)):
#                                        debug.write('%s \n' % current[i])			 
                                       if i == 0 or current[i] != current[i-1]:
						for key in dict3:
							l = list(dict3[key])
#							print l
							try:
								if l.index(current[i]) >= 0:
#									print names.index(key)
									num[names.index(key)] +=1
#									print 'Found : ', key, current[i]
									break
							except ValueError:
								continue
				for j in xrange(0, len(names)):
					stats[names[j]].append(num[j])
		
                                x.append(item)
#                               print len(current),bssid_count
#			print stats
#			print x
			for key in stats:
	                	bar(x,stats[key],color = cmap3(random()))
				print key
			legend(names)
                        title('Contribution of different network -- %s' % device[-1])
                        xlabel('Time', fontsize=15)
                        ylabel('Number of connections', fontsize=15)
                        pp3.savefig(fig5)
                        close()


#Graph for visualing in each day different devicse connect to how many access points
				

#Closing the files that are open
	pp1.close()
	pp2.close()
	pp3.close()
	ppp.close()
#	pp5.close()
	debug.close()
