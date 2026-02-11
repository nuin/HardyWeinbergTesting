NOMAINWIN

[Win000]
WindowWidth = 500 : WindowHeight = 350
DW = DisplayWidth : DH = DisplayHeight : WW = WindowWidth : WH = WindowHeight
UpperLeftX = int((DW-WW)/2) : UpperLeftY = int((DH-WH)/2) : BackgroundColor$ = "lightgray"
Win000 = 1

MENU #Win000, "File", "Exit", [end_win000]

STATICTEXT #Win000.Text001, "HARDY WEINBERG EQUILIBRIUM TEST",                                                          WW/2-190,  20, 406, 30
STATICTEXT #Win000.Text002, "Copyright 2006-2019 by Fernando A. Bautzer Santos, Renan B. Lemes and Paulo A. Otto",      WW/2-215,  65, 450, 15
STATICTEXT #Win000.Text003, "Departamento de Genetica e Biologia Evolutiva, Universidade de Sao Paulo",                 WW/2-180,  80, 450, 15
STATICTEXT #Win000.Text004, "Rua do Matao, 277",                                                                        WW/2-50,  95, 450, 15
STATICTEXT #Win000.Text005, "05508-090 - Sao Paulo, SP, Brazil",                                                         WW/2-80,   110, 450, 15
STATICTEXT #Win000.Text006, "otto@usp.br",                                                                              WW/2-30,  125, 450, 15
STATICTEXT #Win000.Text007, "Number of alleles:",                                                                       WW/2-130, 175, 130, 30
TEXTBOX    #Win000.TextBox001,                                                                                          WW/2+20,  170, 100, 25
BUTTON     #Win000.Button001, "Next", [alleles], UL,                                                                    WW/2-20,  230

OPEN "Hardy Weinberg Equilibrium Test" FOR window_nf AS #Win000
PRINT #Win000, "trapclose [end_win000]"
PRINT #Win000.Text001, "!font Arial 15"
PRINT #Win000.Text007, "!font Arial 13"
PRINT #Win000.TextBox001, "!setfocus";
WAIT

[end_win000]
CONFIRM "Are you sure you want to quit?"; quit$
IF quit$ = "no" THEN WAIT
Win000 = 0
CLOSE #Win000
WAIT

[alleles]
PRINT #Win000.TextBox001, "!contents? NAll$";
FOR i = 1 TO len(NAll$)
  NAll1$ = MID$(NAll$, i, 1)
  IF instr("0123456789", NAll1$) = 0 THEN
    NOTICE "The values you just entered are invalid. Only numbers are allowed."
    WAIT
  END IF
NEXT i
IF (val(NAll$) > 12 OR val(NAll$) < 2) THEN
  NOTICE "The values you just entered are invalid. Choose a number between 2 and 12."
  WAIT
END IF
NAll = val(NAll$)
IF NAll > 2 THEN GOTO [Win004]

[Win001]
WindowWidth = 800 : WindowHeight = 600
DW = DisplayWidth : DH = DisplayHeight : WW = WindowWidth : WH = WindowHeight
UpperLeftX = int((DW-WW)/2) : UpperLeftY = int((DH-WH)/2) : BackgroundColor$ = "lightgray"
Win000 = 0 : Win001 = 1 : CLOSE #Win000

MENU #Win001, "File", "Exit", [end_win001]
STATICTEXT #Win001.Text001, "HARDY WEINBERG EQUILIBRIUM TEST", WW/2-190,  20, 406, 30
STATICTEXT #Win001.Text002, "D = N(AA) =", WW/2+80, 195, 60, 30
STATICTEXT #Win001.Text002, "H = N(Aa) =", WW/2+80, 245, 60, 30
STATICTEXT #Win001.Text002, "R = N(aa) =", WW/2+80, 295, 60, 30
GROUPBOX #Win001.GroupBox001, "Statistical Tests", WW/2-330, 120, 290, 340
GROUPBOX #Win001.GroupBox002, "Genotype Data", WW/2+50, 130, 240, 240
CHECKBOX #Win001.CheckBox001, "Chi-square without correction", [win001_cb1_on], [win001_cb1_off], WW/2-310, 150, 240, 20
CHECKBOX #Win001.CheckBox002, "Chi-square with Yates' correction", [win001_cb2_on], [win001_cb2_off], WW/2-310, 180, 240, 20
CHECKBOX #Win001.CheckBox003, "Chi-square with Hogben/Levene correction", [win001_cb3_on], [win001_cb3_off], WW/2-310, 210, 240, 20
CHECKBOX #Win001.CheckBox004, "Chi-square with Cannings and Edwards correction", [win001_cb4_on], [win001_cb4_off], WW/2-310, 240, 260, 20
CHECKBOX #Win001.CheckBox005, "G or log-likelihood test without correction", [win001_cb5_on], [win001_cb5_off], WW/2-310, 270, 240, 20
CHECKBOX #Win001.CheckBox006, "log-likelihood test with continuity correction", [win001_cb6_on], [win001_cb6_off], WW/2-310, 300, 240, 20
CHECKBOX #Win001.CheckBox007, "Fisher's exact test", [win001_cb7_on], [win001_cb7_off], WW/2-310, 330, 240, 20
CHECKBOX #Win001.CheckBox008, "Haldane's exact test", [win001_cb8_on], [win001_cb8_off], WW/2-310, 360, 240, 20
CHECKBOX #Win001.CheckBox009, "Exact probability by simulation", [win001_cb9_on], [win001_cb9_off], WW/2-310, 390, 240, 20
TEXTBOX #Win001.TextBox001, WW/2+150, 190, 100, 25
TEXTBOX #Win001.TextBox002, WW/2+150, 240, 100, 25
TEXTBOX #Win001.TextBox003, WW/2+150, 290, 100, 25
BUTTON #Win001.Button001, "Select all", [win001_button001], UL, WW/2-310, 420, 240, 20
BUTTON #Win001.Button002, "Run", [Win002], UL, WW/2+150, 390

OPEN "Hardy Weinberg Equilibrium Test" FOR window_nf AS #Win001 ' "_nf" = window has no frame and cannot be resized by user
PRINT #Win001, "trapclose [end_win001]"
PRINT #Win001.Text001, "!font Arial 15"

[win0001_cb1_on] PRINT #Win001.CheckBox001, "set" : tests = 1 : WAIT
[win001_cb1_off] PRINT #Win001.CheckBox001, "set" : WAIT
[win001_cb2_on]  tests = tests + 2 : WAIT
[win001_cb2_off] tests = tests - 2 : WAIT
[win001_cb3_on]  tests = tests + 4 : WAIT
[win001_cb3_off] tests = tests - 4 : WAIT
[win001_cb4_on]  tests = tests + 8 : WAIT
[win001_cb4_off] tests = tests - 8 : WAIT
[win001_cb5_on]  tests = tests + 16 : WAIT
[win001_cb5_off] tests = tests - 16 : WAIT
[win001_cb6_on]  tests = tests + 32 : WAIT
[win001_cb6_off] tests = tests - 32 : WAIT
[win001_cb7_on]  tests = tests + 64 : WAIT
[win001_cb7_off] tests = tests - 64 : WAIT
[win001_cb8_on]  tests = tests + 128 : WAIT
[win001_cb8_off] tests = tests - 128 : WAIT
[win001_cb9_on]  tests = tests + 256 : WAIT
[win001_cb9_off] tests = tests - 256 : WAIT

[win001_button001]
IF win001Button001 = 0 THEN
  PRINT #Win001.CheckBox002, "set" : PRINT #Win001.CheckBox003, "set" : PRINT #Win001.CheckBox004, "set"
  PRINT #Win001.CheckBox005, "set" : PRINT #Win001.CheckBox006, "set" : PRINT #Win001.CheckBox007, "set"
  PRINT #Win001.CheckBox008, "set" : PRINT #Win001.CheckBox009, "set"
  tests = 511
  win001Button001 = 1
  PRINT #Win001.Button001, "Unselect all"
 ELSE
  PRINT #Win001.CheckBox002, "reset" : PRINT #Win001.CheckBox003, "reset" : PRINT #Win001.CheckBox004, "reset"
  PRINT #Win001.CheckBox005, "reset" : PRINT #Win001.CheckBox006, "reset" : PRINT #Win001.CheckBox007, "reset"
  PRINT #Win001.CheckBox008, "reset" : PRINT #Win001.CheckBox009, "reset"
  tests = 1
  win001Button001 = 0
  PRINT #Win001.Button001, "Select all"
END IF
WAIT

[import_data_win001]
FILEDIALOG "Import data", "*.txt", FileName$
IF FileName$ = "" THEN
  NOTICE "No file chosen"
 ELSE
  OPEN FileName$ FOR INPUT AS #000
  FOR i = 1 TO 3
    INPUT #000, TempVar
    IF i = 1 THEN PRINT #Win001.TextBox001, TempVar
    IF i = 2 THEN PRINT #Win001.TextBox002, TempVar
    IF i = 3 THEN PRINT #Win001.TextBox003, TempVar
  NEXT i
  CLOSE #000
END IF
WAIT

[end_win001]
CONFIRM "Are you sure you want to quit?"; quit$
IF quit$ = "no" THEN WAIT
IF Win002 = 1 THEN CLOSE #Win002
IF Win003 = 1 THEN CLOSE #Win003
CLOSE #Win001
WAIT

[Win002]
WW = 800 : WindowHeight = 600 : UpperLeftX = 50 : UpperLeftY = 50 : BackgroundColor$ = "lightgray"

PRINT #Win001.TextBox001, "!contents? D$";
PRINT #Win001.TextBox002, "!contents? H$";
PRINT #Win001.TextBox003, "!contents? R$";

