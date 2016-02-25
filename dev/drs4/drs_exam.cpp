/********************************************************************\

Name:         drs_exam.cpp
Created by:   Stefan Ritt

Contents:     Simple example application to read out a DRS4
evaluation board

$Id: drs_exam.cpp 21308 2014-04-11 14:50:16Z ritt $

\********************************************************************/

#include <math.h>
#include "TTree.h"
#include "TFile.h"
#include "iostream"

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

using namespace std;
extern int errno;
/*------------------------------------------------------------------*/

int
main ()
{
  int i, j, nBoards;
  DRS *drs = NULL;
  DRSBoard *b = NULL;
  bool rootCheck = true;
  float time_array[8][1024];
  float wave_array[8][1024];
  TFile *pf = NULL;
  TTree *pt_wfd = NULL;
  FILE *f;
  FILE *fout;

  if (1)
    printf ("Get DRS ......\n");
  /* do initial scan */

  if (drs)
    delete drs;
  drs = new DRS ();

  printf ("Get boards ......\n");
  /* show any found board(s) */
  if (b)
    delete b;

  for (i = 0; i < drs->GetNumberOfBoards (); i++)
    {
      b = drs->GetBoard (i);
      //          printf("Found DRS4 evaluation board, serial #%d, firmware revision %d\n", 
      //                b->GetBoardSerialNumber(), b->GetFirmwareVersion());
    }

  printf ("Get number of boards ......\n");

  /* exit if no board found */
  nBoards = drs->GetNumberOfBoards ();
  if (nBoards == 0)
    {
      printf ("No DRS4 evaluation board found\n");
      return 0;
    }

  printf ("Continue working with the first board ......\n");
  /* continue working with first board only */
  b = drs->GetBoard (0);

  printf ("Initializing the board ......\n");
  /* initialize board */
  b->Init ();

  printf ("Set the sampling frequency to 1 GSPS ......\n");
  /* set sampling frequency */
  b->SetFrequency (1, true);

  /* enable transparent mode needed for analog trigger */
  b->SetTranspMode (1);

  printf ("Set the input range from -0.5V to +0.5V\n");
  /* set input range to -0.5V ... +0.5V */
  b->SetInputRange (0.0);

  /* use following line to set range to 0..1V */
  //b->SetInputRange(0.5);

  /* use following line to turn on the internal 100 MHz clock connected to all channels  */
  b->EnableTcal (1);

  /* use following lines to enable hardware trigger on CH1 at 50 mV positive edge */
  if (b->GetBoardType () >= 8)
    {				// Evaluaiton Board V4&5
      b->EnableTrigger (1, 0);	// enable hardware trigger
      b->SetTriggerSource (1 << 2);	// set CH3 as source
    }
  else if (b->GetBoardType () == 7)
    {				// Evaluation Board V3
      b->EnableTrigger (0, 1);	// lemo off, analog trigger on
      b->SetTriggerSource (0);	// use CH1 as source
    }
  b->SetTriggerLevel (0.150);	// 0.05 V
  b->SetTriggerPolarity (true);	// positive edge

  /* use following lines to set individual trigger elvels */
  b->SetIndividualTriggerLevel (1, -0.050);
  //b->SetIndividualTriggerLevel(2, 0.2);
  b->SetIndividualTriggerLevel (3, 0.15);
  //b->SetIndividualTriggerLevel(4, 0.4);
  //b->SetTriggerSource(15);

  b->SetTriggerDelayNs (900);	// zero ns trigger delay

  /* use following lines to enable the external trigger */
  //if (b->GetBoardType() == 8) {     // Evaluaiton Board V4
  //   b->EnableTrigger(1, 0);           // enable hardware trigger
  //   b->SetTriggerSource(1<<4);        // set external trigger as source
  //} else {                          // Evaluation Board V3
  //   b->EnableTrigger(1, 0);           // lemo on, analog trigger off
  // }


  float max_amp = 0;
  string sipm_no = "";
  string input = "";
  char outputFile[100], name1[100], name2[100], fname1[100], fname2[100];


  /* continuous loop of 300 events  (each measurement = 300 events) */
  for (j = 0; j < 300; j++)
    {

      if (j == 0)
	{

	  // get SiPM serial number, will be pushed into the loop later on
	  cout << "Please enter the SiPM#:\n>";
	  getline (cin, sipm_no);
	  if (sipm_no == "exit" || sipm_no == "")
	    {
	      cout << "Exiting DRS4 DAQ ......" << endl;
	      break;
	    }

	  cout << "You have entered: " << sipm_no << endl;

	  // Enter the LED number (SIPM CH number)
	  cout << "Please enter the LED#:\n>";
	  getline (cin, input);
	  if (input == "exit")
	    {
	      cout << "Exiting DRS4 DAQ ......" << endl;
	      break;
	    }

	  cout << "You have entered: " << input << endl;

	  /* create the data folder to store all the measured data  */
	  struct stat st;
	  if (stat ("./data/", &st) == 0)
	    {
	      cout << "(#1) ./data/ is present ......" << endl;
	    }

	  else
	    {

	      int d = mkdir ("./data/", S_IRWXU);

	      if (d != 0)
		{
		  printf ("mkdir failed; errno=%d\n", errno);
		}

	      else
		{
		  printf ("created the directory ./data/\n");
		}
	    }


	  /* check if a folder for sipm_no exists */
	  struct stat st1;
	  struct stat st2;
	  int test_no = 0;
	  sprintf (fname1, "./data/sipm_%s_%02d/", sipm_no.c_str (), test_no);
	  sprintf (fname2, "./data/sipm_%s_%02d/sipm_%s_18.txt",
		   sipm_no.c_str (), test_no, sipm_no.c_str ());

	  while (stat (fname1, &st1) == 0 && stat (fname2, &st2) == 0)
	    {
	      cout << "(#2a) " << fname1 << " is present ......" << endl;
	      cout << "(#2b) " << fname2 << " is present ......" << endl;
	      ++test_no;
	      cout << test_no << endl;
	      sprintf (fname1, "./data/sipm_%s_%02d/", sipm_no.c_str (), test_no);
	      sprintf (fname2, "./data/sipm_%s_%02d/sipm_%s_18.txt",
		       sipm_no.c_str (), test_no, sipm_no.c_str ());
	    }

	  /* create a folder for each sipm_no */
	  //            sprintf(name0,"./data/sipm_%s_%02d/",sipm_no.c_str(), test_no);
	  struct stat st3;
	  if (stat (fname1, &st3) == 0)
	    {
	      cout << "(#3) " << fname1 << " is present ......" << endl;
	    }

	  else
	    {

	      int e = mkdir (fname1, S_IRWXU);

	      if (e != 0)
		{
		  printf ("mkdir failed; errno=%d\n", errno);
		}

	      else
		{
		  printf ("created the directory %s\n", fname1);
		}
	    }

	  /* open txt file to save waveforms */
	  sprintf (name1, "./data/sipm_%s_%02d/sipm_%s_%s.txt",
		   sipm_no.c_str (), test_no, sipm_no.c_str (), input.c_str ());
	  f = fopen (name1, "w");

	  sprintf (name2, "./data/sipm_%s_%02d/sipm_%s_%s_full.txt",
		   sipm_no.c_str (), test_no, sipm_no.c_str (), input.c_str ());
	  fout = fopen (name2, "w");

	  if (f == NULL || fout == NULL)
	    {
	      perror ("ERROR: Cannot open file \"data.txt\"");
	      return 1;
	    }

	  /* set up appropriate output files */
	  if (rootCheck)
	    {			// initialize root file, tree, and branches otherwise open */
	      sprintf (outputFile, "./data/sipm_%s_%02d/sipm_%s_%s.root",
		       sipm_no.c_str (), test_no, sipm_no.c_str (), input.c_str ());
	      pf = new TFile (outputFile, "recreate");
	      pt_wfd = new TTree ("WFDTree", "Waveform Arrays");
	      pt_wfd->Branch ("Channel1", &wave_array[0], "wave_array[1024]/F");
	      pt_wfd->Branch ("Time", &time_array[0], "time_array[1024]/F");
	    }


	}


      /* start board (activate domino wave) */
      b->StartDomino ();

      /* wait for trigger */
      // printf("Waiting for trigger...");

      fflush (stdout);

      while (b->IsBusy ());

      /* read all waveforms */
      b->TransferWaves (0, 8);

      /* read time (X) array of first channel in ns */
      b->GetTime (0, 0, b->GetTriggerCell (0), time_array[0]);

      /* decode waveform (Y) array of first channel in mV */
      b->GetWave (0, 0, wave_array[0]);

      /* read time (X) array of second channel in ns
         Note: On the evaluation board input #1 is connected to channel 0 and 1 of
         the DRS chip, input #2 is connected to channel 2 and 3 and so on. So to
         get the input #2 we have to read DRS channel #2, not #1. */
      b->GetTime (0, 2, b->GetTriggerCell (0), time_array[1]);

      /* decode waveform (Y) array of second channel in mV */
      b->GetWave (0, 2, wave_array[1]);

      /* Save waveform: X=time_array[i], Yn=wave_array[n][i] */
      //      fprintf(f, "Event #%d ----------------------\n  t1[ns]  u1[mV]  t2[ns] u2[mV]\n", j);
      max_amp += *std::max_element (&wave_array[0][0], &wave_array[0][1023]) / 300;
      fprintf (f, "%5.1f\n", *std::max_element (&wave_array[0][0], &wave_array[0][1023]));


      if (rootCheck)
	{
	  pt_wfd->Fill ();	// fill root tree
	}

      if (j % 50 == 0)
	{
	  for (i = 0; i < 1024; i++)
	    {
	      fprintf (fout, "%7.3f %7.1f\n", time_array[0][i], wave_array[0][i]);
	    }
	}
      //cout<<time_array[0][i]<<" "<< wave_array[0][i]<<endl;
      //fprintf(f,"%7.1f",*std::max_element(&wave_array[0][0],&wave_array[0][1023]));
      //fprintf(f, "%7.3f %7.1f %7.3f %7.1f\n", time_array[0][i], wave_array[0][i], time_array[1][i], wave_array[1][i]);
      /* print some progress indication */
      if (j % 100 == 0)
	{
	  printf ("Event #%d read successfully\n", j);
	}

      if (j == 299)
	{
	  j = -1;
	  cout << max_amp << endl;
	  fclose (f);
	  fclose (fout);
	  if (rootCheck)
	    {
	      pf->Write ();	// write root file
	      pf->Close ();
	    }
	  max_amp = 0;
	}
    }


  /* delete DRS object -> close USB connection */
  delete drs;
}
