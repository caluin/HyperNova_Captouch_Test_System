import sys
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

class cap_analysis:
    def __init__(self,filename,column_name,test_config): 
        self.useful_min = 0
        self.useful_max = 1000000
        self.filename = filename
        self.column_name = column_name
        self.test_config = test_config
        self.semtech = False
        if self.filename.endswith('_xy1.csv'):
            self.semtech = True
        self.df = pd.read_csv(self.filename)
        if (test_config != 'noise'):
            self.find_pad_centers()
        self.table={}
        if self.test_config == 'full_scan_hover':
            fig,(self.ax1,self.ax2) = plt.subplots(2,1)
        elif self.test_config == 'linearity_jitter':
            fig,(self.ax3,self.table['Jitter']) = plt.subplots(2,1)
        elif self.test_config == 'noise':
            fig,(self.table['Noise']) = plt.subplots(1,1)
        elif self.test_config == 'arbitrary_x_hover':
            fig,self.ax4 = plt.subplots(1,1)
        fig.tight_layout()

    def show_plot(self):
        plt.show()
        
    def find_pad_centers(self):
        def find_center(column_name):
            y_min = 0
            if self.semtech:
                index = self.df[column_name].loc[(self.df['y']>=y_min) & (self.df[column_name]>=self.useful_min) & (self.df[column_name]<=self.useful_max)].idxmax()
            else:
                index = self.df[column_name].loc[self.df['y']>=y_min].idxmin()
            return self.df.loc[index,'x']
        if self.semtech:
            center1 = find_center(self.column_name+'1')
            center2 = find_center(self.column_name+'2')
            center3 = find_center(self.column_name+'3')
            center4 = find_center(self.column_name+'4')
            center5 = find_center(self.column_name+'5')
            center6 = find_center(self.column_name+'6')
            self.centers = {'pad 1':center1,'pad 2':center2,'pad 3':center3,'pad 4':center4,'pad 5':center5,'pad 6':center6}
        else:
            center1 = find_center(self.column_name+'1')
            center2 = find_center(self.column_name+'2')
            center3 = find_center(self.column_name+'3')
            center4 = find_center(self.column_name+'4')
            self.centers = {'pad 1':center1,'pad 2':center2,'pad 3':center3,'pad 4':center4}

    def find_noise(self):
        def stats(df,column_name):
            mean = df[column_name].mean()
            std = df[column_name].std()
            minimum = df[column_name].min()
            maximum = df[column_name].max()
            return {'mean':mean,'std':std,'min':minimum,'max':maximum}

        def position(df,pad,count):
            column_name = self.column_name+str(count)
            df = df.loc[df['y'] > 0]
            result = stats(df,column_name)
            return {pad:result}

        result = {}
        self.centers = {'pad1':0,'pad2':0,'pad3':0,'pad4':0}
        pad = 'pad1'
        result[0] = position(self.df,pad,1)
        pad = 'pad2'
        result[1] = position(self.df,pad,2)
        pad = 'pad3'
        result[2] = position(self.df,pad,3)
        pad = 'pad4'
        result[3] = position(self.df,pad,4)
        val=[]
        try:
            for pad,result0 in result.items():
                center = list(result0.keys())[0]
                stat = result0[center]
                val.append([int(pad),int(stat['mean']),round(stat['std'],1),stat['min'],stat['max']])
                df = pd.DataFrame(val,columns=['pad','mean(cap)','std(cap)','min(cap)','max(cap)'])
                self.table['Noise'].axis('off')
                self.table['Noise'].table(cellText=df.values, colLabels=df.columns, loc='upper center')
                self.table['Noise'].set_title('Noise'+'\n'+self.filename.split('/')[-1])
        except:
            print("Noise figure invalid, Y position is 0(probe touches the glass), this may not be a noise measurement\n")
        return result

    def find_jitter(self):
        def stats(df,column_name):
            mean = df[column_name].mean()
            std = df[column_name].std()
            minimum = df[column_name].min()
            maximum = df[column_name].max()
            return {'mean':mean,'std':std,'min':minimum,'max':maximum}

        def position(df,center):
            if self.semtech:
                column_name = 'diffE'
            else:
                column_name = 'Slider reported position'
            #remove slider position of 65535 since it's invalid
            df1 = self.df.loc[self.df[column_name]!=65535]
            df1 = df1.loc[df['x'] == center]
            min_y = df1['y'].min()
            df  = df1.loc[df['y']==min_y]
            result = stats(df,column_name)
            return {center:result}

        result = {}
        for pad,center in self.centers.items():
            result[pad] = position(self.df,center)

        val=[]
        try:
            for pad,result0 in result.items():
                center = list(result0.keys())[0]
                stat = result0[center]
                val.append([pad,round(center,1),int(stat['mean']),round(stat['std'],1),stat['min'],stat['max']])
            df = pd.DataFrame(val,columns=['pad','center(mm)','mean(slider)','std(slider)','min(slider)','max(slider)'])
            self.table['Jitter'].axis('off')
            self.table['Jitter'].table(cellText=df.values, colLabels=df.columns, loc='upper center')
            self.table['Jitter'].set_title('Jitter'+'\n'+self.filename.split('/')[-1])
        except:
            print("Jitter figure invalid. It's possible that center was found using instant slider value but no correct slider position value for that center pad is found.\n")
        return result

    def plot_full_scale(self):
        df = self.df.loc[self.df['y']>=0.00]
        x  = df['x']
        if self.semtech:
            y1 = df[self.column_name+'1']
            y2 = df[self.column_name+'2']
            y3 = df[self.column_name+'3']
            y4 = df[self.column_name+'4']
            y5 = df[self.column_name+'5']
            y6 = df[self.column_name+'6']
            self.ax1.plot(x,y1,'o-',markersize=1,label='pad 1')
            self.ax1.plot(x,y2,'o-',markersize=1,label='pad 2')
            self.ax1.plot(x,y3,'o-',markersize=1,label='pad 3')
            self.ax1.plot(x,y4,'o-',markersize=1,label='pad 4')
            self.ax1.plot(x,y5,'o-',markersize=1,label='pad 5')
            self.ax1.plot(x,y6,'o-',markersize=1,label='pad 6')
            self.ax1.set_ylim([self.useful_min,self.useful_max])
        else:
            y1 = df[self.column_name+'1']
            y2 = df[self.column_name+'2']
            y3 = df[self.column_name+'3']
            y4 = df[self.column_name+'4']
            self.ax1.plot(x,y1,'o-',markersize=1,label='pad 1')
            self.ax1.plot(x,y2,'o-',markersize=1,label='pad 2')
            self.ax1.plot(x,y3,'o-',markersize=1,label='pad 3')
            self.ax1.plot(x,y4,'o-',markersize=1,label='pad 4')
        self.ax1.set_title('full scale '+self.column_name+'\n'+self.filename.split('/')[-1])
        self.ax1.set_xlabel('mm parallel to DUT surface')
        self.ax1.set_ylabel('captouch')
        self.ax1.grid(True)
        self.ax1.legend()
        # plt.show()

    def plot_hover(self):
        peaks = list(self.centers.values())

        if self.semtech:
            df1 = self.df.loc[self.df['x']==peaks[0]]
            df2 = self.df.loc[self.df['x']==peaks[1]]
            df3 = self.df.loc[self.df['x']==peaks[2]]
            df4 = self.df.loc[self.df['x']==peaks[3]]
            df5 = self.df.loc[self.df['x']==peaks[4]]
            df6 = self.df.loc[self.df['x']==peaks[5]]
            x1 = df1['y']
            y1 = df1[self.column_name+'1']
            x2 = df2['y']
            y2 = df2[self.column_name+'2']
            x3 = df3['y']
            y3 = df3[self.column_name+'3']
            x4 = df4['y']
            y4 = df4[self.column_name+'4']
            x5 = df5['y']
            y5 = df5[self.column_name+'5']
            x6 = df6['y']
            y6 = df6[self.column_name+'6']
            self.ax2.plot(x1,y1,'o-',markersize=5,label='pad 1')
            self.ax2.plot(x2,y2,'o-',markersize=5,label='pad 2')
            self.ax2.plot(x3,y3,'o-',markersize=5,label='pad 3')
            self.ax2.plot(x4,y4,'o-',markersize=5,label='pad 4')
            self.ax2.plot(x5,y5,'o-',markersize=5,label='pad 5')
            self.ax2.plot(x6,y6,'o-',markersize=5,label='pad 6')
        else:
            df1 = self.df.loc[self.df['x']==peaks[0]]
            df2 = self.df.loc[self.df['x']==peaks[1]]
            df3 = self.df.loc[self.df['x']==peaks[2]]
            df4 = self.df.loc[self.df['x']==peaks[3]]
            x1 = df1['y']
            y1 = df1[self.column_name+'1']
            x2 = df2['y']
            y2 = df2[self.column_name+'2']
            x3 = df3['y']
            y3 = df3[self.column_name+'3']
            x4 = df4['y']
            y4 = df4[self.column_name+'4']
            self.ax2.plot(x1,y1,'o-',markersize=5,label='pad 1')
            self.ax2.plot(x2,y2,'o-',markersize=5,label='pad 2')
            self.ax2.plot(x3,y3,'o-',markersize=5,label='pad 3')
            self.ax2.plot(x4,y4,'o-',markersize=5,label='pad 4')

        self.ax2.set_title('Hover @ pad centers '+ self.column_name+'\n'+self.filename.split('/')[-1])
        self.ax2.set_xlabel('mm distance from DUT surface')
        self.ax2.set_ylabel('captouch')
        self.ax2.grid(True)
        self.ax2.legend()
        # plt.show()

    def plot_arbitrary_x_hover(self):
        disabled_x = self.df.loc[0,'x',]
        df = self.df.loc[self.df['x']==disabled_x]
        x = df['y']
        y1 = df[self.column_name+'1']
        y2 = df[self.column_name+'2']
        y3 = df[self.column_name+'3']
        y4 = df[self.column_name+'4']
        self.ax4.plot(x,y1,'o-',markersize=5,label='pad 1')
        self.ax4.plot(x,y2,'o-',markersize=5,label='pad 2')
        self.ax4.plot(x,y3,'o-',markersize=5,label='pad 3')
        self.ax4.plot(x,y4,'o-',markersize=5,label='pad 4')
        self.ax4.set_title('Hover @ X='+str(round(disabled_x,1)) + "mm " + self.column_name+'\n'+self.filename.split('/')[-1])
        self.ax4.set_xlabel('mm distance from DUT surface')
        self.ax4.set_ylabel('captouch')
        self.ax4.grid(True)
        self.ax4.legend()

    def plot_linearity(self):
        if self.semtech:
            min_y = self.df['y'].min()
            df = self.df.loc[self.df['y']==min_y]
            df = df.loc[df['diffE']<=400]
            y1 = df['diffE'] 
        else:
            df = self.df.loc[self.df['y']==0]
            #remove slider position greater than 100 since it's invalid
            df = df.loc[df['Slider reported position']<=100]
            y1 = df['Slider reported position']
        x = df['x']
        d = np.polyfit(x,y1,1)
        f = np.poly1d(d)
        fx = f(x)
        max_delta = max(np.abs(fx-y1))
        self.ax3.plot(x,y1,'o',marker=1,label='position')
        self.ax3.plot(x,fx)
        # self.ax3.set_ylim(0,100)
        self.ax3.set_title('Linearity max delta = '+str(round(max_delta,1))+'\n'+self.filename.split('/')[-1])
        self.ax3.set_xlabel('probe position mm')
        self.ax3.set_ylabel('DUT reported position')
        self.ax3.grid(True)
        self.ax3.legend()
        # plt.show()


if __name__ == '__main__':
    filename = 'C:/Users/wenhaochen/Documents/GitHub/interface_motor/data/Xrubber_tip_finger_probe_full_scale_hover_Stella_slider_2022-05-23_20-32-52_DUT_xy.csv'

    column_name = 'Slider instant'
    my_analysis = cap_analysis(filename,column_name)
    my_analysis.plot_full_scale()
    my_analysis.plot_hover()
    my_analysis.plot_linearity()
    result=my_analysis.find_noise()
    print('noise')
    pprint(result)
    result=my_analysis.find_jitter()
    print('jitter')
    pprint(result)
    # plt.show()
    my_analysis.show_plot()