FOR i = 1 TO len(D$)
  D1$ = MID$(D$, i, 1)
  IF instr("0123456789", D1$) = 0 THEN
    NOTICE "The values you just entered are invalid. Please run the program again."
    WAIT
  END IF
NEXT i
FOR i = 1 TO len(H$)
  H1$ = MID$(H$, i, 1)
  IF instr("0123456789", H1$) = 0 THEN
    NOTICE "The values you just entered are invalid. Please run the program again."
    WAIT
  END IF
NEXT i
FOR i = 1 TO len(R$)
  R1$ = MID$(R$, i, 1)
  IF instr("0123456789", R1$) = 0 THEN
    NOTICE "The values you just entered are invalid. Please run the program again."
    WAIT
  END IF
NEXT i
D = val(D$) : H = val(H$) : R = val(R$)

EPS = 0.0000000000000000001
N = D + H + R : P = 2 * D + H : Q = H + 2 * R
IF N > 1000 THEN NOTICE "Maximum population size exceeded. Please run the program again." : WAIT

' Warnings
IF D < 0 OR H < 0 OR R < 0 OR P = 0 OR Q = 0 OR N < 3 THEN
  NOTICE "The values you just entered are invalid. Please run the program again."
  WAIT
END IF

Win002 = 1 : TernaryPlot = 0
OPEN "Hardy-Weinberg Equilibrium Testing" FOR text AS #Win002
PRINT #Win002, "!trapclose [end_win002]"

' chi-squared test without correction
FOR i001 = 1 TO 511 STEP 2
  IF tests <> i001 THEN GOTO [notCH1]
  DE0 = P ^ 2 / (4 * N)
  HE0 = P * Q / (2 * N)
  RE0 = Q ^ 2 / (4 * N)
  CH(1) = N * (H * H - 4 * D * R) ^ 2 / (P * Q) ^ 2
  [notCH1]
NEXT i001

' chi-squared test with Yates' continuity correction
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 1
    IF tests <> 2*i001 + j001 THEN GOTO [notCH2]
    CH(2) = N * (abs(H * H - 4 * D * R) - 2 * N) ^ 2 / (P * Q) ^ 2
    [notCH2]
  NEXT j001
NEXT i001

' chi-squared test with Levene/Hogben correction
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 3
    IF tests <> 4*i001 + j001 THEN GOTO [notCH3]
    DE1 = P * (P - 1) / (2 * (2 * N - 1))
    HE1 = P * Q / (2 * N - 1)
    RE1 = Q * (Q - 1) / (2 * (2 * N - 1))
    IF DE1 = 0 THEN DE1 = EPS
    IF HE1 = 0 THEN HE1 = EPS
    IF RE1 = 0 THEN RE1 = EPS
    CH(3) = D ^ 2 / DE1 + H ^ 2 / HE1 + R ^ 2 / RE1 - N
    [notCH3]
  NEXT j001
NEXT i001

' chi-squared test with Cannings & Edwards correction
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 7
    IF tests <> 8*i001 + j001 THEN GOTO [notCH4]
    DE2 = (P ^ 2 - H) / (4 * N)
    HE2 = (P * Q + H) / (2 * N)
    RE2 = (Q ^ 2 - H) / (4 * N)
    IF DE2 = 0 THEN DE2 = EPS
    IF HE2 = 0 THEN HE2 = EPS
    IF RE2 = 0 THEN RE2 = EPS
    CH(4) = D ^ 2 / DE2 + H ^ 2 / HE2 + R ^ 2 / RE2 - N
    [notCH4]
  NEXT j001
NEXT i001

' g-test (log-likelihood test)
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 15
    IF tests <> 16*i001 + j001 THEN GOTO [notCH5]
    D1 = D
    H1 = H / 2
    R1 = R
    IF D1 = 0 THEN D1 = EPS
    IF H1 = 0 THEN H1 = EPS
    IF R1 = 0 THEN R1 = EPS
    GT01 = D1 * log(D1) + 2 * H1 * log(H1) + R1 * log(R1)
    GT01 = GT01 - 2 * (D1 + H1) * log(D1 + H1)
    GT01 = GT01 - 2 * (H1 + R1) * log(H1 + R1)
    GT01 = GT01 + N * log(N)
    CH(5) = GT01 * 2
    [notCH5]
  NEXT j001
NEXT i001

' g-test (log-likelihood test) with correction
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 31
    IF tests <> 32*i001 + j001 THEN GOTO [notCH6]
    IF D1 * R1 < H1 * H1 THEN
      D1 = D1 + .5
      R1 = R1 + .5
      IF H1 >= 1 THEN H1 = H1 - .5
    ELSE
      IF D1 >= 1 THEN D1 = D1 - .5
      IF R1 >= 1 THEN R1 = R1 - .5
      H1 = H1 + .5
    END IF
    GT02 = D1 * log(D1) + 2 * H1 * log(H1) + R1 * log(R1)
    GT02 = GT02 - 2 * (D1 + H1) * log(D1 + H1)
    GT02 = GT02 - 2 * (H1 + R1) * log(H1 + R1)
    GT02 = GT02 + N * log(N)
    CH(6) = GT02 * 2
    [notCH6]
  NEXT j001
NEXT i001

' Obtaining P-values
FOR i = 1 TO 6
  IF CH(i) < EPS THEN
    PC(i) = 1
   ELSE
    v = 1 : w = abs(CH(i)) : GOSUB [CHISQDIS] : PC(i) = PCHI
  END IF
NEXT i

' Fisher exact test
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 63
    FISHFLAG = 0
    IF tests <> 64*i001 + j001 THEN GOTO [notCH7]
    P1 = 0 : PR2 = 0 : PR3 = 0 : P99 = 0
    D99 = D : H99 = H : R99 = R : N99 = N
    IF (D = 0 AND H = 1) OR (R = 0 AND H = 1) THEN
      FISHFLAG = 1
      GOTO [EXACTTEST]
    END IF
    A = D99 : D = R99
    IF int(H99 / 2) = H99 / 2 THEN
      B = H99 / 2 : C = H99 / 2
     ELSE
      IF H > 1 THEN B = (H99 + 1) / 2 : C = (H99 - 1) / 2 ELSE B = 1: C = 0
    END IF
    E = A + C : F = B + D : G = A + B : H = C + D : N = G + H
    IF G > H THEN
      GTEMP = H : H = G : G = GTEMP
      ATEMP = C : C = A : A = ATEMP
      BTEMP = D : D = B : B = BTEMP
    END IF
    IF E > F THEN
      ETEMP = F : F = E : E = ETEMP
      ATEMP = B : B = A : A = ATEMP
      CTEMP = D : D = C : C = CTEMP
    END IF
    IF G > E THEN
      GTEMP = E : E = G : G = GTEMP
      FTEMP = H : H = F : F = FTEMP
      BTEMP = C : C = B : B = BTEMP
    END IF
    IF A > B THEN
      ATEMP = B : B = A : A = ATEMP
      CTEMP = D : D = C : C = CTEMP
      ETEMP = F : F = E : E = ETEMP
    END IF
    AD = A - E * G / N : DA = D - A
    I99 = A : GOSUB [FACTRL] : P1 = P99 : EPS = P1 / 10000
    IF P1 < .00000001 THEN P1 = 0 : PR2 = 0 : PR3 = 0 : GOTO [END_FISHER]
    IF AD = 0 THEN PR2 = (1 - P1) / 2 : PR3 = PR2 : GOTO [END_FISHER]
    FOR I99 = A - 1 TO 0 STEP -1 : GOSUB [FACTRL] : P2 = P99
      IF P1 > P2 THEN PR2 = PR2 + P2
      IF P2 < EPS THEN EXIT FOR
    NEXT I99
    FOR I99 = A + 1 TO G : GOSUB [FACTRL] : P3 = P99
      IF P1 > P3 THEN PR3 = PR3 + P3
      IF P3 < EPS THEN EXIT FOR
    NEXT I99
    [END_FISHER]
    PFISH = P1 + PR2 + PR3
    D = D99 : H = H99 : R = R99 : N = N99
    [notCH7]
  NEXT j001
NEXT i001

' Hardy-Weinberg exact test (Haldane)
[EXACTTEST]
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 127
    IF tests <> 128*i001 + j001 THEN GOTO [notCH8]
    IF int(H / 2) = H / 2 THEN HMIN = 0 ELSE HMIN = 1
    IF D > R THEN HMAX = Q ELSE HMAX = P
    k = N : GOSUB [FACTORIAL] : NFAC = FACT
    k = 2 * N : GOSUB [FACTORIAL] : N2FAC = FACT
    k = P: GOSUB [FACTORIAL] : PFAC = FACT
    k = Q: GOSUB [FACTORIAL] : QFAC = FACT
    CONSTFAC = NFAC - N2FAC + PFAC + QFAC
    D1 = D : H1 = H : R1 = R : GOSUB [FACTOFDHR]
    PROB2 = CONSTFAC - DFAC - HFAC - RFAC + H * log(2) : PROB2 = exp(PROB2)
    PROBT = 0
    FOR H9 = HMIN TO HMAX STEP 2
      H1 = H9: D1 = (P - H1) / 2: R1 = (Q - H1) / 2
      GOSUB [FACTOFDHR] : PROB1 = CONSTFAC - DFAC - HFAC - RFAC + H1 * log(2)
      PROB1 = exp(PROB1) : IF PROB1 <= PROB2 THEN PROBT = PROBT + PROB1
    NEXT H9
    [notCH8]
  NEXT j001
NEXT i001

