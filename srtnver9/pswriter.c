//This program reads in a specified set of spectrum data from a .rad data file from the SRT and produces a postscript plot of the spectrum

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <sched.h>
 
int main(void)
{
	char txt[80], fnam[80], datafile[80];
	int i, j, jmax, k, np, j1, j2, n3, npoint, yr, da, hr, mn, sc, obsn1, obsn2;
	double xx, yy, dmax, ddmax, dmin, slope, dd, ddd, totpp, scale, sigma, freq, freqq, fstart, fstop, vstart, vstop, xoffset;
	double freqsep, x1, x2, y1, y2, wid, sx, sy, yoffset, x, y, xp, yp, av, avx, avy, avxx, avxy, psx1, psx2, psy1, psy2, yps;
	double restfreq;

//Added variables for data input from file
	double aznow, elnow, tsys, tant, vlsr, glat, glon, bw, fbw, integ;
	int nfreq, nsam, bsw, intp;
	char soutrack[80], buf[80];
	double pp[512];
	FILE *file1 = NULL;
	FILE *dfile=NULL;

//Ask user to enter name of data file to be read
	printf("Enter name of data file: ");
	scanf("%s", datafile);
	if ((dfile = fopen(datafile, "r")) == NULL) {
            printf("cannot read %s\n", datafile);
            return 0;
        }

//Ask user to enter observation to be read
	printf("Enter observation number to read: ");
	scanf("%d", &obsn1);


	obsn2=-1; //Initialize obsn2 for first comparison
	while(obsn1!=obsn2)	//Scan in data file until entered and scanned observation numbers match
	{
	//Scan in first two lines of data
		fscanf(dfile, "%[^\n]\n", buf);
		if (buf[0] == '*')
		{
			fscanf(dfile, "DATE %4d:%03d:%02d:%02d:%02d obsn %3d az %lf el %lf freq_MHz %lf Tsys %lf Tant %lf vlsr %lf glat %lf glon %lf source %s\n",
				&yr, &da, &hr, &mn, &sc, &obsn2, &aznow, &elnow, &freq, &tsys, &tant, &vlsr, &glat, &glon, soutrack);
		} else
		{
			sscanf(buf, "DATE %4d:%03d:%02d:%02d:%02d obsn %3d az %lf el %lf freq_MHz %lf Tsys %lf Tant %lf vlsr %lf glat %lf glon %lf source %s\n",
        	      	         &yr, &da, &hr, &mn, &sc, &obsn2, &aznow, &elnow, &freq, &tsys, &tant, &vlsr, &glat, &glon, soutrack);
		}
		fscanf(dfile, "Fstart %lf fstop %lf spacing %lf bw %lf fbw %lf MHz nfreq %d nsam %d npoint %d integ %lf sigma %lf bsw %d\n",
      	                 &fstart, &fstop, &freqsep, &bw, &fbw, &nfreq, &nsam, &npoint, &integ, &sigma, &bsw);
	//Calculate a few things that are based on early data in the file and are needed to define later scanning from the file
		np = npoint;
		j1 = np * 0;
		j2 = np * 1;
	//Scan in spectrum data
		fscanf(dfile, "Spectrum %2d integration periods\n", &intp);
	        for (j=0; j<j2; j++)
			fscanf(dfile, "%lf ", &pp[j]);
	        fscanf(dfile, "\n");
		if (fabs(pp[0] - pp[1]) > 200)
		{
			intp = 1;
			fseek(dfile, -9 * np, SEEK_CUR);
			fscanf(dfile, "Spectrum \n");
			for (j=0; j<j2; j++)
				fscanf(dfile, "%lf ", &pp[j]);
			fscanf(dfile, "\n");
		}
	}

//Print out scanned data
	printf("Data scanned from file:\n");
	printf("DATE %4d:%03d:%02d:%02d:%02d obsn %3d az %3.0f el %2.0f freq_MHz %10.4f Tsys %6.3f Tant %6.3f vlsr %7.2f glat %6.3f glon %6.3f source %s\n",
                        yr, da, hr, mn, sc, obsn2, aznow, elnow, freq, tsys, tant, vlsr, glat, glon, soutrack);
	printf("Fstart %8.3f fstop %8.3f spacing %8.6f bw %8.3f fbw %8.3f MHz nfreq %d nsam %d npoint %d integ %5.0f sigma %8.3f bsw %d\n",
                        fstart, fstop, freqsep, bw, fbw, nfreq, nsam, npoint, integ, sigma, bsw);
	printf("Spectrum     %d integration periods\n", intp);
	for (j=0; j<j2; j++)
		printf("%8.3f ", pp[j]);
	printf("j=%d\n", j);

//Write postscript set up commands

	printf("\nEnter postscript file name: ");
	scanf("%s", fnam);
        if ((file1 = fopen(fnam, "wx")) == NULL) {
            printf("cannot write %s\n", fnam);
            return 0;
        }
        fprintf(file1, "%%!PS-Adobe-\n%c%cBoundingBox:  0 0 612 792\n%c%cEndProlog\n", '%', '%', '%', '%');
        fprintf(file1, "1 setlinewidth\n");
        fprintf(file1, "/Times-Roman findfont\n 10 scalefont\n setfont\n");
        fprintf(file1, "0 0 0 sethsbcolor\n");



//Set up graphing parameters
        wid = 500.0;
        sx=5.0/wid;
        sy=5.0/wid;
        dmax = ddmax = -1.0e99;
        dmin = 1.0e99;
        dd = 0.0;
        jmax = 0;
        av = avx = avy = avxx = avxy = 0.0;

//    for (j = j1; j < j2+1; j++) {
    for (j = 0; j < np; j++) {
        dd = pp[j];
        if (j >= j1 && j < j2) {
            avx += j;
            avy += dd;
            avxx += j * j;
            avxy += j * dd;
            av++;
            if (dd > ddmax)
                ddmax = dd;
        }
    }
    slope = (-avx * avy + av * avxy) / (av * avxx - avx * avx);
    for (j = j1; j < j2; j++) {
        if (np > 1)
            pp[j] -= slope * (double) (j - j1) / ((double) (j2 - j1) - 1.0);
        dd = pp[j];
        if (dd > dmax) {
            dmax = dd;
            jmax = j;
        }
        if (dd < dmin)
            dmin = dd;
    }
    xoffset = 80.0;
    yoffset = 50.0;
    yps = 450.0;
    if (dmax > dmin)
        scale = 1.2 * (dmax - dmin);
    else
        scale = 1.0;
    if (freqsep > 0.0)
        xx = floor(freq / freqsep) * freqsep;
    else
        xx = freq;

    if (np > 1) {
        sprintf(txt, "%4d:%03d:%02d:%02d:%02d", yr, da, hr, mn, sc);
        x1 = (125 + xoffset) * sx;
        y1 = (yoffset - 20.0) * sy;
        psx1 = x1 / sx;
        psy1 = yps - y1 / sy;
        fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
        sprintf(txt, "integ. %5.1f m", (intp * nsam) / (2.0e6 * bw * 60.0));
        x1 = (xoffset + 200.0) * sx;
        y1 = (yoffset + 15.0) * sy;
        psx1 = x1 / sx;
        psy1 = yps - y1 / sy;
        fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
        if (soutrack[0] > 0) {
            sprintf(txt, "%s", soutrack);
            x1 = (xoffset + 20.0) * sx;
            y1 = (yoffset + 15.0) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
            if (!strstr(soutrack, "Sun") && !strstr(soutrack, "Moon")) {
                sprintf(txt, "Galactic l = %3.0f b = %3.0f", glon, glat);
                x1 = (xoffset + 60.0) * sx;
                y1 = (yoffset + 15.0) * sy;
                psx1 = x1 / sx;
                psy1 = yps - y1 / sy;
                fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
            }
        }
        for (y = 0; y < 2; y++) {
            x1 = xoffset * sx;
            y1 = (yoffset + y * 319) * sy;
            x2 = (xoffset + 320) * sx;
            y2 = (yoffset + y * 319) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            psx2 = x2 / sx;
            psy2 = yps - y2 / sy;
            fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                        psx2, psy2);
            x1 = (xoffset + y * 320) * sx;
            y1 = (yoffset) * sy;
            x2 = (xoffset + y * 320) * sx;
            y2 = (yoffset + 319) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            psx2 = x2 / sx;
            psy2 = yps - y2 / sy;
            fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                        psx2, psy2);
        }

        yp = 0;
        xp = (npoint - 1) * 320.0 / (double) npoint;
        for (j = 1; j < npoint; j++) {
            x = (npoint - j) * 320.0 / (double) npoint;
            xx = j / (double) npoint;
            k = (int) (xx * (double) np + 0.5);
            if (k >= np)
                k = np - 1;
            if (scale > 0.0)
                totpp = (pp[k] - dmin) / scale;
            else
                totpp = 0;
            y = (260.0 - totpp * 260.0);
            if (y < 0)
                y = 0;
            if (y > 260)
                y = 260;
            if (j == 1)
                yp = y;
            if (y != yp) {
                if (k >= j1 + 1 && k < j2 - 1)
                    i = 1;
                else
                    i = 0;
                if (i) {
                    x1 = (x + xoffset) * sx;
                    y1 = (yoffset + yp) * sy;
                    x2 = (xp + xoffset) * sx;
                    psx1 = x1 / sx;
                    psy1 = yps - y1 / sy;
                    psx2 = x2 / sx;
                    psy2 = yps - y2 / sy;
                    fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1,
                                psy1, psx2, psy1);
                }
                xp = x;
                if (y > yp && i) {
                    x1 = (x + xoffset) * sx;
                    y1 = (yoffset + yp) * sy;
                    y2 = (yoffset + y) * sy;
                    psx1 = x1 / sx;
                    psy1 = yps - y1 / sy;
                    psx2 = x2 / sx;
                    psy2 = yps - y2 / sy;
                    fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1,
                                psy1, psx1, psy2);
                }
                if (yp > y && i) {
                    x1 = (x + xoffset) * sx;
                    y1 = (yoffset + y) * sy;
                    y2 = (yoffset + yp) * sy;
                    psx1 = x1 / sx;
                    psy1 = yps - y1 / sy;
                    psx2 = x2 / sx;
                    psy2 = yps - y2 / sy;
                    fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1,
                                psy1, psx1, psy2);
                }
            }
            yp = y;
        }

        if (freq > 1500.0)
        restfreq = 1612.201;    // OH line
	else
		restfreq=1420.405752;
        fstart = freq + (double) (1 - np / 2) * freqsep;
        fstop = freq + (double) (np - 1 - np / 2) * freqsep;
        vstart = -vlsr - (fstop - restfreq) * 299790.0 / restfreq;
        vstop = -vlsr - (fstart - restfreq) * 299790.0 / restfreq;
        ddd = fstop - fstart;
        n3 = (int) (ddd) + 1;
        ddd = 10.0 / n3;
        j1 = (int) (fstart * ddd);
        j2 = (int) (fstop * ddd);
	fprintf(file1, "/Times-Roman findfont\n 10 scalefont\n setfont\n");
        for (j = j1 + 1; j <= j2; j++) {
            dd = ((double) (j) / ddd - freq + (double) (np / 2) * freqsep)
                * 320.0 / ((double) (np) * freqsep);
            x1 = (320 - dd + xoffset) * sx;
            y1 = (yoffset + 310.0) * sy;
            x2 = (320 - dd + xoffset) * sx;
            y2 = (yoffset + 319.0) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            psx2 = x2 / sx;
            psy2 = yps - y2 / sy;
            fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                        psx2, psy2);
            sprintf(txt, "%6.1f", j / ddd);
            x1 = (300 - dd + xoffset) * sx;
            y1 = (yoffset + 335.0) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            fprintf(file1, "%f %f moveto\n (%s) show\n", psx1 + 10.0, psy1, txt);
            sprintf(txt, "Frequency (MHz)");
            x1 = (125.0 + xoffset) * sx;
            y1 = (yoffset + 350.0) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
        }
        ddd = 10.0 * n3;
        j1 = (int) (vstart / ddd);
        j2 = (int) (vstop / ddd);
	fprintf(file1, "/Times-Roman findfont\n 8 scalefont\n setfont\n");
        for (j = j1 + 1; j <= j2 - 1; j++) {
            freqq = restfreq - ((double) (j) * ddd + vlsr) * restfreq / 299790.0;
            dd = (freqq - freq + (double) (np / 2) * freqsep)
                * 320.0 / ((double) (np) * freqsep);
            x1 = (320 - dd + xoffset) * sx;
            y1 = (yoffset + 265.0) * sy;
            x2 = (320 - dd + xoffset) * sx;
            y2 = (yoffset + 275.0) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            psx2 = x2 / sx;
            psy2 = yps - y2 / sy;
            fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                        psx2, psy2);
            sprintf(txt, "%5.0f", j * ddd);
            x1 = (300 - dd + xoffset) * sx;
            y1 = (yoffset + 290.0) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            fprintf(file1, "%f %f moveto\n (%s) show\n", psx1 + 10.0, psy1, txt);
            sprintf(txt, "VLSR (km/s)");
            x1 = (135 + xoffset) * sx;
            y1 = (yoffset + 305.0) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
        }
	fprintf(file1, "/Times-Roman findfont\n 10 scalefont\n setfont\n");
        dd = log(scale) / log(2.0) - 0.6;
        if (dd < 0.0)
            j = (int) (dd - 0.5);
        else
            j = (int) (dd + 0.5);
        dd = 0.5 * pow(2.0, (double) j);
        j1 = 0;
        j2 = (int) (scale / dd);
        for (j = 0; j <= j2; j++) {
            y = (int) (260.0 - ((double) j * dd / scale) * 260.0);
            if (y > 0) {
                x1 = xoffset * sx;
                y1 = (yoffset + y) * sy;
                x2 = (10 + xoffset) * sx;
                y2 = (yoffset + y) * sy;
                psx1 = x1 / sx;
                psy1 = yps - y1 / sy;
                psx2 = x2 / sx;
                psy2 = yps - y2 / sy;
                fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                            psx2, psy2);
                sprintf(txt, "%5.1fK", j * dd);
                x1 = (xoffset - 30) * sx;
                y1 = (yoffset + y + 2.0) * sy;
                psx1 = x1 / sx;
                psy1 = yps - y1 / sy;
                fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
            }
        }
        yy = ((3.0 * sigma) / scale) * 260.0;
        if (yy > 0.0) {
            x1 = (xoffset + 310) * sx;
            y1 = (yoffset + 10) * sy;
            x2 = (xoffset + 310) * sx;
            y2 = (yoffset + yy + 10) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            psx2 = x2 / sx;
            psy2 = yps - y2 / sy;
            fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                        psx2, psy2);
            x1 = (xoffset + 305) * sx;
            y1 = (yoffset + 10) * sy;
            x2 = (xoffset + 315) * sx;
            y2 = (yoffset + 10) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            psx2 = x2 / sx;
            psy2 = yps - y2 / sy;
            fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                        psx2, psy2);
            x1 = (xoffset + 305) * sx;
            y1 = (yoffset + yy + 10) * sy;
            x2 = (xoffset + 315) * sx;
            y2 = (yoffset + yy + 10) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            psx2 = x2 / sx;
            psy2 = yps - y2 / sy;
            fprintf(file1, "newpath\n %5.1f %5.1f moveto \n %5.1f %5.1f lineto\nstroke\n", psx1, psy1,
                        psx2, psy2);
            sprintf(txt, "3-sigma");
            x1 = (xoffset + 270) * sx;
            y1 = (yoffset + yy * 0.5 + 14) * sy;
            psx1 = x1 / sx;
            psy1 = yps - y1 / sy;
            fprintf(file1, "%f %f moveto\n (%s) show\n", psx1, psy1, txt);
        }
    }
        fprintf(file1, "showpage\n%c%cTrailer\n", '%', '%');
        fclose(file1);
        sprintf(txt, "file: %s written", fnam);
        x1 = (xoffset + 5) * sx;
        y1 = (yoffset + 440) * sy;
return 0;
}
