import pandas as pd

folder = r"E:\Gilbos Machines\SmarTwist\Maintenance\20210824 Dixie\CTS data\W2021_33"
file = "CTS_GMS2_26134.2_b1cd2a4815830104775578113a61ade98040249c_2021-08-16-84328.csv"
file = folder + "\\" + file

line = "DT;SZ;mmin;SnID;NrSgm;f1;f2;f3;f4;f5;f6;f7;f8;f9;f10;f11;f12;f13;f14;f15;f16;S1;S2;S3;S4;S5;S6;S7;S8;S9;S10;S11;S12;S13;S14;S15;S16;FT1;FT2;FT3;FT4;FT5;FT6;FT7;FT8;FT9;FT10;FT11;FT12;FT13;FT14;FT15;SnNOK;FTNOK;Shrt;Inv;TSlw;ADCOv;ADCFlt;UndFlt;V;#Tens"
line2 = "DT;SZ;mmin;SnID;NrSgm;f1;f2;f3;f4;f5;f6;f7;f8;f9;f10;f11;f12;f13;f14;f15;f16;S1;S2;S3;S4;S5;S6;S7;S8;S9;S10;S11;S12;S13;S14;S15;S16;FT1;FT2;FT3;FT4;FT5;FT6;FT7;FT8;FT9;FT10;FT11;FT12;FT13;FT14;FT15;SnNOK;FTNOK;Shrt;Inv;TSlw;ADCOv;ADCFlt;UndFlt;V;#Tens"

# infile = open(file, 'r')
# firstLine = infile.readline().rstrip()

firstLine = open(file, 'r').readline().rstrip()

print(line == firstLine)
print(line2 is firstLine)