PRINT #Win002, ""
PRINT #Win002, "                       HARDY-WEINBERG TESTING"
PRINT #Win002, ""
PRINT #Win002, "                       Copyright 2006-2019 by"
PRINT #Win002, "      Fernando A. Bautzer Santos, Renan B. Lemes & Paulo A. Otto"
PRINT #Win002, "            Departamento de Genetica e Biologia Evolutiva"
PRINT #Win002, "                     Universidade de Sao Paulo"
PRINT #Win002, "                         Rua do Matao, 277"
PRINT #Win002, "                   05508-090 Sao Paulo SP, Brazil"
PRINT #Win002, "                            otto@usp.br"
PRINT #Win002, ""
PRINT #Win002, "                                        AA         Aa         aa          N"
PRINT #Win002, "---------------------------------------------------------------------------"
PRINT #Win002, "obs. abs. frequencies                 ";
PRINT #Win002, using("####",D); : PRINT #Win002, "       ";
PRINT #Win002, using("####",H); : PRINT #Win002, "       ";
PRINT #Win002, using("####",R); : PRINT #Win002, "       ";
PRINT #Win002, using("####",N)
PRINT #Win002, "exp. abs. freq. (without correction)  ";
PRINT #Win002, using("####.###",DE0); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",HE0); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",RE0); : PRINT #Win002, "   ";
PRINT #Win002, using("####",N)
PRINT #Win002, "exp. abs. freq. (Hogben/Levene)       ";
PRINT #Win002, using("####.###",DE1); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",HE1); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",RE1); : PRINT #Win002, "   ";
PRINT #Win002, using("####",N)
PRINT #Win002, "exp. abs. freq. (Cannings & Edwards)  ";
PRINT #Win002, using("####.###",DE2); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",HE2); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",RE2); : PRINT #Win002, "   ";
PRINT #Win002, using("####",N)
PRINT #Win002, "---------------------------------------------------------------------------"
PRINT #Win002, "obs. rel. frequencies                 ";
PRINT #Win002, using("####.###",D/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",H/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",R/N); : PRINT #Win002, "   ";
PRINT #Win002, "   -"
PRINT #Win002, "exp. rel .freq. (without correction)  ";
PRINT #Win002, using("####.###",DE0/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",HE0/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",RE0/N); : PRINT #Win002, "   ";
PRINT #Win002, "   -"
PRINT #Win002, "exp. rel. freq. (Hogben/Levene)       ";
PRINT #Win002, using("####.###",DE1/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",HE1/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",RE1/N); : PRINT #Win002, "   ";
PRINT #Win002, "   -"
PRINT #Win002, "exp. rel. freq. (Cannings & Edwards)  ";
PRINT #Win002, using("####.###",DE2/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",HE2/N); : PRINT #Win002, "   ";
PRINT #Win002, using("####.###",RE2/N); : PRINT #Win002, "   ";
PRINT #Win002, "   -"
PRINT #Win002, "---------------------------------------------------------------------------"
PRINT #Win002, ""
P = P / (2 * N) : Q = Q / (2 * N) : SEPQ1 = sqr(P * Q / (2 * N))
SEPQ2 = sqr((P + D / N - 2 * P * P) / (2 * N))
PRINT #Win002, "p = P(A) = "; : PRINT #Win002, using("###.####", P)
PRINT #Win002, "q = P(a) = "; : PRINT #Win002, using("###.####", Q)
PRINT #Win002, "H0:{d,h,r}        s.e.(p) = s.e.(q) = "; : PRINT #Win002, using("###.####", SEPQ2)
PRINT #Win002, "Ha:{p^2,2pq,q^2}  s.e.(p) = s.e.(q) = "; : PRINT #Win002, using("###.####", SEPQ1)
PRINT #Win002, ""

FOR i001 = 1 TO 511 STEP 2
  IF tests <> i001 THEN GOTO [notCH1_2]
  PRINT #Win002, "P(chi-squared test without correction)  ";
  IF PC(1) >= 10^(-4) THEN
    PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PC(1))
  ELSE
    IF PC(1) >= 10^(-5) THEN
      PRINT #Win002, " < 10^-4"
    ELSE
      IF PC(1) >= 10^(-6) THEN
        PRINT #Win002, " < 10^-5"
      ELSE
        PRINT #Win002, " < 10^-6"
      END IF
    END IF
  END IF
  [notCH1_2]
NEXT i001
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 1
    IF tests <> 2*i001 + j001 THEN GOTO [notCH2_2]
    PRINT #Win002, "P(chi-sq. test with Yates' correction)  ";
    IF PC(2) >= 10^(-4) THEN
      PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PC(2))
    ELSE
      IF PC(2) >= 10^(-5) THEN
        PRINT #Win002, " < 10^-4"
      ELSE
        IF PC(2) >= 10^(-6) THEN
          PRINT #Win002, " < 10^-5"
        ELSE
          PRINT #Win002, " < 10^-6"
        END IF
      END IF
    END IF
    [notCH2_2]
  NEXT j001
NEXT i001
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 3
    IF tests <> 4*i001 + j001 THEN GOTO [notCH3_2]
    PRINT #Win002, "P(c.s. test w/ Hogben/Levene correct.)  ";
    IF PC(3) >= 10^(-4) THEN
      PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PC(3))
    ELSE
      IF PC(3) >= 10^(-5) THEN
        PRINT #Win002, " < 10^-4"
      ELSE
        IF PC(3) >= 10^(-6) THEN
          PRINT #Win002, " < 10^-5"
        ELSE
          PRINT #Win002, " < 10^-6"
        END IF
      END IF
    END IF
    [notCH3_2]
  NEXT j001
NEXT i001
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 7
    IF tests <> 8*i001 + j001 THEN GOTO [notCH4_2]
    PRINT #Win002, "P(c.s. test w/ Cannings & Edwards corr.)";
    IF PC(4) >= 10^(-4) THEN
      PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PC(4))
    ELSE
      IF PC(4) >= 10^(-5) THEN
        PRINT #Win002, " < 10^-4"
      ELSE
        IF PC(4) >= 10^(-6) THEN
          PRINT #Win002, " < 10^-5"
        ELSE
          PRINT #Win002, " < 10^-6"
        END IF
      END IF
    END IF
    [notCH4_2]
  NEXT j001
NEXT i001
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 15
    IF tests <> 16*i001 + j001 THEN GOTO [notCH5_2]
    PRINT #Win002, "P(G or log-likelihood test without cor.)";
    IF PC(5) >= 10^(-4) THEN
      PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PC(5))
    ELSE
      IF PC(5) >= 10^(-5) THEN
        PRINT #Win002, " < 10^-4"
      ELSE
        IF PC(5) >= 10^(-6) THEN
          PRINT #Win002, " < 10^-5"
        ELSE
          PRINT #Win002, " < 10^-6"
        END IF
      END IF
    END IF
    [notCH5_2]
  NEXT j001
NEXT i001
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 31
    IF tests <> 32*i001 + j001 THEN GOTO [notCH6_2]
    PRINT #Win002, "P(log-likelih. test w/ continuity corr.)";
    IF PC(6) >= 10^(-4) THEN
      PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PC(6))
    ELSE
      IF PC(6) >= 10^(-5) THEN
        PRINT #Win002, " < 10^-4"
      ELSE
        IF PC(6) >= 10^(-6) THEN
          PRINT #Win002, " < 10^-5"
        ELSE
          PRINT #Win002, " < 10^-6"
        END IF
      END IF
    END IF
    [notCH6_2]
  NEXT j001
NEXT i001
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 63
    IF tests <> 64*i001 + j001 THEN GOTO [notCH7_2]
    IF FISHFLAG = 1 THEN
      PRINT #Win002, "P(Fisher's exact test)                   =    -"
     ELSE
      PRINT #Win002, "P(Fisher's exact test)                  ";
      IF PFISH >= 10^(-4) THEN
        PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PFISH)
      ELSE
        IF PFISH >= 10^(-5) THEN
          PRINT #Win002, " < 10^-4"
        ELSE
          IF PFISH >= 10^(-6) THEN
            PRINT #Win002, " < 10^-5"
          ELSE
            PRINT #Win002, " < 10^-6"
          END IF
        END IF
      END IF
    END IF
    [notCH7_2]
  NEXT j001
NEXT i001
FOR i001 = 1 TO 511 STEP 2
  FOR j001 = 0 TO 127
    IF tests <> 128*i001 + j001 THEN GOTO [notCH8_2]
    PRINT #Win002, "P(Haldane's exact test)                 ";
    IF PROBT >= 10^(-4) THEN
      PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PROBT)
    ELSE
      IF PROBT >= 10^(-5) THEN
        PRINT #Win002, " < 10^-4"
      ELSE
        IF PROBT >= 10^(-6) THEN
          PRINT #Win002, " < 10^-5"
        ELSE
          PRINT #Win002, " < 10^-6"
        END IF
      END IF
    END IF
    [notCH8_2]
  NEXT j001
NEXT i001

IF tests < 256 THEN GOTO [notCH9]
' Exact test (1000 bootstrap simulations)
T = 1000 : PROBT = 0
DIM OD(T), OH(T), ED(T), EH(T)
' Estimating exact probability of the sample
P = 2*D + H : Q = H + 2*R : P0 = P / (2*N) : P1 = P : Q1 = Q
ExpD = P0^2 : ExpH = 2*P0*(1-P0) : ExpR = (1-P0)^2
D1 = D : H1 = H : R1 = R
k = N :     GOSUB [FACTORIAL] : NFAC  = FACT
k = 2 * N : GOSUB [FACTORIAL] : N2FAC = FACT
CONSTFAC = NFAC - N2FAC : D1 = D : H1 = H : R1 = R : GOSUB [FACTPQDHR]
PROB2 = exp(CONSTFAC + PFAC + QFAC - DFAC - HFAC - RFAC + H1 * log(2))

