void plot(){


    TFile *f1[18];
    TFile *f2[18];

    char name1[50];
    char name2[50];

    TTree *tree1[18];
    TTree *tree2[18];

    TH1F *h1;

    TCanvas *c1 = new TCanvas("c1","c1",1000,600);
c1->Divide(2,1);

    double volt[18]={};
    double mean1[18]={};
    double mean2[18]={};
    double sigma1[18]={};
    double sigma2[18]={};

    for(int i = 0; i<18; i++){

        sprintf(name1,"../data/sipm_0007/sipm_0007_volt_%02d_%05d.root",i+1,i+19);
        sprintf(name2,"../data/sipm_0007/sipm_0007_volt_%02d_%05d.root",i+1,i+37);

        f1[i] = new TFile(name1);
        f2[i] = new TFile(name2);

        //f1[i]->ls();
        //f2[i]->ls();

        tree1[i]=(TTree*)f1[i]->Get("waveform");
        tree2[i]=(TTree*)f2[i]->Get("waveform");


        h1 = new TH1F("h1","h1",1020,-5,60);
        h2 = new TH1F("h2","h2",1020,-10,500);

        TF1 *fit = new TF1("fit","gaus(0)",-10,500);

        c1->cd(1);
        tree1[i]->Draw("trace_amp>>h1");

        h1 = new TH1F("h1","h1",100,h1->GetMean()-10*h1->GetRMS(),h1->GetMean()+10*h1->GetRMS());
        tree1[i]->Draw("trace_amp>>h1");
        fit->SetParameters(100,h1->GetMean(),h1->GetRMS());
        fit->SetLineColor(2);
        h1->Fit("fit","REQM");
        cout<<fit->GetParameter<<endl;


        c1->cd(2);
        tree2[i]->Draw("trace_amp>>h2");
        h2 = new TH1F("h2","h2",100,h2->GetMean()-10*h2->GetRMS(),h2->GetMean()+10*h2->GetRMS());
        tree2[i]->Draw("trace_amp>>h2");
        fit->SetParameters(100,h2->GetMean(),h2->GetRMS());
        fit->SetLineColor(2);
        h2->Fit("fit","REQM");



    }






}
