import numpy as np
import matplotlib.pyplot as plt
import ROOT

f_root = ROOT.TFile.Open('data1.root','RECREATE')
hist0 = ROOT.TH1D("hist0","Baseline Subtracted Pulse",700,0,700)
hist1 = ROOT.TH1D("hist1","Baseline Subtracted PHS",3000,0,3000)
hist2 = ROOT.TH1D("hist2","Timing Spectrum",100,0,100)
hist3 = ROOT.TH2D("hist3","Pulse Height Vs PSD",100,100,2000,100,0,1)

vals = []
inverted_wf = []
mynewhandle = open("waveform-DT5730-ch-0-2017-08-24-11-11-08.txt", "r")
while True:                            # Keep reading forever
    theline = mynewhandle.readline()   # Try to read next line
    if len(theline) == 0:              # If there are no more lines
        break                          #     leave the loop

    # Now process the line we've just read
    vals.append(float(theline))
    if len(vals) == 700:
        average = np.mean(vals[0:10])
        for i in np.arange(0,700):
            inverted_wf.append(average - vals[i])
        x = np.arange(0,700)
        y = np.array(inverted_wf)
        for j in np.arange(0,700):
            hist0.SetBinContent(int(x[j]),y[j])
        max = hist0.GetMaximum()
        max_bin = hist0.GetMaximumBin()
        hist1.Fill(max)
        
        a = hist0.GetMaximum()
        b = (0.20*a)
        c = hist0.GetMaximumBin()

        while a > b:
            a = a-9
            c = c-1
        timing = c
        hist2.Fill(timing)

        long_integral = hist0.Integral(timing,700)
        short_integral = hist0.Integral(200,700)
        psd = short_integral/long_integral
        hist3.Fill(max,psd)
        
        vals = []
        inverted_wf = []
        hist0.Reset()

    

mynewhandle.close()

f_root.Write()
f_root.Close()