PTOT = 0 : D1TOT = 0 : H1TOT = 0 : R1TOT = 0 : OD1TOT = 0 : OH1TOT = 0 : OR1TOT = 0
FOR i = 1 TO T
  R1 = 0 : D1 = 0 : H1 = 0 : OD1 = 0 : OH1 = 0 : OR1 = 0
  FOR INDIV = 1 TO N
    ' Obtaining D and H from simulation of expected frequencies (exact test and ternary plot)
    A = rnd(1)
    IF A <= ExpD THEN
      D1 = D1 + 1
     ELSE
      IF A >= ExpD + ExpH THEN
        R1 = R1 + 1
       ELSE
        H1 = H1 + 1
      END IF
    END IF

    IF A <= D/N THEN
      OD1 = OD1 + 1
     ELSE
      IF A > D/N AND A <= (D+H)/N THEN
        OH1 = OH1 + 1
       ELSE
        OR1 = OR1 + 1
      END IF
    END IF
  NEXT INDIV
  ' Comparing exact probability from simulation with the one from the sample
  P1 = 2 * D1 + H1 : Q1 = H1 + 2 * R1
  D1TOT = D1TOT + D1 : H1TOT = H1TOT + H1 : R1TOT = R1TOT + R1
  PTOT = PTOT + P1 / (2 * N)
  GOSUB [FACTPQDHR]
  PROB1 = EXP(CONSTFAC + PFAC + QFAC - DFAC - HFAC - RFAC + H1 * log(2))
  IF PROB1 <= PROB2 THEN PROBT = PROBT + 1
  OD1TOT = OD1TOT + OD1 : OH1TOT = OH1TOT + OH1 : OR1TOT = OR1TOT + OR1
  ' Saving variables to make the ternary plot
  OD(i) = OD1 : OH(i) = OH1 : ED(i) = D1 : EH(i) = H1
NEXT i

PRINT #Win002, "" : PRINT #Win002, "'EXACT' BOOTSTRAP (1000 SIMULATIONS) ESTIMATES" : PRINT #Win002, ""
PRINT #Win002, "OBS. SAMPLE p = P(A)  = (2D+H)/2N        = "; : PRINT #Win002, using("#.####", P0)
PRINT #Win002, "BOOTSTRAP EST. p                         = "; : PRINT #Win002, using("#.####", PTOT/T)
PRINT #Win002, ""
PRINT #Win002, "EXACT PROBABILITY (1000 SIMUL.)         ";
IF PROBT/T >= 10^(-4) THEN
  PRINT #Win002, " = "; : PRINT #Win002, using("#.####", PROBT/T)
ELSE
  IF PROBT/T >= 10^(-5) THEN
    PRINT #Win002, " < 10^-4"
  ELSE
    IF PROBT/T >= 10^(-6) THEN
      PRINT #Win002, " < 10^-5"
    ELSE
      PRINT #Win002, " < 10^-6"
    END IF
  END IF
END IF

DIM P(T), H88(25)
PRINT #Win002, ""
PRINT #Win002, "               normal approximation            bootstrap (1000 simul.)"
PRINT #Win002, "genotype      calc.P         95% C.I.        meanP  med.P      95% C.I."
PRINT #Win002, "-------------------------------------------------------------------------"
PRINT #Win002, "   AA       obs. "; : PRINT #Win002, using ("#.###", D/N);
TempVar = D/N - 1.96 * sqr(D/N * (1 - D/N) / N) : IF TempVar < 0 THEN TempVar = 0
PRINT #Win002, "    {"; : PRINT #Win002, using ("#.###", TempVar); : PRINT #Win002, ",";
TempVar = D/N + 1.96 * sqr(D/N * (1 - D/N) / N) : IF TempVar > 1 THEN TempVar = 1
PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, "}    ";
FOR i = 1 TO T : P(i) = OD(i)/N : NEXT i
GOSUB [SORTVALUES]
PRINT #Win002, using("###.###", OD1TOT/(T*N)); : PRINT #Win002, using("###.###", (P(500)+P(501))/2);
PRINT #Win002, "   {"; : PRINT #Win002, using("#.###", P(26)); : PRINT #Win002, ",";
PRINT #Win002, using("#.###", P(975)); : PRINT #Win002, "}"
PRINT #Win002, "            exp. "; : PRINT #Win002, using("#.###", ExpD);
TempVar = ExpD - 1.96 * sqr(4*P0^3 * (1-P0) / (2*N)) : IF TempVar < 0 THEN TempVar = 0
PRINT #Win002, "    {"; : PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, ",";
TempVar = ExpD + 1.96 * sqr(4*P0^3 * (1-P0) / (2*N)) : IF TempVar > 1 THEN TempVar = 1
PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, "}    ";
FOR i = 1 TO T : P(i) = ED(i)/N : NEXT i
GOSUB [SORTVALUES]
PRINT #Win002, using("###.###", D1TOT/(T*N)); : PRINT #Win002, using("###.###", (P(500)+P(501))/2);
PRINT #Win002, "   {"; : PRINT #Win002, using("#.###", P(26)); : PRINT #Win002, ",";
PRINT #Win002, using("#.###", P(975)); : PRINT #Win002, "}"
PRINT #Win002, "   Aa       obs. "; : PRINT #Win002, using ("#.###", H/N);
TempVar = H/N - 1.96 * sqr(H/N * (1 - H/N) / N) : IF TempVar < 0 THEN TempVar = 0
PRINT #Win002, "    {"; : PRINT #Win002, using ("#.###", TempVar); : PRINT #Win002, ",";
TempVar = H/N + 1.96 * sqr(H/N * (1 - H/N) / N) : IF TempVar > 1 THEN TempVar = 1
PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, "}    ";
FOR i = 1 TO T : P(i) = OH(i)/N : NEXT i
GOSUB [SORTVALUES]
PRINT #Win002, using("###.###", OH1TOT/(T*N)); : PRINT #Win002, using("###.###", (P(500)+P(501))/2);
PRINT #Win002, "   {"; : PRINT #Win002, using("#.###", P(26)); : PRINT #Win002, ",";
PRINT #Win002, using("#.###", P(975)); : PRINT #Win002, "}"
PRINT #Win002, "            exp. "; : PRINT #Win002, using("#.###", ExpH);
TempVar = ExpH - 1.96 * sqr(4*P0*(1-P0) * (P0 + (1-P0) - 4*P0*(1-P0)) / (2*N)) : IF TempVar < 0 THEN TempVar = 0
PRINT #Win002, "    {"; : PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, ",";
TempVar = ExpH + 1.96 * sqr(4*P0*(1-P0) * (P0 + (1-P0) - 4*P0*(1-P0)) / (2*N)) : IF TempVar > 1 THEN TempVar = 1
PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, "}    ";
FOR i = 1 TO T : P(i) = EH(i)/N : NEXT i
GOSUB [SORTVALUES]
PRINT #Win002, using("###.###", H1TOT/(T*N)); : PRINT #Win002, using("###.###", (P(500)+P(501))/2);
PRINT #Win002, "   {"; : PRINT #Win002, using("#.###", P(26)); : PRINT #Win002, ",";
PRINT #Win002, using("#.###", P(975)); : PRINT #Win002, "}"
PRINT #Win002, "   aa       obs. "; : PRINT #Win002, using ("#.###", R/N);
TempVar = R/N - 1.96 * sqr(R/N * (1 - R/N) / N) : IF TempVar < 0 THEN TempVar = 0
PRINT #Win002, "    {"; : PRINT #Win002, using ("#.###", TempVar); : PRINT #Win002, ",";
TempVar = R/N + 1.96 * sqr(R/N * (1 - R/N) / N) : IF TempVar > 1 THEN TempVar = 1
PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, "}    ";
FOR i = 1 TO T : P(i) = (N - (OD(i) + OH(i)))/N : NEXT i
GOSUB [SORTVALUES]
PRINT #Win002, using("###.###", OR1TOT/(T*N)); : PRINT #Win002, using("###.###", (P(500)+P(501))/2);
PRINT #Win002, "   {"; : PRINT #Win002, using("#.###", P(26)); : PRINT #Win002, ",";
PRINT #Win002, using("#.###", P(975)); : PRINT #Win002, "}"
PRINT #Win002, "            exp. "; : PRINT #Win002, using("#.###", ExpR);
TempVar = ExpR - 1.96 * sqr(4*(1-P0)^3 * P0 / (2*N)) : IF TempVar < 0 THEN TempVar = 0
PRINT #Win002, "    {"; : PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, ",";
TempVar = ExpR + 1.96 * sqr(4*(1-P0)^3 * P0 / (2*N)) : IF TempVar > 1 THEN TempVar = 1
PRINT #Win002, using("#.###", TempVar); : PRINT #Win002, "}    ";
FOR i = 1 TO T : P(i) = (N - (ED(i) + EH(i)))/N : NEXT i
GOSUB [SORTVALUES]
PRINT #Win002, using("###.###", R1TOT/(T*N)); : PRINT #Win002, using("###.###", (P(500)+P(501))/2);
PRINT #Win002, "   {"; : PRINT #Win002, using("#.###", P(26)); : PRINT #Win002, ",";
PRINT #Win002, using("#.###", P(975)); : PRINT #Win002, "}"
PRINT #Win002, "-------------------------------------------------------------------------"
TernaryPlot = 1
[notCH9]

IF TernaryPlot = 1 THEN GOTO [Win003]
WAIT

[end_win002]
CONFIRM "Are you sure you want to quit?"; quit$
IF quit$ = "no" THEN WAIT
Win002 = 0
CLOSE #Win002
WAIT

[Win003]
Win003 = 1
SIZE = DH * .6 : WindowWidth  = DH * .8 : WindowHeight = DH * .8
UpperLeftX = int(DW-(DH * .9)) : UpperLeftY = int(DH-(DH * .9))

MENU #Win003, "&File", "Save As...", [saveAs_win003], "Exit", [end_win003]
OPEN "Hardy Weinberg Equilibrium Test" FOR graphics_nsb_nf AS #Win003 ' "_nsb" = no scrollbars; "_nf" = window has no frame and cannot be resized by user
PRINT #Win003, "trapclose [end_win003]"

