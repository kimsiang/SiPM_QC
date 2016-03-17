#include <iostream>

void plot_Vbd(){

gStyle->SetOptFit();
    TCanvas *c1 = new TCanvas("c1","c1",800,600);

    gStyle->SetMarkerSize(1.5);
    gStyle->SetLabelSize(0.04,"xy");
    gStyle->SetTitleSize(0.04,"xy");

    double v1[20];
    double v2[20];

    double a1_10[20];
    double a2_10[20];
    double a1_20[20];
    double a2_10_err[20];

    int n1=0;
    int n2=0;

    ifstream file1("L0_vbd_sipm_1.txt");
    ifstream file2("vbd.txt");

    // read from the files (format = Vbias, Amp_gain10, Amp_gain20)
    while(file1>>v1[n1]>>a1_10[n1]>>a1_20[n1]){
        n1++;
    }

    while(file2>>v2[n2]>>a2_10[n2]>>a2_10_err[n2]){
        n2++;
    
    }


    TGraph *g1_10 = new TGraph(n1,v1,a1_10);
    TGraph *g1_20 = new TGraph(n1,v1,a1_20);
    TGraphErrors *g2_10 = new TGraphErrors(n2,v2,a2_10,0,a2_10_err);

//    g1_20->GetXaxis()->SetLimits(64,69);
//    g1_20->GetYaxis()->SetRangeUser(0,300);
    g2_10->GetXaxis()->SetTitle("V_{bias} [V]");
    g2_10->GetYaxis()->SetTitle("Amp [mV]");

    g2_10->SetTitle("Amplitude versus V_{bias} ");
    g2_10->Draw("AP");
//    g1_20->Draw("Psame");
 //   g2_10->Draw("Psame");

    g1_10->SetMarkerStyle(20);
    g1_20->SetMarkerStyle(24);
    g2_10->SetMarkerStyle(20);

    g1_10->SetMarkerColor(2);
    g1_20->SetMarkerColor(2);
    g2_10->SetMarkerColor(2);

    leg = new TLegend(0.15,0.6,0.68,0.85);
    leg->AddEntry(g2_10,"SiPM #1, Gain 10, V_{bd}~65.5 V","pe");
//   leg->AddEntry(g1_20,"SiPM #1, Gain 20, V_{bd}~65.5 V","p");
//    leg->AddEntry(g2_10,"SiPM #1, Gain 10, V_{bd}~65.5 V","p");
    leg->SetTextSize(0.04);
    leg->Draw();
}
