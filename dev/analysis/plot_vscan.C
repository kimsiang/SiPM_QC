void plot_vscan(){


    TFile *f1[16];

    char name1[50];

    TTree *tree1[16];
    TTree *tree2[16];

    TH1F *tmp[16];
    TH1F *h[16];
    TF1 *fit[16];
    TF1 *fit_trace[16];

    TCanvas *c1 = new TCanvas("c1","c1",1000,1000);
    TCanvas *c2 = new TCanvas("c2","c2",1000,600);
    c1->Divide(4,4);

    double volt[100]={};
    double mean1[100]={};
    double sigma1[100]={};

    int sipm_no = 10;
    int seq_no = 209;

    for(int i = 0; i<16; i++){

        volt[i] = 65.5 + 0.25*i;

        sprintf(name1,"../data/sipm_%04d/sipm_%04d_volt_%02d_%05d.root",sipm_no, sipm_no, i+1,i+seq_no);

        f1[i] = new TFile(name1);

        //f1[i]->ls();
        //f2[i]->ls();

        tree1[i]=(TTree*)f1[i]->Get("waveform");
        tree2[i]=(TTree*)f1[i]->Get("info");


        c1->cd(i+1);
        tmp[i] = new TH1F("tmp","tmp",1020,-10,500);

        fit[i] = new TF1("fit","gaus(0)",-10,500);

        tree1[i]->Draw("trace_amp>>tmp");

        h[i] = new TH1F("h1","h1",100,tmp[i]->GetMean()-10*tmp[i]->GetRMS(),tmp[i]->GetMean()+10*tmp[i]->GetRMS());

        tree1[i]->Draw("trace_amp>>h1");

        fit[i] = new TF1("fit","gaus(0)",h[i]->GetMean()-3*h[i]->GetRMS(),h[i]->GetMean()+3*h[i]->GetRMS());
        fit[i]->SetParameters(100,h[i]->GetMean(),h[i]->GetRMS());
        fit[i]->SetParLimits(0,0,1000);
        fit[i]->SetParLimits(1,0,500);
        fit[i]->SetParLimits(2,0,30);
        fit[i]->SetLineColor(2);

        h[i]->Fit(fit[i],"REQN");

        cout<<fit[i]->GetParameter(1)<<" "<<fit[i]->GetParameter(2)<<endl;

        mean1[i]=fit[i]->GetParameter(1);
        sigma1[i]=fit[i]->GetParameter(2);

        tree2[i]->Draw("avg_trace:Iteration$>>trace","Iteration$>180 && Iteration$< 340 && Entry$==0","l");

        fit_trace[i] = new TF1("fit_trace","gaus(0)+pol1(3)");
        fit_trace[i]->SetParameters(5,240,2,1,1);
        //        trace[i]->Fit("fit_trace");

        h[i]->GetXaxis()->SetTitle("time [ns]");
        h[i]->GetXaxis()->SetTitle("ADC [mV]");

        char title[20];
        sprintf(title,"V=%02.2f V",volt[i]);
        TText *t22 = new TText(0.15,0.7,title);
        t22->SetNDC(kTRUE);
        t22->SetTextSize(0.05);
        t22->SetTextColor(2);
        t22->Draw();

    }

    char outfile[50];
    sprintf(outfile,"sipm_%04d_avg_trace.pdf",sipm_no);
    c1->Print(outfile);

    c2->cd();
    TGraphErrors *g1 = new TGraphErrors(16,volt,mean1,0,sigma1);
    g1->SetMarkerStyle(20);
    g1->SetMarkerColor(2);
    g1->Draw("AP");
    g1->GetXaxis()->SetTitle("V [V]");
    g1->GetYaxis()->SetTitle("Amp [mV]");

    sprintf(outfile,"sipm_%04d_bias_amp.pdf",sipm_no);
    c2->Print(outfile);


}