CritChisq = 3.8415 ' Critical Chi-sqared value for alpha = 0.05 (1 degree of freedom)

' Ternary plot
#Win003, "place "+str$(SIZE*.85+50)+" 50 ; down; goto "+str$(SIZE*.7+50)+" "+str$(SIZE*.3+50)
#Win003, "place "+str$(SIZE*.85+50)+" 50 ; down; goto "+str$(SIZE+50)+" "+str$(SIZE*.3+50)
#Win003, "place "+str$(SIZE*.7+50)+" "+str$(SIZE*.3+50)+" ; down; goto "+str$(SIZE+50)+" "+str$(SIZE*.3+50)
#Win003, "place "+str$(SIZE*.82+50)+" "+str$(SIZE*.18+50)+"; circle 2"
#Win003, "place "+str$(SIZE*.82+50)+" "+str$(SIZE*.19+50)+" ; down; goto "+str$(SIZE*.82+50)+" "+str$(SIZE*.3+50)
#Win003, "place "+str$(SIZE*.76+50)+" "+str$(SIZE*.18+50)+" ; down; goto "+str$(SIZE*.81+50)+" "+str$(SIZE*.18+50)
#Win003, "place "+str$(SIZE*.83+50)+" "+str$(SIZE*.18+50)+" ; down; goto "+str$(SIZE*.94+50)+" "+str$(SIZE*.18+50)
#Win003, "down; place "+str$(SIZE*.815+50)+" "+str$(SIZE*.25+50) : #Win003, "|h"
#Win003, "down; place "+str$(SIZE*.78+50)+" "+str$(SIZE*.185+50) : #Win003, "|d"
#Win003, "down; place "+str$(SIZE*.88+50)+" "+str$(SIZE*.185+50) : #Win003, "|r"
#Win003, "down; place "+str$(SIZE*.75+50)+" "+str$(SIZE*.305+50) : #Win003, "|p"
#Win003, "down; place "+str$(SIZE*.9+50) +" "+str$(SIZE*.305+50) : #Win003, "|q"

#Win003 "place "+str$(SIZE/2+50)+" 50 ; down; goto 50 "+str$(SIZE+50)
#Win003 "place "+str$(SIZE/2+50)+" 50 ; down; goto "+str$(SIZE+50)+" "+str$(SIZE+50)
#Win003 "place 50 "+str$(SIZE+50)+" ; down; goto "+str$(SIZE+50)+" "+str$(SIZE+50)

#Win003 "place 40 50 ; down; goto 40 "+str$(SIZE+50)
FOR i = 0 TO 20 : #Win003 "place 35 "+str$(SIZE*i/20+50)+" ; down; goto 40 "+str$(SIZE*i/20+50) : NEXT i
#Win003, "down; place 12 55" : #Win003, "|1.0"
#Win003, "down; place 12 "+str$(SIZE+55) : #Win003, "|0.0"
#Win003 "place 50 "+str$(SIZE+60)+" ; down; goto "+str$(SIZE+50)+" "+str$(SIZE+60)
FOR i = 0 TO 20 : #Win003 "place "+str$(SIZE*i/20+50)+" "+str$(SIZE+60)+" ; down; goto "+str$(SIZE*i/20+50)+" "+str$(SIZE+65) : NEXT i
#Win003, "down; place 42 "+str$(SIZE+80) : #Win003, "|0.0"
#Win003, "down; place "+str$(SIZE+42)+" "+str$(SIZE+80) : #Win003, "|1.0"

' Plotting parabolas
FOR i = 1 TO SIZE
  X1 = 50 + i
  pGraph = i/SIZE
  hGraph = 2*pGraph*(1-pGraph)
  Y1 = (50 + SIZE) - SIZE*hGraph
  #Win003 "set "+str$(X1)+" "+str$(Y1)+""
NEXT i
' Bottom limit
FOR i = 1 TO SIZE
  X1 = 50 + i
  pGraph = i/SIZE
  FGraph = (CritChisq/N)^(1/2)
  hGraph = 2*pGraph*(1-pGraph)*(1-FGraph)
  Y1 = (50 + SIZE) - SIZE*hGraph
  IF N > CritChisq THEN #Win003 "set "+str$(X1)+" "+str$(Y1)+""
NEXT i
' Upper limit
FOR i = 1 TO SIZE
  X1 = 50 + i
  pGraph = i/SIZE
  FGraph = 0-(CritChisq/N)^(1/2)
  hGraph = 2*pGraph*(1-pGraph)*(1-FGraph)
  Y1 = (50 + SIZE) - SIZE*hGraph
  IF  FGraph*(1-pGraph) >= 0-pGraph AND FGraph*pGraph >= pGraph-1 THEN #Win003 "set "+str$(X1)+" "+str$(Y1)+""
NEXT i

' Plotting points (expected and observed)
DIM X(2*T) , Y(2*T)
j = 0
FOR i = 1 TO T
  j = j + 1
  X(j) = 50 + SIZE*((ED(i) + EH(i)/2)/N) : Y(j) = (50+SIZE) - SIZE*(EH(i)/N)
  #Win003 "place "+str$(X(j))+" "+str$(Y(j))+"; color red; backcolor red; circlefilled 2"
  j = j + 1
  X(j) = 50 + SIZE*((OD(i) + OH(i)/2)/N) : Y(j) = (50+SIZE) - SIZE*(OH(i)/N)
  #Win003 "place "+str$(X(j))+" "+str$(Y(j))+"; color black; backcolor black; circlefilled 2"
NEXT i
XC = 50 + SIZE*((D + H/2)/N) : YC1 = (50+SIZE) - SIZE*(H/N) : YC2 = (50+SIZE) - SIZE*(ExpH)
#Win003 "set "+str$(XC)+" "+str$(YC1)+"; color black; backcolor blue; circlefilled 4"
#Win003 "set "+str$(XC)+" "+str$(YC2)+"; color black; backcolor blue; circlefilled 4"

' Plotting parabolas
FOR i = 1 TO SIZE
  X1 = 50 + i
  pGraph = i/SIZE
  hGraph = 2*pGraph*(1-pGraph)
  Y1 = (50 + SIZE) - SIZE*hGraph
  #Win003 "set "+str$(X1)+" "+str$(Y1)+""
NEXT i
' Bottom limit
FOR i = 1 TO SIZE
  X1 = 50 + i
  pGraph = i/SIZE
  FGraph = (CritChisq/N)^(1/2)
  hGraph = 2*pGraph*(1-pGraph)*(1-FGraph)
  Y1 = (50 + SIZE) - SIZE*hGraph
  IF N > CritChisq THEN #Win003 "set "+str$(X1)+" "+str$(Y1)+""
NEXT i
' Upper limit
FOR i = 1 TO SIZE
  X1 = 50 + i
  pGraph = i/SIZE
  FGraph = 0-(CritChisq/N)^(1/2)
  hGraph = 2*pGraph*(1-pGraph)*(1-FGraph)
  Y1 = (50 + SIZE) - SIZE*hGraph
  IF  FGraph*(1-pGraph) >= 0-pGraph AND FGraph*pGraph >= pGraph-1 THEN #Win003 "set "+str$(X1)+" "+str$(Y1)+""
NEXT i

PRINT #Win003, "flush"
WAIT

[saveAs_win003]
PRINT #Win003, "getbmp TernaryPlot 0 0 "+str$(SIZE+100)+" "+str$(SIZE+100)
FILEDIALOG "Save As... ", "*.bmp", savefile$
IF savefile$ = "" THEN
  NOTICE "No filename specified. File NOT saved!"
  WAIT
END IF
BMPSAVE "TernaryPlot", savefile$
NOTICE "Ternary plot saved as ";savefile$
WAIT

[end_win003]
CONFIRM "Are you sure you want to quit?"; quit$
IF quit$ = "no" THEN WAIT
Win003 = 0
CLOSE #Win003
WAIT

[Win004]
WindowWidth = 800 : WindowHeight = 600
DW = DisplayWidth : DH = DisplayHeight : WW = WindowWidth : WH = WindowHeight
UpperLeftX = int((DW-WW)/2) : UpperLeftY = int((DH-WH)/2) : BackgroundColor$ = "lightgray"
Win000 = 0 : Win004 = 1 : CLOSE #Win000

MENU #Win004, "File", "Exit", [end_win004]
GROUPBOX #Win004.GroupBox001, "Statistical Tests",                                                              WW*.1,         50, WW*.8,    50
GROUPBOX #Win004.GroupBox002, "Number of Genotyped Individuals",                                                WW*.1,        120, WW*.8, WH*.7
CHECKBOX #Win004.CheckBox001, "Chi-square without correction", [win004_cb1_on], [win004_cb1_off],               WW*.1+130,     70,   200,    20
CHECKBOX #Win004.CheckBox002, "Exact probability by simulation", [win004_cb2_on], [win004_cb2_off],             WW*.1+350,     70,   210,    20
BUTTON #Win004.Button001, "Run", [Win005], UL,                                                                  WW*.1+280, WH*.85,   120,    20
STATICTEXT #Win004.Text000, "HARDY WEINBERG EQUILIBRIUM TEST",                                                  WW/2-190,      20,   406,    30
STATICTEXT #Win004.Text001, "A", WindowWidth-565, 140, 10, 20
STATICTEXT #Win004.Text002, "B", WindowWidth-535, 140, 10, 20
STATICTEXT #Win004.Text003, "C", WindowWidth-505, 140, 10, 20
STATICTEXT #Win004.Text004, "A", WindowWidth-600, 165, 10, 20
STATICTEXT #Win004.Text005, "B", WindowWidth-600, 195, 10, 20
STATICTEXT #Win004.Text006, "C", WindowWidth-600, 225, 10, 20
TEXTBOX #Win004.TextBox001, WindowWidth-570, 160, 20, 20
TEXTBOX #Win004.TextBox002, WindowWidth-540, 160, 20, 20
TEXTBOX #Win004.TextBox003, WindowWidth-540, 190, 20, 20
TEXTBOX #Win004.TextBox004, WindowWidth-510, 160, 20, 20
TEXTBOX #Win004.TextBox005, WindowWidth-510, 190, 20, 20
TEXTBOX #Win004.TextBox006, WindowWidth-510, 220, 20, 20
IF NAll > 3 THEN
  STATICTEXT #Win004.Text007, "D", WindowWidth-475, 140, 10, 20
  STATICTEXT #Win004.Text008, "D", WindowWidth-600, 255, 10, 20
  TEXTBOX #Win004.TextBox007, WindowWidth-480, 160, 20, 20
  TEXTBOX #Win004.TextBox008, WindowWidth-480, 190, 20, 20
  TEXTBOX #Win004.TextBox009, WindowWidth-480, 220, 20, 20
  TEXTBOX #Win004.TextBox010, WindowWidth-480, 250, 20, 20
