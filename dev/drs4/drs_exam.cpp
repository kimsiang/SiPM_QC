/********************************************************************\

Name:         drs_exam.cpp
Created by:   Stefan Ritt

Contents:     Simple example application to read out a DRS4
evaluation board

$Id: drs_exam.cpp 21308 2014-04-11 14:50:16Z ritt $

Modified by:   Kim Siang Khaw (khaw84@uw.edu)
Date:          2016-03-13
Contents:      Fast drs4 application to used by UW SiPM QC GUI

\********************************************************************/

#include <math.h>
#include "TTree.h"
#include "TFile.h"
#include "iostream"
#include <zmq.h>
#include <assert.h>

#ifdef _MSC_VER

#include <windows.h>

#elif defined(OS_LINUX)

#define O_BINARY 0

#include <unistd.h>
#include <ctype.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>

#define DIR_SEPARATOR '/'

#endif

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <algorithm>

#include "strlcpy.h"
#include "DRS.h"

const int MAX_EVENT = 500;
const int MAX_SAMPLE = 1024;

using namespace std;
extern int errno;
/*------------------------------------------------------------------*/

int main (){

    int evtno_, nBoards_;
    DRS *drs_ = NULL;
    DRSBoard *board_ = NULL;
    float time_array[8][MAX_SAMPLE]={};
    float wave_array[8][MAX_SAMPLE]={};
    float avg_wave_array[MAX_SAMPLE]={};
    float trace_max=0;
    float trace_min=0;
    float trace_amp=0;
    float trace_baseline=0;
    float time_max=0;
    float time_min=0;
    TFile *rootfile_ = NULL;
    TTree *infotree_ = NULL;
    TTree *waveformtree_ = NULL;
    FILE *ampfile_ = NULL;
    FILE *wavefile_ = NULL;

    /* do initial scan */
    if (drs_)
        delete drs_;
    drs_ = new DRS ();

    /* exit if no board found */
    nBoards_ = drs_->GetNumberOfBoards ();
    if (nBoards_ == 0) {
        printf ("No DRS4 evaluation board found\n");
        return 0;
    }

    /* show any found board(s) */
    if (board_)
        delete board_;

    /* continue working with first board only */
    board_ = drs_->GetBoard (0);

    if (board_) {
        printf("Found DRS4 evaluation board, serial #%d, firmware revision %d\n", 
                board_->GetBoardSerialNumber(), board_->GetFirmwareVersion());
    }

    else return 0;

    /* Reset the usb device in case it was shutdown improperly */
    libusb_reset_device(board_->GetUSBInterface()->dev);

    /* initialize board */
    board_->Init ();

    /* set sampling frequency */
    board_->SetFrequency (1, true);

    /* enable transparent mode needed for analog trigger */
    board_->SetTranspMode (1);

    /* set input range to -0.5V ... +0.5V */
    board_->SetInputRange (0.0);

    /* use following line to turn on the internal 100 MHz clock connected to all channels  */
    board_->EnableTcal (1);

    /* use following lines to enable hardware trigger on CH1 at 50 mV positive edge */
    if (board_->GetBoardType () >= 8) {				// Evaluaiton Board V4&5
        board_->EnableTrigger (1, 0);	// enable hardware trigger
        board_->SetTriggerSource (1 << 2);	// set CH3 as source
    }

    else if (board_->GetBoardType () == 7) {				// Evaluation Board V3
        board_->EnableTrigger (0, 1);	// lemo off, analog trigger on
        board_->SetTriggerSource (0);	// use CH1 as source
    }

    board_->SetTriggerLevel (0.150);	// 0.05 V
    board_->SetTriggerPolarity (true);	// positive edge

    /* use following lines to set individual trigger elvels */
    board_->SetIndividualTriggerLevel (1, -0.050);
    //board_->SetIndividualTriggerLevel(2, 0.2);
    board_->SetIndividualTriggerLevel (3, 0.15);
    //board_->SetIndividualTriggerLevel(4, 0.4);
    //board_->SetTriggerSource(15);

    board_->SetTriggerDelayNs (900);	// zero ns trigger delay

    board_->StartClearCycle();
    board_->FinishClearCycle();
    board_->Reinit();

    string sipm_no = "";
    string type = "";
    string subrun = "";
    string seq_no = "";
    string begin = "";
    char fileroot_[100], name1_[100], name2_[100], fname_[100];

    /* Prepare our context and socket */
    void *context = zmq_ctx_new ();
    void *responder = zmq_socket (context, ZMQ_REP);
    int rc = zmq_bind (responder, "tcp://*:5555");
    assert (rc == 0);

    /* continuous loop of 500 events  (each measurement = 500 events) */
    for (evtno_= 0; evtno_< MAX_EVENT; evtno_++) {

        if (evtno_== 0) {
            
            /* get SiPM serial number, run type, subrun# and seq# */
            char buffer [20];
            cout << "Please enter the (SiPM#, Run type, Subrun#, Seq#)\n";
            zmq_recv (responder, buffer, 20, 0);
            printf ("Received %s\n", buffer);
            char *word;
            
            word = strtok(buffer, " ");
            printf("1st word: %s\n", word);
            sipm_no = word;
            word = strtok(NULL, " ");
            printf("2nd word: %s\n", word);
            type = word;
            word = strtok(NULL, " ");
            printf("3rd word: %s\n", word);
            subrun = word;
            word = strtok(NULL, " ");
            printf("4th word: %s\n", word);
            seq_no = word;

            //char *test[10];

            cout << "Please enter the (SiPM#, Run type, Subrun#, Seq#)\n";
            //cin >> sipm_no >> type >> subrun >> seq_no;
            cout << "You have entered: " << sipm_no << " " << type <<" " << subrun <<" " << seq_no <<endl;

            if (sipm_no == "q" || sipm_no == "q" || subrun == "q" || seq_no == "q") {
                cout << "Exiting DRS4 DAQ ......" << endl;
                break;
            }


            /* create the data folder to store all the measured data  */
            struct stat st;
            if (stat ("./data/", &st) == 0){
                cout << "(#1) ./data/ is present ......" << endl; }

            else {
                int d = mkdir ("./data/", S_IRWXU);

                if (d != 0) {
                    printf ("mkdir failed; errno=%d\n", errno); }
                else {
                    printf ("created the directory ./data/\n"); }
            }

            /* check if a folder for sipm_no exists */
            struct stat st1;
            sprintf (fname_, "./data/sipm_%s/", sipm_no.c_str ());

            if (stat (fname_, &st1) == 0) {
                cout << "(#2) " << fname_ << " is present ......" << endl; }

            else {int e = mkdir (fname_, S_IRWXU);

                if (e != 0) {
                    printf ("mkdir failed; errno=%d\n", errno);
                }

                else {
                    printf ("created the directory %s\n", fname_);
                }
            }

            /* open txt file to save waveforms */
            sprintf (name1_, "./data/sipm_%s/sipm_%s_%s_%s_%s.txt",
                    sipm_no.c_str (),  sipm_no.c_str (), type.c_str(), subrun.c_str (), seq_no.c_str());
            ampfile_ = fopen (name1_, "w");

            sprintf (name2_, "./data/sipm_%s/sipm_%s_%s_%s_%s_full.txt",
                    sipm_no.c_str (), sipm_no.c_str (), type.c_str(), subrun.c_str (), seq_no.c_str());
            wavefile_ = fopen (name2_, "w");

            if (ampfile_ == NULL || wavefile_ == NULL) {
                printf ("ERROR: Cannot open data files %s and %s!!", name1_, name2_);
                return 1;
            }

            /* set up appropriate output files */
            // initialize root file, tree, and branches otherwise open */
            sprintf (fileroot_, "./data/sipm_%s/sipm_%s_%s_%s_%s.root",
                    sipm_no.c_str (), sipm_no.c_str (), type.c_str(), subrun.c_str (), seq_no.c_str());
            rootfile_ = new TFile (fileroot_, "recreate");
            infotree_ = new TTree ("info", "Event Info");
            infotree_->Branch ("sipm_no", &sipm_no);
            infotree_->Branch ("type", &type);
            infotree_->Branch ("subrun", &subrun);
            infotree_->Branch ("seq_no", &seq_no);
            infotree_->Branch ("avg_trace", &avg_wave_array, "avg_trace[1024]/F");
            waveformtree_ = new TTree ("waveform", "Waveform Arrays");
            waveformtree_->Branch ("trace", &wave_array[0], "wave_array[1024]/F");
            waveformtree_->Branch ("time", &time_array[0], "time_array[1024]/F");
            waveformtree_->Branch ("trace_max", &trace_max, "trace_max/F");
            waveformtree_->Branch ("trace_min", &trace_min, "trace_min/F");
            waveformtree_->Branch ("trace_amp", &trace_amp, "trace_amp/F");
            waveformtree_->Branch ("trace_baseline", &trace_baseline, "trace_baseline/F");
            waveformtree_->Branch ("time_max", &time_max, "time_max/F");
            waveformtree_->Branch ("time_min", &time_min, "time_min/F");

        } // end of if statement for first event

        /* start board (activate domino wave) */
        board_->StartDomino ();

        /* wait for trigger */
        // printf("Waiting for trigger...");

        fflush (stdout);

        while (board_->IsBusy ());

        /* read all waveforms */
        board_->TransferWaves (0, 8);

        /* read time (X) array of first channel in ns */
        board_->GetTime (0, 0, board_->GetTriggerCell (0), time_array[0]);

        /* decode waveform (Y) array of first channel in mV */
        board_->GetWave (0, 0, wave_array[0]);

        /* read time (X) array of second channel in ns */
        /* Note: On the evaluation board input #1 is connected to channel 0 and 1 of */
        /* the DRS chip, input #2 is connected to channel 2 and 3 and so on. So to */
        /* get the input #2 we have to read DRS channel #2, not #1. */
        //board_->GetTime (0, 2, board_->GetTriggerCell (0), time_array[1]);

        /* decode waveform (Y) array of second channel in mV */
        //board_->GetWave (0, 2, wave_array[1]);

        /* Save waveform: X=time_array[i], Yn=wave_array[n][i] */
        // fprintf(f, "Event #%d ----------------------\n  t1[ns]  u1[mV]  t2[ns] u2[mV]\n", evtno_);

        /* get trace max and min */
        trace_max = *std::max_element (&wave_array[0][175], &wave_array[0][225]);
        trace_min = *std::min_element (&wave_array[0][175], &wave_array[0][225]);

        /* get time max and min */
        time_max = std::distance(&wave_array[0][0], std::max_element (&wave_array[0][175], &wave_array[0][225]));
        time_min = std::distance(&wave_array[0][0], std::min_element (&wave_array[0][175], &wave_array[0][225]));

        float trace_avg = 0;

        for(int smpno_ = 0; smpno_ < MAX_SAMPLE; smpno_++) {

            /* get trace average */
            avg_wave_array[smpno_] += wave_array[0][smpno_];
            trace_avg += wave_array[0][smpno_];

            /* get trace baseline */
            if(smpno_ < 150) {
                trace_baseline += wave_array[0][smpno_];}
        }

        /* Calculate the amplitude after substracting the baseline */
        trace_baseline /= 150.; 
        trace_avg /= float(MAX_SAMPLE); 
        trace_amp = trace_max - trace_baseline;

        fprintf (ampfile_, "%5.1f\n", trace_amp);

        waveformtree_->Fill ();


        /* dump run summary at the last event */
        if (evtno_== MAX_EVENT - 1) { 
            printf ("Event #%d read successfully\n", evtno_);

            /* reset the event number to -1 */
            evtno_= -1;

            for (int smpno_ = 0; smpno_ < MAX_SAMPLE; smpno_++){
                avg_wave_array[smpno_] /= float(MAX_EVENT);
                fprintf (wavefile_, "%7.3f %7.1f\n", time_array[0][smpno_], avg_wave_array[smpno_]);
            }

            /* close output files */
            fclose (ampfile_);
            fclose (wavefile_);
            zmq_send (responder, "Finished!", 9, 0);

            /* fill and close ROOT output files */
            infotree_->Fill();
            rootfile_->Write ();	
            rootfile_->Close ();

        } // end of if statement for last event
    }

    /* delete DRS object -> close USB connection */
    delete drs_;
}
