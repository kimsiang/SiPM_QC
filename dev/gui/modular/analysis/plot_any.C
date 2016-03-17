void plot_any(){


    TFile *f1[100];

    char name1[100];

    TTree *tree1[100];
    TTree *tree2[100];

    TH1F *tmp[100];
    TH1F *h[100];
    TF1 *fit[100];
    TF1 *fit_trace[100];
    TGraphErrors *g1[10]; 
    TLegend *leg;

    TCanvas *c1 = new TCanvas("c1","c1",1000,1000);
    TCanvas *c2 = new TCanvas("c2","c2",1000,600);
    c1->Divide(4,4);

    double volt[100]={};
    double mean1[10][100]={};
    double sigma1[10][100]={};

    int sipm_no[]={1,2,3,4,5,6,7,8,10};
    int run_no[]={2,4,6,8,10,12,14,16,24};

    //int sipm_no[]={14, 16, 17, 18};
    // int run_no[]={18, 22, 20, 26};

    int size = sizeof(sipm_no)/sizeof(*sipm_no);

    for(int j = 0; j<size; j++){

        for(int i = 0; i<16; i++){

            sprintf(name1,"/Users/kimsiang/Work/UWCENPA/gm2/Calorimeter/SiPM/L0L1Test/data/sipm_%04d/sipm_%04d_volt_%02d_%04d.root",sipm_no[j], sipm_no[j], i+1,run_no[j]);

            f1[i] = new TFile(name1);
            volt[i] = 66.0 + 0.2*i;
            tree1[i]=(TTree*)f1[i]->Get("waveform");
            tree2[i]=(TTree*)f1[i]->Get("info");


            c1->cd(i+1);
            tmp[i] = new TH1F("tmp","tmp",1620,-10,800);
            fit[i] = new TF1("fit","gaus(0)",-10,800);
            tree1[i]->Draw("trace_amp>>tmp");
            h[i] = new TH1F("h1","h1",50,tmp[i]->GetMean()-10*tmp[i]->GetRMS(),tmp[i]->GetMean()+10*tmp[i]->GetRMS());
            tree1[i]->Draw("trace_amp>>h1");
            fit[i] = new TF1("fit","gaus(0)",h[i]->GetMean()-2*h[i]->GetRMS(),h[i]->GetMean()+2*h[i]->GetRMS());
            fit[i]->SetParameters(100,h[i]->GetMean(),h[i]->GetRMS());
            fit[i]->SetParLimits(0,0,1000);
            fit[i]->SetParLimits(1,0,800);
            fit[i]->SetParLimits(2,0,30);
            fit[i]->SetLineColor(2);

            h[i]->Fit(fit[i],"REQ");

            cout<<fit[i]->GetParameter(1)<<" "<<fit[i]->GetParameter(2)<<endl;
            mean1[j][i]=fit[i]->GetParameter(1);
            sigma1[j][i]=fit[i]->GetParameter(2);
            fit[i]->SetLineColor(2);
            fit[i]->SetNpx(10000);

            //tree2[i]->Draw("avg_trace:Iteration$>>trace","Iteration$>180 && Iteration$< 340 && Entry$==0","l");

            fit_trace[i] = new TF1("fit_trace","gaus(0)+pol1(3)");
            fit_trace[i]->SetParameters(100,240,2,1,1);
            //trace[i]->Fit("fit_trace");

            char title[20];
            sprintf(title,"V=%02.2f V",volt[i]);
            TText *t22 = new TText(0.15,0.7,title);
            t22->SetNDC(kTRUE);
            t22->SetTextSize(0.05);
            t22->SetTextColor(2);
            t22->Draw();
        }


        for(int i=0; i<16; i++){
            sigma1[j][i] /= mean1[j][15];
            mean1[j][i] /= mean1[j][15];
        }


        c2->cd();
        g1[j] = new TGraphErrors(16,volt,mean1[j],0,sigma1[j]);
        g1[j]->SetTitle("SiPM Response");
        g1[j]->GetXaxis()->SetTitle("V [V]");
        g1[j]->GetYaxis()->SetTitle("Normalized Amplitude");
        g1[j]->SetMarkerStyle(20);
        g1[j]->SetMarkerColor(j+1);
        g1[j]->SetLineColor(j+1);
        g1[j]->SetLineWidth(2);
        if(j==0) g1[j]->Draw("APC");
        if(j>0) g1[j]->Draw("samePC");

        if(j==0)leg = new TLegend(0.15,0.35,0.3,0.85);
        char name[20];
        sprintf(name,"SiPM %d",sipm_no[j]);
        leg->AddEntry(g1[j],name,"lp");
    }

    leg->Draw();

    //  char out1[100], out2[100];
    // sprintf(out1,"sipm_%04d_vscan_run_%04d_hist.eps",sipm_no, run_no);
    //  sprintf(out2,"sipm_%04d_vscan_run_%04d_graph.eps",sipm_no, run_no);
    //  c1->Print(out1);
       c2->Print("sipm_pack_1.pdf");

}