END IF
IF NAll > 4 THEN
  STATICTEXT #Win004.Text009, "E", WindowWidth-445, 140, 10, 20
  STATICTEXT #Win004.Text010, "E", WindowWidth-600, 285, 10, 20
  TEXTBOX #Win004.TextBox011, WindowWidth-450, 160, 20, 20
  TEXTBOX #Win004.TextBox012, WindowWidth-450, 190, 20, 20
  TEXTBOX #Win004.TextBox013, WindowWidth-450, 220, 20, 20
  TEXTBOX #Win004.TextBox014, WindowWidth-450, 250, 20, 20
  TEXTBOX #Win004.TextBox015, WindowWidth-450, 280, 20, 20
END IF
IF NAll > 5 THEN
  STATICTEXT #Win004.Text011, "F", WindowWidth-415, 140, 10, 20
  STATICTEXT #Win004.Text012, "F", WindowWidth-600, 315, 10, 20
  TEXTBOX #Win004.TextBox016, WindowWidth-420, 160, 20, 20
  TEXTBOX #Win004.TextBox017, WindowWidth-420, 190, 20, 20
  TEXTBOX #Win004.TextBox018, WindowWidth-420, 220, 20, 20
  TEXTBOX #Win004.TextBox019, WindowWidth-420, 250, 20, 20
  TEXTBOX #Win004.TextBox020, WindowWidth-420, 280, 20, 20
  TEXTBOX #Win004.TextBox021, WindowWidth-420, 310, 20, 20
END IF
IF NAll > 6 THEN
  STATICTEXT #Win004.Text013, "G", WindowWidth-385, 140, 10, 20
  STATICTEXT #Win004.Text014, "G", WindowWidth-600, 345, 10, 20
  TEXTBOX #Win004.TextBox022, WindowWidth-390, 160, 20, 20
  TEXTBOX #Win004.TextBox023, WindowWidth-390, 190, 20, 20
  TEXTBOX #Win004.TextBox024, WindowWidth-390, 220, 20, 20
  TEXTBOX #Win004.TextBox025, WindowWidth-390, 250, 20, 20
  TEXTBOX #Win004.TextBox026, WindowWidth-390, 280, 20, 20
  TEXTBOX #Win004.TextBox027, WindowWidth-390, 310, 20, 20
  TEXTBOX #Win004.TextBox028, WindowWidth-390, 340, 20, 20
END IF
IF NAll > 7 THEN
  STATICTEXT #Win004.Text015, "H", WindowWidth-355, 140, 10, 20
  STATICTEXT #Win004.Text016, "H", WindowWidth-600, 375, 10, 20
  TEXTBOX #Win004.TextBox029, WindowWidth-360, 160, 20, 20
  TEXTBOX #Win004.TextBox030, WindowWidth-360, 190, 20, 20
  TEXTBOX #Win004.TextBox031, WindowWidth-360, 220, 20, 20
  TEXTBOX #Win004.TextBox032, WindowWidth-360, 250, 20, 20
  TEXTBOX #Win004.TextBox033, WindowWidth-360, 280, 20, 20
  TEXTBOX #Win004.TextBox034, WindowWidth-360, 310, 20, 20
  TEXTBOX #Win004.TextBox035, WindowWidth-360, 340, 20, 20
  TEXTBOX #Win004.TextBox036, WindowWidth-360, 370, 20, 20
END IF
IF NAll > 8 THEN
  STATICTEXT #Win004.Text017, "I", WindowWidth-325, 140, 10, 20
  STATICTEXT #Win004.Text018, "I", WindowWidth-600, 405, 10, 20
  TEXTBOX #Win004.TextBox037, WindowWidth-330, 160, 20, 20
  TEXTBOX #Win004.TextBox038, WindowWidth-330, 190, 20, 20
  TEXTBOX #Win004.TextBox039, WindowWidth-330, 220, 20, 20
  TEXTBOX #Win004.TextBox040, WindowWidth-330, 250, 20, 20
  TEXTBOX #Win004.TextBox041, WindowWidth-330, 280, 20, 20
  TEXTBOX #Win004.TextBox042, WindowWidth-330, 310, 20, 20
  TEXTBOX #Win004.TextBox043, WindowWidth-330, 340, 20, 20
  TEXTBOX #Win004.TextBox044, WindowWidth-330, 370, 20, 20
  TEXTBOX #Win004.TextBox045, WindowWidth-330, 400, 20, 20
END IF
IF NAll > 9 THEN
  STATICTEXT #Win004.Text019, "J", WindowWidth-295, 140, 10, 20
  STATICTEXT #Win004.Text020, "J", WindowWidth-600, 435, 10, 20
  TEXTBOX #Win004.TextBox046, WindowWidth-300, 160, 20, 20
  TEXTBOX #Win004.TextBox047, WindowWidth-300, 190, 20, 20
  TEXTBOX #Win004.TextBox048, WindowWidth-300, 220, 20, 20
  TEXTBOX #Win004.TextBox049, WindowWidth-300, 250, 20, 20
  TEXTBOX #Win004.TextBox050, WindowWidth-300, 280, 20, 20
  TEXTBOX #Win004.TextBox051, WindowWidth-300, 310, 20, 20
  TEXTBOX #Win004.TextBox052, WindowWidth-300, 340, 20, 20
  TEXTBOX #Win004.TextBox053, WindowWidth-300, 370, 20, 20
  TEXTBOX #Win004.TextBox054, WindowWidth-300, 400, 20, 20
  TEXTBOX #Win004.TextBox055, WindowWidth-300, 430, 20, 20
END IF
IF NAll > 10 THEN
  STATICTEXT #Win004.Text021, "K", WindowWidth-265, 140, 10, 20
  STATICTEXT #Win004.Text022, "K", WindowWidth-600, 465, 10, 20
  TEXTBOX #Win004.TextBox056, WindowWidth-270, 160, 20, 20
  TEXTBOX #Win004.TextBox057, WindowWidth-270, 190, 20, 20
  TEXTBOX #Win004.TextBox058, WindowWidth-270, 220, 20, 20
  TEXTBOX #Win004.TextBox059, WindowWidth-270, 250, 20, 20
  TEXTBOX #Win004.TextBox060, WindowWidth-270, 280, 20, 20
  TEXTBOX #Win004.TextBox061, WindowWidth-270, 310, 20, 20
  TEXTBOX #Win004.TextBox062, WindowWidth-270, 340, 20, 20
  TEXTBOX #Win004.TextBox063, WindowWidth-270, 370, 20, 20
  TEXTBOX #Win004.TextBox064, WindowWidth-270, 400, 20, 20
  TEXTBOX #Win004.TextBox065, WindowWidth-270, 430, 20, 20
  TEXTBOX #Win004.TextBox066, WindowWidth-270, 460, 20, 20
END IF
IF NAll > 11 THEN
  STATICTEXT #Win004.Text023, "L", WindowWidth-235, 140, 10, 20
  STATICTEXT #Win004.Text024, "L", WindowWidth-600, 495, 10, 20
  TEXTBOX #Win004.TextBox067, WindowWidth-240, 160, 20, 20
  TEXTBOX #Win004.TextBox068, WindowWidth-240, 190, 20, 20
  TEXTBOX #Win004.TextBox069, WindowWidth-240, 220, 20, 20
  TEXTBOX #Win004.TextBox070, WindowWidth-240, 250, 20, 20
  TEXTBOX #Win004.TextBox071, WindowWidth-240, 280, 20, 20
  TEXTBOX #Win004.TextBox072, WindowWidth-240, 310, 20, 20
  TEXTBOX #Win004.TextBox073, WindowWidth-240, 340, 20, 20
  TEXTBOX #Win004.TextBox074, WindowWidth-240, 370, 20, 20
  TEXTBOX #Win004.TextBox075, WindowWidth-240, 400, 20, 20
  TEXTBOX #Win004.TextBox076, WindowWidth-240, 430, 20, 20
  TEXTBOX #Win004.TextBox077, WindowWidth-240, 460, 20, 20
  TEXTBOX #Win004.TextBox078, WindowWidth-240, 490, 20, 20
END IF

OPEN "Hardy Weinberg Equilibrium Test" FOR window_nf AS #Win004 ' "_nf" = window has no frame and cannot be resized by user
PRINT #Win004, "trapclose [end_win004]"
PRINT #Win004.Text000, "!font Arial 15"

NGenot = 0
FOR i = 1 TO NAll
  NGenot = NGenot + i
NEXT i

[win004_cb1_on]  PRINT #Win004.CheckBox001, "set"   : tests02 = 1 : WAIT
[win004_cb1_off] PRINT #Win004.CheckBox001, "set"   : WAIT
[win004_cb2_on]  PRINT #Win004.CheckBox002, "set"   : tests02 = tests02 + 2 : WAIT
[win004_cb2_off] PRINT #Win004.CheckBox002, "reset" : tests02 = tests02 - 2 : WAIT

WAIT

[end_win004]
CONFIRM "Are you sure you want to quit?"; quit$
IF quit$ = "no" THEN WAIT
IF Win005 = 1 THEN CLOSE #Win005
CLOSE #Win004
WAIT


[Win005]
TempVar = 0
FOR i = 1 TO NGenot
  IF i < 10 THEN
    TempVar$ = "#Win004.TextBox00" + str$(i)
   ELSE
    TempVar$ = "#Win004.TextBox0" + str$(i)
  END IF
  PRINT #TempVar$, "!contents? TempVar$";
  IF TempVar$ = "" THEN NOTICE "Empty fields are not allowed. Please check the inputted data." : WAIT
  FOR j = 1 TO len(TempVar$)
    TempVar2$ = MID$(TempVar$, j, 1)
    IF instr("0123456789", TempVar2$) = 0 THEN
      NOTICE "The values you just entered are invalid. Just integer numbers are allowed."
      i = NGenot + 1 : j = len(TempVar$) + 1
      TempVar = 1
    END IF
  NEXT j
NEXT i
IF TempVar = 1 THEN WAIT

DIM Genot(NAll, NAll), All(NAll), P(NAll)
k = 0
FOR i = 1 TO NAll
  FOR j = 1 TO i
    k = k + 1
    IF k < 10 THEN
      TempVar$ = "#Win004.TextBox00" + str$(k)
     ELSE
      TempVar$ = "#Win004.TextBox0" + str$(k)
    END IF
    PRINT #TempVar$, "!contents? TempVar$";
    Genot(j, i) = val(TempVar$)
  NEXT j
NEXT i

N2 = 0 : EPS = 0.0000000000000000001
DIM All(NAll), P(NAll)
FOR i = 1 TO NAll
  FOR j = 1 TO i
    N2 = N2 + Genot(j, i)
  NEXT j
NEXT i

FOR i = 1 TO NAll
  FOR j = 1 TO i
    All(i) = All(i) + Genot(j, i)
    All(j) = All(j) + Genot(j, i)
    P(i) = P(i) + Genot(j, i)/(2*N2)
    P(j) = P(j) + Genot(j, i)/(2*N2)
  NEXT j
NEXT i

FOR i = 1 TO NAll
  IF P(i) = 0 THEN NOTICE "This locus has less than " + str$(NAll) + " alleles." : WAIT
NEXT i

Win005 = 1
OPEN "Hardy-Weinberg Equilibrium Testing" FOR text AS #Win005
PRINT #Win005, "!trapclose [end_win005]"

' chi-squared test without correction
TempVar = 0
FOR i = 1 TO NAll
  FOR j = 1 TO i
    IF i =  j THEN TempVar = TempVar + (Genot(j, i) - (  P(i)*P(j)*N2))^2/(  P(i)*P(j)*N2)
    IF i <> j THEN TempVar = TempVar + (Genot(j, i) - (2*P(i)*P(j)*N2))^2/(2*P(i)*P(j)*N2)
  NEXT j
NEXT i
CH2(1) = TempVar

' Obtaining P-value
v = NAll*(NAll-1)/2
IF CH2(1) < EPS AND INT(v/2) <> v/2 THEN
  PC(1) = 1
 ELSE
  w = abs(CH2(1)) : GOSUB [CHISQDIS] : PC(1) = PCHI
END IF

PRINT #Win005, ""
PRINT #Win005, "                       HARDY-WEINBERG TESTING"
PRINT #Win005, ""
PRINT #Win005, "                       Copyright 2006-2019 by"
PRINT #Win005, "      Fernando A. Bautzer Santos, Renan B. Lemes & Paulo A. Otto"
PRINT #Win005, "            Departamento de Genetica e Biologia Evolutiva"
PRINT #Win005, "                     Universidade de Sao Paulo"
PRINT #Win005, "                         Rua do Matao, 277"
PRINT #Win005, "                   05508-090 Sao Paulo SP, Brazil"
PRINT #Win005, "                            otto@usp.br"
PRINT #Win005, ""
PRINT #Win005, "----------------------------------------------------------------------------"
PRINT #Win005, "                     genotype                         genotype"
PRINT #Win005, "               absolute frequencies             relative frequencies"
PRINT #Win005, "----------------------------------------------------------------------------"
PRINT #Win005, "            observed       expected          observed       expected"
PRINT #Win005, ""

FOR i = 1 TO NAll
  FOR j = i TO NAll
    PRINT #Win005, "    "; : PRINT #Win005, MID$("ABCDEFGHIJKLMNO", i, 1);
    PRINT #Win005, MID$("ABCDEFGHIJKLMNO", j, 1);
    PRINT #Win005, "        ";
    PRINT #Win005, using("####", Genot(i, j));
    PRINT #Win005, "         ";
    IF i = j THEN
      PRINT #Win005, using("####.###", P(i)*P(j)*N2);
     ELSE
      PRINT #Win005, using("####.###", 2*P(i)*P(j)*N2);
    END IF
    PRINT #Win005, "            ";
    PRINT #Win005, using("#.###", Genot(i, j)/N2);
    PRINT #Win005, "          ";
    IF i = j THEN
      PRINT #Win005, using("#.###", P(i)*P(j));
     ELSE
      PRINT #Win005, using("#.###", 2*P(i)*P(j));
    END IF
    PRINT #Win005, ""
  NEXT j
NEXT i
PRINT #Win005, ""
PRINT #Win005, "----------------------------------------------------------------------------"
PRINT #Win005, "    N         "; : PRINT #Win005, using("####", N2)
PRINT #Win005, "" : PRINT #Win005, ""
PRINT #Win005, "----------------------------------------------------"
PRINT #Win005, "            allele     s.e.(pi)       s.e.(pi)    "
PRINT #Win005, "          freq. (pi)  H0:{d,h,r}  H1:{p^2,2pq,q^2}"
PRINT #Win005, ""
FOR i = 1 TO NAll
  PRINT #Win005, "     "+ MID$("ABCDEFGHIJKLMNO", i, 1) + "       " + using("#.###", P(i));
  PRINT #Win005, "       " + using("#.###", sqr((P(i) + Genot(i, i)/N2 - 2*P(i)^2)/(2*N2)));
  PRINT #Win005, "          " + using("#.###", sqr(P(i)*(1-P(i))*(1+F)/(2*N2)))
NEXT i
PRINT #Win005, "----------------------------------------------------"
PRINT #Win005, "" : PRINT #Win005, ""
PRINT #Win005, "P(chi-squared test without correction)  ";
IF PC(1) >= 10^(-4) THEN
  PRINT #Win005, " = "; : PRINT #Win005, using("#.####", PC(1))
ELSE
  IF PC(1) >= 10^(-5) THEN
    PRINT #Win005, " < 10^-4"
  ELSE
    IF PC(1) >= 10^(-6) THEN
      PRINT #Win005, " < 10^-5"
    ELSE
      PRINT #Win005, " < 10^-6"
    END IF
  END IF
END IF

IF tests02 < 2 THEN GOTO [notMultiCH2]
' Exact test (1000 bootstrap simulations)
T = 1000
DIM SP(NAll), GENOTYPE(NAll, NAll), TGENOTYP(NAll, NAll)
DIM ALLELE(NAll), TALLEL(NAll), F(2*N2), Q(NAll), P(T)
GOSUB [CLEARALLVAR]
PRINT #Win005, "" : PRINT #Win005, "" : PRINT #Win005, ""
PRINT #Win005, "                normal approximation            bootstrap (1000 simul.)"
PRINT #Win005, "genotype       calc.P         95% C.I.        meanP  med.P      95% C.I."
PRINT #Win005, "--------------------------------------------------------------------------"

FOR i = 1 TO NAll
  ALLELE(i) = All(i)
  Q(i) = ALLELE(i)/(2*N2)
  FOR j = i TO NAll
    GENOTYPE(i, j) = Genot(i, j)
  NEXT j
NEXT i

FOR i = 1 TO NAll
  FOR j = i TO NAll
    PRINT #Win005, "   ";
    PRINT #Win005, MID$("ABCDEFGHIJKLMNO", i, 1);
    PRINT #Win005, MID$("ABCDEFGHIJKLMNO", j, 1);
    PRINT #Win005, "        "; : PRINT #Win005, "obs. ";
    PRINT #Win005, using("#.###", GENOTYPE(i, j)/N2); : PRINT #Win005, "    {";
    PLOW = GENOTYPE(i, j)/N2 - 1.96*sqr(GENOTYPE(i, j)/N2*(1 - GENOTYPE(i, j)/N2)/N2) : IF PLOW < 0 THEN PLOW = 0
    PUPP = GENOTYPE(i, j)/N2 + 1.96*sqr(GENOTYPE(i, j)/N2*(1 - GENOTYPE(i, j)/N2)/N2) : IF PUPP > 1 THEN PUPP = 1
    PRINT #Win005, using("#.###", PLOW); : PRINT #Win005, ",";
    PRINT #Win005, using("#.###", PUPP); : PRINT #Win005, "}    ";
    SP = 0
    FOR I99 = 1 TO T
      P(I99) = 0
      FOR INDIV = 1 TO N2
        A = rnd(1)
        IF A <= GENOTYPE(i, j)/N2 THEN P(I99) = P(I99) + 1/N2
      NEXT INDIV
      SP = SP + P(I99)
    NEXT I99
    GOSUB [SORTVALUES]
    PRINT #Win005, using("###.###", SP/T);
    PRINT #Win005, using("###.###", (P(T/2)+P(T/2 + 1))/2); : PRINT #Win005, "   {";
    PRINT #Win005, using("#.###", P(T*0.025 + 1)); : PRINT #Win005, ",";
    PRINT #Win005, using("#.###", P(T*0.975)); : PRINT #Win005, "}"
    IF i = j THEN
      EXGE = Q(i)*Q(j)
      SEEX = sqr(4*Q(i)^3*(1 - Q(i))/(2*N2))
     ELSE
      EXGE = 2*Q(i)*Q(j)
      SEEX = sqr(4*Q(i)*Q(j)*(Q(i)+Q(j) - 4*Q(i)*Q(j))/(2*N2))
    END IF
    PLOW = EXGE - 1.96 * SEEX : IF PLOW < 0 THEN PLOW = 0
    PUPP = EXGE + 1.96 * SEEX : IF PLOW > 1 THEN PLOW = 1
    PRINT #Win005, "             exp. ";
    PRINT #Win005, using("#.###", EXGE); : PRINT #Win005, "    "; : PRINT #Win005, "{";
    PRINT #Win005, using("#.###", PLOW); : PRINT #Win005, ",";
    PRINT #Win005, using("#.###", PUPP); : PRINT #Win005, "}    ";
    SP = 0
    FOR I99 = 1 TO T
      QI = 0 : QJ = 0 : P(I99) = 0
      FOR INDIV = 1 TO N2
        B = rnd(1)
        IF B <= Q(i) THEN QI = QI + 1
        IF B > Q(i) AND B <= Q(i) + Q(j) THEN QJ = QJ + 1
        C = rnd(1)
        IF C <= Q(i) THEN QI = QI + 1
        IF C > Q(i) AND C <= Q(i) + Q(j) THEN QJ = QJ + 1
      NEXT INDIV
      QI = QI/(2*N2) : QJ = QJ/(2*N2)
      IF i = j THEN P(I99) = QI^2 ELSE P(I99) = 2*QI*QJ
      SP = SP + P(I99)
    NEXT I99
    GOSUB [SORTVALUES]
    PRINT #Win005, using("###.###", SP/T);
    PRINT #Win005, using("###.###", (P(T/2)+P(T/2 + 1))/2); : PRINT #Win005, "   {";
    PRINT #Win005, using("#.###", P(T*0.025 + 1)); : PRINT #Win005, ",";
    PRINT #Win005, using("#.###", P(T*0.975)); : PRINT #Win005, "}"
  NEXT j
NEXT i
PRINT #Win005, "--------------------------------------------------------------------------"
PRINT #Win005, "" : PRINT #Win005, ""
PRINT #Win005, "EXACT PROBABILITY (1000 SIMUL.)         ";

GOSUB [SIMULATION]
exactSim = PROBT/T

IF exactSim >= 10^(-4) THEN
  PRINT #Win005, " = "; : PRINT #Win005, using("#.####", exactSim)
ELSE
  IF exactSim >= 10^(-5) THEN
    PRINT #Win005, " < 10^-4"
  ELSE
    IF exactSim >= 10^(-6) THEN
      PRINT #Win005, " < 10^-5"
    ELSE
      PRINT #Win005, " < 10^-6"
    END IF
  END IF
END IF
[notMultiCH2]
WAIT

[end_win005]
CONFIRM "Are you sure you want to quit?"; quit$
IF quit$ = "no" THEN WAIT
Win005 = 0
CLOSE #Win005
WAIT

' SUBROUTINES

[CHISQDIS]
  R9 = 1: FOR I9 = v TO 2 STEP -2: R9 = R9 * I9: NEXT I9
  K9 = w ^ (INT((v + 1) / 2)) / EXP(w / 2) / R9
  IF INT(v / 2) = v / 2 THEN 2400
  J9 = SQR(2 / w / 3.141592653599)
  GOTO 2500
2400 J9 = 1
2500 L9 = 1: M9 = 1
2700 v = v + 2: M9 = M9 * w / v
  IF M9 < .0000001 THEN 3300
  L9 = L9 + M9: GOTO 2700
3300
PCHI = 1 - J9 * K9 * L9
RETURN

[FACTORIAL]
FACT = 0
FOR j = 1 TO k
  FACT = FACT + log(j)
NEXT j
RETURN

[FACTRL]
P99 = 1
FOR I6 = 1 TO I99
  P99 = P99 * (G + I6 - I99) / (F + I6)
NEXT I6
FOR I6 = I99 + 1 TO E
  P99 = P99 * (1 - G / (F + I6)) / (1 - I99 / I6)
NEXT I6
RETURN

[FACTPQDHR]
k = P1: GOSUB [FACTORIAL] : PFAC = FACT
k = Q1: GOSUB [FACTORIAL] : QFAC = FACT
[FACTOFDHR]
k = D1: GOSUB [FACTORIAL] : DFAC = FACT
k = H1: GOSUB [FACTORIAL] : HFAC = FACT
k = R1: GOSUB [FACTORIAL] : RFAC = FACT
RETURN

[SORTVALUES]
D88 = 10: K88 = 1: L88 = 1: R88 = T
[560] ' EXCHANGE SORT IF BLOCKSIZE <= D88
    IF R88 - L88 + 1 > D88 THEN [590]
    GOSUB [900]: GOTO [780]
[590] I88 = L88: J88 = R88: W88 = rnd(1) * (R88 - L88) + .5
    W88 = int(W88 + L88): F88 = P(W88)
    ' PARTITION PHASE
[620] IF P(I88) >= F88 THEN [640]
    I88 = I88 + 1:  GOTO [620]
[640] IF P(J88) <= F88 THEN [660]
    J88 = J88 - 1:  GOTO [640]
[660] IF I88 > J88 THEN [680]
    W88 = P(I88): P(I88) = P(J88): P(J88) = W88: I88 = I88 + 1: J88 = J88 - 1
[680] IF I88 <= J88 THEN [620]
    ' BOOKKEEPING PHASE
    IF J88 - L88 >= R88 - I88 THEN [740]
    IF I88 >= R88 THEN [730]
    H88(K88) = I88: K88 = K88 + 1: H88(K88) = R88: K88 = K88 + 1
[730] R88 = J88:  GOTO [770]
[740] IF L88 >= J88 THEN [760]
    H88(K88) = L88: K88 = K88 + 1: H88(K88) = J88: K88 = K88 + 1
[760] L88 = I88
[770] IF L88 < R88 THEN [590]
[780] IF K88 <= 1 THEN [800]
    K88 = K88 - 1: R88 = H88(K88): K88 = K88 - 1: L88 = H88(K88): GOTO [560]
[800] RETURN
[900] ' EXCHANGE SORT
    FOR I88 = L88 TO R88 - 1: K1 = I88
    FOR J88 = I88 + 1 TO R88: IF P(J88) >= P(K1) THEN [940]
    K1 = J88
[940] NEXT J88
    IF K1 = I88 THEN [970]
    W88 = P(I88): P(I88) = P(K1): P(K1) = W88
[970] NEXT I88
RETURN

[SIMULATION]
FOR i = 1 TO 2 * N2 : F(i) = F(i - 1) + log(i) : NEXT i
NFAC = F(N2) : N2FAC = F(2 * N2) : CONSTFAC = NFAC - N2FAC
GOSUB [EXACTPROBCALC] : PROB2 = EXPROB
FOR i = 1 TO NAll : SSP = SSP + Q(i): SP(i) = SP(i) + SSP: NEXT i
FOR i = 1 TO T
  GOSUB [CLEARALLVAR]
  FOR INDIV = 1 TO N2
    A = rnd(1): B = rnd(1)
    FOR I88 = 1 TO NAll
      IF A > SP(I88 - 1) AND A <= SP(I88) THEN
        AI88 = I88 : ALLELE(I88) = ALLELE(I88) + 1
        TALLEL(I88) = TALLEL(I88) + 1
      END IF
      IF B > SP(I88 - 1) AND B <= SP(I88) THEN
        BI88 = I88 : ALLELE(I88) = ALLELE(I88) + 1
        TALLEL(I88) = TALLEL(I88) + 1
      END IF
    NEXT I88
    IF AI88 > BI88 THEN AI88TEMP = AI88 : AI88 = BI88 : BI88 = AI88TEMP
    GENOTYPE(AI88, BI88) = GENOTYPE(AI88, BI88) + 1
    TGENOTYP(AI88, BI88) = TGENOTYP(AI88, BI88) + 1
  NEXT INDIV
  GOSUB [EXACTPROBCALC] : PROB1 = EXPROB
  IF PROB1 <= PROB2 THEN PROBT = PROBT + 1
NEXT i
RETURN

[CLEARALLVAR]
HETLOG = 0 : ALLELFAC = 0 : GENOTFAC = 0
FOR I66 = 1 TO NAll
  ALLELE(I66) = 0
  FOR J66 = I66 TO NAll
    GENOTYPE(I66, J66) = 0
  NEXT J66
NEXT I66
RETURN

[EXACTPROBCALC]
GOSUB [FACTALLEL] : GOSUB [FACTGENOT]
FOR I9 = 1 TO NAll - 1
  FOR J9 = I9 + 1 TO NAll
    IF I9 <> J9 THEN HETLOG = HETLOG + GENOTYPE(I9, J9) * log(2)
  NEXT J9
NEXT I9
EXPROB = EXP(CONSTFAC + ALLELFAC - GENOTFAC + HETLOG)
RETURN

[FACTALLEL]
FOR I9 = 1 TO NAll
  FACT = F(ALLELE(I9)): ALLELFAC = ALLELFAC + FACT
NEXT I9
RETURN

[FACTGENOT]
FOR I9 = 1 TO NAll
  FOR J9 = I9 TO NAll
    FACT = F(GENOTYPE(I9, J9)) : GENOTFAC = GENOTFAC + FACT
  NEXT J9
NEXT I9
RETURN
