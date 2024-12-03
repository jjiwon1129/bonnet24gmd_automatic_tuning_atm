# this script has functions that are called to load the PPEs

import numpy as np
import os
from os.path import exists


def read_ICONPPE(filenames_,nsimu,noutput,startfile,endfile,years):

    results_=np.zeros((nsimu,noutput))
    isimu=0
    nzero=0
    i=0
    paramfile = open('ParamSamplesForICON/'+filenames_[1], 'r')
    
    for line in paramfile:
        #print(line)
        dirr='./../C-Postprocessing_PaperExample/tables/ALL_PPES_IN_PAPER'# '/work/bd1179/b309216/icon/FolderForSimlinkInScratch/model/scripts/postprocessing/Quickplots'
        file="table_"+str(years)+startfile+"_nrun_"+str(isimu)+endfile
        File_object = os.path.abspath(os.path.join(dirr,file))
        if exists(File_object):
            content=open(File_object).readlines()
            rsnttrue=0
            rlnttrue=0
            clttrue=0
            prwtrue=0
            ind=0
            for line in content[467:]:
                User_Inputs = line.split(' ')
                for inn in User_Inputs:
                    if len(inn)>1 :
                        ind+=1
                        if inn=='rsnt':
                            rsnttrue=1
                            var=inn
                        if ind==3 and rsnttrue==1:
                            #print(var,inn)
                            results_[isimu,0]=inn

                        if inn=='rlnt':
                            rlnttrue=1
                            var=inn
                        if ind==3 and rlnttrue==1:
                            #print(var,inn)
                            results_[isimu,1]=inn

                        if inn=='clt':
                            clttrue=1
                            var=inn
                        if ind==3 and clttrue==1:
                            #print(var,inn)
                            results_[isimu,3]=inn    

                        if inn=='prw':
                            prwtrue=1
                            var=inn
                        if ind==3 and prwtrue==1:
                            #print(var,inn)
                            results_[isimu,4]=inn    
                rsnttrue=0
                rlnttrue=0
                clttrue=0
                prwtrue=0
                ind=0   
        else:
            print('warning ', File_object,' does not exist')
            nzero+=1
        #print(isimu)

        results_[isimu,2]=results_[isimu,0]+results_[isimu,1]

        isimu+=1
    return results_


def read_ICONPPE_2ndtuningstep(filenames_,nsimu,noutput2ndtuningstep,endfile,years):

    results_=np.zeros((nsimu,noutput2ndtuningstep))
    isimu=0
    nzero=0
    i=0
    paramfile = open('ParamSamplesForICON/'+filenames_[1], 'r')
    #print("table_"+str(years)+startfile+"_nrun_0"+endfile) #to delete

    for line in paramfile:
        #print(line)
        dirr='../C-Postprocessing_PaperExample/tables/ALL_PPES_IN_PAPER'# '/work/bd1179/b309216/icon/FolderForSimlinkInScratch/model/scripts/postprocessing/Quickplots'
        file="table_"+str(years)+"_nrun_"+str(isimu)+endfile
        File_object = os.path.abspath(os.path.join(dirr,file))
        if exists(File_object):
            content=open(File_object).readlines()
            rsnttrue=0
            rlnttrue=0
            clttrue=0
            prwtrue=0
            ind=0
            for line in content[467:]:
                User_Inputs = line.split(' ')
                for inn in User_Inputs:
                    if len(inn)>1 :
                        ind+=1
                        if inn=='psl':
                            rsnttrue=1
                            var=inn
                        if ind==3 and rsnttrue==1:
                            #print(var,inn)
                            results_[isimu,0]=inn

                        if inn=='tauu':
                            rlnttrue=1
                            var=inn
                        if ind==3 and rlnttrue==1:
                            #print(var,inn)
                            results_[isimu,1]=inn
                rsnttrue=0
                rlnttrue=0
                clttrue=0
                prwtrue=0
                ind=0   
        else:
            print('warning ', File_object,' does not exist')
            nzero+=1
        #print(isimu)

        isimu+=1
    return results_


def read_ICONPPE_2ndTunStep_tauu(filenames_,nsimu,noutput2ndtuningstep,endfile,years):

    results_=np.zeros((nsimu,noutput2ndtuningstep))
    isimu=0
    nzero=0
    i=0
    paramfile = open('ParamSamplesForICON/'+filenames_[1], 'r')
    #print("table_"+str(years)+startfile+"_nrun_0"+endfile) #to delete

    for line in paramfile:
        #print(line)
        dirr='../C-Postprocessing_PaperExample/tables/ALL_PPES_IN_PAPER'# /work/bd1179/b309216/icon/FolderForSimlinkInScratch/model/scripts/postprocessing/Quickplots'
        file="table_"+str(years)+"_nrun_"+str(isimu)+endfile
        File_object = os.path.abspath(os.path.join(dirr,file))
        if exists(File_object):
            content=open(File_object).readlines()
            rsnttrue=0
            rlnttrue=0
            clttrue=0
            prwtrue=0
            ind=0
            for line in content[467:]:
                User_Inputs = line.split(' ')
                for inn in User_Inputs:
                    if len(inn)>1 :
                        ind+=1
                        if inn=='tauu':
                            rsnttrue=1
                            var=inn
                        if ind==2 and rsnttrue==1:
                            #print(var,inn)
                            results_[isimu,0]=inn
                rsnttrue=0
                rlnttrue=0
                clttrue=0
                prwtrue=0
                ind=0   
        else:
            print('warning ', File_object,' does not exist')
            nzero+=1
        #print(isimu)

        isimu+=1
    return results_


def read_ICONPPE_2ndTunStep_ua(filenames_,nsimu,noutput2ndtuningstep,endfile,years):

    results_=np.zeros((nsimu,noutput2ndtuningstep))
    isimu=0
    nzero=0
    i=0
    paramfile = open('ParamSamplesForICON/'+filenames_[1], 'r')
    #print("table_"+str(years)+startfile+"_nrun_0"+endfile) #to delete

    for line in paramfile:
        #print(line)
        dirr='../C-Postprocessing_PaperExample/tables/ALL_PPES_IN_PAPER' #/work/bd1179/b309216/icon/FolderForSimlinkInScratch/model/scripts/postprocessing/Quickplots'
        file="table_"+str(years)+"_nrun_"+str(isimu)+endfile
        File_object = os.path.abspath(os.path.join(dirr,file))
        if exists(File_object):
            content=open(File_object).readlines()
            rsnttrue=0
            rlnttrue=0
            clttrue=0
            prwtrue=0
            ind=0
            for line in content[467:]:
                User_Inputs = line.split(' ')
                for inn in User_Inputs:
                    if len(inn)>1 :
                        ind+=1
                        if inn=='ua':
                            rsnttrue=1
                            var=inn
                        if ind==2 and rsnttrue==1:
                            #print(var,inn)
                            results_[isimu,0]=inn
                rsnttrue=0
                rlnttrue=0
                clttrue=0
                prwtrue=0
                ind=0   
        else:
            print('warning ', File_object,' does not exist')
            nzero+=1
        #print(isimu)

        isimu+=1
    return results_


def read_parametersICONPPE_2ndtuningstep(filenames,nsimu,nparam2ndtuningstep):
    #load the parameter values from the .txt files
    i=0

    var_=np.zeros((nsimu,nparam2ndtuningstep)) 

    ipara=0
    for filename in filenames:
        file = open('ParamSamplesForICON/'+filename, 'r')
        isimu=0
        for line in file:
            var_[isimu,ipara]=float(line)
            isimu+=1
        #print(var[:,ipara])
        ipara+=1
    return var_


#function for reading phy and dyn outputs
def results_phydyn(fn,nsimu,yrs,ef,ef_NAO,ef_SOO,ef_60N_1000hPa,ef_60S_1000hPa,ef_60N_10hPa,ef_60S_10hPa):    
    noutput_phy=5
    noutput_dyn=2
    #PhyDyn parameters, New Param, Test Max bounds
    resultsPhy_PhyDyn=read_ICONPPE(fn,nsimu,noutput_phy,"",ef,yrs)
    resultsDyn_PhyDyn=read_ICONPPE_2ndtuningstep(fn,nsimu,noutput_dyn,ef,yrs) #psl and tauu global
    resultsPhyDyn_NAO=read_ICONPPE_2ndTunStep_tauu(fn,nsimu,noutput_dyn,ef_NAO,yrs) #psl and tauu local
    resultsPhyDyn_SOO=read_ICONPPE_2ndTunStep_tauu(fn,nsimu,noutput_dyn,ef_SOO,yrs) #psl and tauu local
    noutput_ua=1
    resultsPhyDyn_60N_1000hPa=read_ICONPPE_2ndTunStep_ua(fn,nsimu,noutput_ua,ef_60N_1000hPa,yrs)
    resultsPhyDyn_60S_1000hPa= read_ICONPPE_2ndTunStep_ua(fn,nsimu,noutput_ua,ef_60S_1000hPa,yrs)
    resultsPhyDyn_60N_10hPa=   read_ICONPPE_2ndTunStep_ua(fn,nsimu,noutput_ua,ef_60N_10hPa,yrs)
    resultsPhyDyn_60S_10hPa=   read_ICONPPE_2ndTunStep_ua(fn,nsimu,noutput_ua,ef_60S_10hPa,yrs)

    pressure_addi=1000
    pressure_fact=100
    tauufact=1000
    #concatenate results for the 2nd tuning step, PhyDyn
    resultPhyDyn_psl_glo=np.zeros((len(resultsDyn_PhyDyn[:,0]),1))
    resultPhyDyn_psl_glo[:,0]=(resultsDyn_PhyDyn[:,0]+pressure_addi)*pressure_fact
    resultPhyDyn_tauu_NAO=np.zeros((len(resultsPhyDyn_NAO[:,0]),1))
    resultPhyDyn_tauu_NAO[:,0]=resultsPhyDyn_NAO[:,0]/tauufact
    resultPhyDyn_tauu_SOO=np.zeros((len(resultsPhyDyn_SOO[:,0]),1))
    resultPhyDyn_tauu_SOO[:,0]=resultsPhyDyn_SOO[:,0]/tauufact

    resultsPhyDyn=np.concatenate((resultsPhy_PhyDyn, resultPhyDyn_psl_glo,resultPhyDyn_tauu_NAO, resultPhyDyn_tauu_SOO\
                                    ,resultsPhyDyn_60N_1000hPa,resultsPhyDyn_60S_1000hPa, resultsPhyDyn_60N_10hPa, resultsPhyDyn_60S_10hPa),axis=1)
    return resultsPhyDyn


#function for reading phy and dyn outputs
def results_phydyn_NewParam_2tun():
    nsimu=50
    yrs="1979-1990"
    PPE='2ndtuningstepsample_PhyDynParam_NewParam_'
    samplesh=PPE+'Epen_R0top_Cvtfall_Crs_Csatsc_Cd_G_sTI_Gpicmea_Gstd'
    fn=[samplesh+'-Epen.txt',samplesh+'-R0top.txt',samplesh+'-Cvtfall.txt',samplesh+'-Crs.txt',samplesh+'-Csatsc.txt',\
                                   samplesh+'-Cd.txt',samplesh+'-G.txt',samplesh+'-sTI.txt',samplesh+'-Gpicmea.txt',samplesh+'-Gstd.txt']
    PPE2='2ndtuningstep_PhyDynParam_NewParam_'
    ef = "-"+PPE2+"fldmean_ANN.ps"
    ef_NAO = "-"+PPE2+"NAO_fldmean_ANN.ps"
    ef_SOO = "-"+PPE2+"SOO_fldmean_ANN.ps"
    ef_60N_1000hPa = "-"+PPE2+"60N_1000hPa_fldmean_ANN.ps"
    ef_60S_1000hPa = "-"+PPE2+"60S_1000hPa_fldmean_ANN.ps"
    ef_60N_10hPa = "-"+PPE2+"60N_10hPa_fldmean_ANN.ps"
    ef_60S_10hPa = "-"+PPE2+"60S_10hPa_fldmean_ANN.ps"
    
    resultsPhyDyn=results_phydyn(fn,nsimu,yrs,ef,ef_NAO,ef_SOO,ef_60N_1000hPa,ef_60S_1000hPa,ef_60N_10hPa,ef_60S_10hPa)
    varPhyDyn_NewParam_2tun=read_parametersICONPPE_2ndtuningstep(fn,nsimu,nparamPhyDyn_NewParam_2ndTun)
    return varPhyDyn_NewParam_2tun,resultsPhyDyn

#function for reading phy and dyn outputs
def results_phydyn_5thPPE_2ndTuningStep():    
    
    nsimu=30
    yrs="1979-1990"
    PPE='2ndtuningstepsample_PhyDynParam_5thPPE_'
    samplesh=PPE+'Epen_R0top_Cvtfall_Crs_Csatsc_Cd_G_sTI_Gpicmea_Gstd'
    fn=[samplesh+'-Epen.txt',samplesh+'-R0top.txt',samplesh+'-Cvtfall.txt',samplesh+'-Crs.txt',samplesh+'-Csatsc.txt',\
                                   samplesh+'-Cd.txt',samplesh+'-G.txt',samplesh+'-sTI.txt',samplesh+'-Gpicmea.txt',samplesh+'-Gstd.txt']
    
    PPE2='2ndtuningstep_PhyDynParam_5thPPE_'
    ef = "-"+PPE2+"fldmean_ANN.ps"
    ef_NAO = "-"+PPE2+"NAO_fldmean_ANN.ps"
    ef_SOO = "-"+PPE2+"SOO_fldmean_ANN.ps"
    ef_60N_1000hPa = "-"+PPE2+"60N_1000hPa_fldmean_ANN.ps"
    ef_60S_1000hPa = "-"+PPE2+"60S_1000hPa_fldmean_ANN.ps"
    ef_60N_10hPa = "-"+PPE2+"60N_10hPa_fldmean_ANN.ps"
    ef_60S_10hPa = "-"+PPE2+"60S_10hPa_fldmean_ANN.ps"
    

    resultsPhyDyn=results_phydyn(fn,nsimu,yrs,ef,ef_NAO,ef_SOO,ef_60N_1000hPa,ef_60S_1000hPa,ef_60N_10hPa,ef_60S_10hPa)
    
    varPhyDyn_NewParam_5thPPE=read_parametersICONPPE_2ndtuningstep(fn,nsimu,nparamPhyDyn_NewParam_2ndTun)
    return varPhyDyn_NewParam_5thPPE,resultsPhyDyn


def IniDef():
    nparam=6
    noutput=4+1
    nparam2ndtuningstep=3
    startfile='_'
    return nparam,noutput,nparam2ndtuningstep,startfile

def IniDef_PhyDyn():
    nparamPhyDyn2ndTun=7
    nparamPhyDyn_NewParam_2ndTun=10
    return nparamPhyDyn2ndTun,nparamPhyDyn_NewParam_2ndTun

#1st PPE, 1st tuning step
def Definitions():
    samplesh='sample_Emid_Epen_Edd_Taumf_Pr_R0top'
    filenames=[samplesh+'-Emid.txt',samplesh+'-Epen.txt',samplesh+'-Edd.txt',samplesh+'-Taumf.txt', samplesh+'-Pr.txt', samplesh+'-R0top.txt']
    nsimu=30
    endfile = "-LHCsampling_fldmean_ANN.ps"
    return filenames,nsimu,endfile, "1979-1981"

#2nd PPE, 1st tuning step
def Definitions2():
    samplesh='2ndsample_Emid_Epen_Edd_Taumf_Pr_R0top'
    filenames2ndPPE=[samplesh+'-Emid.txt',samplesh+'-Epen.txt',samplesh+'-Edd.txt',samplesh+'-Taumf.txt', samplesh+'-Pr.txt', samplesh+'-R0top.txt']
    nsimu2=29
    endfile2 = "-2ndLHCsampling_fldmean_ANN.ps"
    return filenames2ndPPE,nsimu2,endfile2, "1979-1981"

##More Cloud Param
def iniDefMorecloudparam():
    nparamMoreCloudParam=7
    startfileMoreCloudParam="_MoreCloudParam" 
    return nparamMoreCloudParam, startfileMoreCloudParam

#PPE, MoreCloudParam
def Definitions_Morecloudparam():
    nsimuMoreCloudParam=30
    endfileMoreCloudParam = "-LHCsampling_fldmean_ANN.ps"
    samplesh='MoreCloudParamsample_Cmfctop_Cprcon_Ccsaut_Csecfrl_Cvtfall_Pr_R0top'
    filenamesMoreCloudParam=[samplesh+'-Cmfctop.txt',samplesh+'-Cprcon.txt',samplesh+'-Ccsaut.txt',samplesh+'-Csecfrl.txt',samplesh+'-Cvtfall.txt', samplesh+'-Pr.txt',samplesh+'-R0top.txt']
    return nsimuMoreCloudParam, endfileMoreCloudParam, filenamesMoreCloudParam, "1979-1981"

#PPE, MoreCloudParam2
def Definitions_Morecloudparam2():
    nsimuMoreCloudParam2=30
    #nparamMoreCloudParam2=7 use nparamMoreCloudParam
    #startfileMoreCloudParam2="_MoreCloudParam_" use startfileMoreCloudParam 
    endfileMoreCloudParam2 = "-2ndMoreCloudParam_fldmean_ANN.ps"
    #table_1979-1981_MoreCloudParam_nrun_3-2ndMoreCloudParam_fldmean_ANN.ps
    samplesh='2ndMoreCloudParamsample_Cmfctop_Cprcon_Ccsaut_Csecfrl_Cvtfall_Pr_R0top'
    filenamesMoreCloudParam2=[samplesh+'-Cmfctop.txt',samplesh+'-Cprcon.txt',samplesh+'-Ccsaut.txt', samplesh+'-Csecfrl.txt', samplesh+'-Cvtfall.txt', samplesh+'-Pr.txt',samplesh+'-R0top.txt']
    return nsimuMoreCloudParam2, endfileMoreCloudParam2, filenamesMoreCloudParam2, "1979-1981"


def read_parametersICONPPE(filenames,nsimu,nparam):
    #load the parameter values from the .txt files
    i=0

    var_=np.zeros((nsimu,nparam)) 

    ipara=0
    for filename in filenames:
        file = open('ParamSamplesForICON/'+filename, 'r')
        isimu=0
        for line in file:
            var_[isimu,ipara]=float(line)
            isimu+=1
        #print(var[:,ipara])
        ipara+=1
    return var_

#LHC PPEs
nparam,noutput,nparam2ndtuningstep,startfile=IniDef()
nparamPhyDyn2ndTun,nparamPhyDyn_NewParam_2ndTun=IniDef_PhyDyn()

def load_all_ppes(): 

    #1st tuning step
    #1st PPE Paper: PPE1
    filenames,nsimu,endfile,yrs=Definitions()
    var1stPPE=read_parametersICONPPE(filenames,nsimu,nparam)
    startfile=""
    results1stPPE=read_ICONPPE(filenames,nsimu,noutput, startfile,endfile,yrs)

    #2nd PPE: PPE2
    filenames2ndPPE,nsimu2,endfile2,yrs2=Definitions2()
    var2ndPPE=read_parametersICONPPE(filenames2ndPPE,nsimu2,nparam)
    results2ndPPE=read_ICONPPE(filenames2ndPPE,nsimu2,noutput,startfile,endfile2,yrs2)

    nparamMoreCloudParam, startfileMoreCloudParam=iniDefMorecloudparam()

    # PPE MoreCloudParam: PPE3
    nsimuMoreCloudParam, endfileMoreCloudParam, filenamesMoreCloudParam,yrsM=Definitions_Morecloudparam()
    varMoreCloudParam=read_parametersICONPPE(filenamesMoreCloudParam,nsimuMoreCloudParam,nparamMoreCloudParam)
    resultsMoreCloudParam=read_ICONPPE(filenamesMoreCloudParam,nsimuMoreCloudParam,noutput,startfileMoreCloudParam,endfileMoreCloudParam,yrsM)

    # PPE MoreCloudParam 2: PPE4
    nsimuMoreCloudParam2, endfileMoreCloudParam2, filenamesMoreCloudParam2,yrsM2= Definitions_Morecloudparam2()
    varMoreCloudParam2=read_parametersICONPPE(filenamesMoreCloudParam2,nsimuMoreCloudParam2,nparamMoreCloudParam)
    resultsMoreCloudParam2=read_ICONPPE(filenamesMoreCloudParam2,nsimuMoreCloudParam2,noutput,startfileMoreCloudParam,endfileMoreCloudParam2,yrsM2)

    #2nd tuning step: PPE5 
    varPhyDyn_NewParam_2tun,resultsPhyDyn_NewParam_2tun=results_phydyn_NewParam_2tun()
    varPhyDyn_NewParam_5thPPE_2tun,results_5thPPE_2tun=results_phydyn_5thPPE_2ndTuningStep()
    return var1stPPE, results1stPPE,var2ndPPE, results2ndPPE, varMoreCloudParam, resultsMoreCloudParam,\
     varMoreCloudParam2, resultsMoreCloudParam2, varPhyDyn_NewParam_2tun,resultsPhyDyn_NewParam_2tun,\
      varPhyDyn_NewParam_5thPPE_2tun,results_5thPPE_2tun


def read_ICONPPE_add_2dvar(filenames_,nsimu,noutput,startfile,endfile,years):
    noutput=7
    results_=np.zeros((nsimu,noutput))
    isimu=0
    nzero=0
    i=0
    paramfile = open('ParamSamplesForICON/'+filenames_[1], 'r')
    
    for line in paramfile:
        #print(line)
        dirr='./../C-Postprocessing_PaperExample/tables/ALL_PPES_IN_PAPER'# '/work/bd1179/b309216/icon/FolderForSimlinkInScratch/model/scripts/postprocessing/Quickplots'
        file="table_"+str(years)+startfile+"_nrun_"+str(isimu)+endfile
        File_object = os.path.abspath(os.path.join(dirr,file))
        if exists(File_object):
            content=open(File_object).readlines()
            prtrue=0
            tstrue=0
            clivitrue=0
            psltrue=0
            ind=0
            for line in content[0:]:
                User_Inputs = line.split(' ')
                for inn in User_Inputs:
                    if len(inn)>1 :
                        ind+=1
                        if inn=='pr':
                            prtrue=1
                            var=inn
                        if ind==3 and prtrue==1:
                            results_[isimu,0]=inn

                        if inn=='ts':
                            tstrue=1
                            var=inn
                        if ind==3 and tstrue==1:
                            results_[isimu,1]=inn

                        if inn=='psl':
                            psltrue=1
                            var=inn
                        if ind==3 and psltrue==1:
                            results_[isimu,2]=inn   

                        if inn=='clivi':
                            clivitrue=1
                            var=inn
                        if ind==3 and clivitrue==1:
                            results_[isimu,3]=inn    

                        if inn=='cllvi':
                            cllvitrue=1
                            var=inn
                        if ind==3 and cllvitrue==1:
                            results_[isimu,4]=inn  
                            
                        if inn=='hfss':
                            hfsstrue=1
                            var=inn
                        if ind==3 and hfsstrue==1:
                            results_[isimu,5]=inn   
                            
                        if inn=='hfls':
                            hflstrue=1
                            var=inn
                        if ind==3 and hflstrue==1:
                            results_[isimu,6]=inn    
 
                prtrue=0
                tstrue=0
                psltrue=0
                clivitrue=0
                cllvitrue=0
                hfsstrue=0
                hflstrue=0
                ind=0   
        else:
            print('warning ', File_object,' does not exist')
            nzero+=1
        isimu+=1
    return results_


def results_phydyn_NewParam_2tun_add_2dvar():
    nsimu=50
    noutput=4
    clivi_fact=1e-3#1000
    pressure_addi=1000
    pressure_fact=100
    yrs="1979-1990"
    PPE='2ndtuningstepsample_PhyDynParam_NewParam_'
    samplesh=PPE+'Epen_R0top_Cvtfall_Crs_Csatsc_Cd_G_sTI_Gpicmea_Gstd'
    fn=[samplesh+'-Epen.txt',samplesh+'-R0top.txt',samplesh+'-Cvtfall.txt',samplesh+'-Crs.txt',samplesh+'-Csatsc.txt',\
                                   samplesh+'-Cd.txt',samplesh+'-G.txt',samplesh+'-sTI.txt',samplesh+'-Gpicmea.txt',samplesh+'-Gstd.txt']
    PPE2='2ndtuningstep_PhyDynParam_NewParam_'
    ef = "-"+PPE2+"fldmean_ANN.ps"
    results_=read_ICONPPE_add_2dvar(fn,nsimu,noutput,"",ef,yrs)
    results_[:,2]=(results_[:,2]+pressure_addi)*pressure_fact
    results_[:,3]=results_[:,3]*clivi_fact
    results_[:,4]=results_[:,4]*clivi_fact
    varPhyDyn_NewParam_2tun=read_parametersICONPPE_2ndtuningstep(fn,nsimu,nparamPhyDyn_NewParam_2ndTun)
    return varPhyDyn_NewParam_2tun,results_

def results_phydyn_5thPPE_2ndTuningStep_add_2dvar():    
    nsimu=30
    noutput=4
    clivi_fact=1e-3#1000
    pressure_addi=1000
    pressure_fact=100
    yrs="1979-1990"
    PPE='2ndtuningstepsample_PhyDynParam_5thPPE_'
    samplesh=PPE+'Epen_R0top_Cvtfall_Crs_Csatsc_Cd_G_sTI_Gpicmea_Gstd'
    fn=[samplesh+'-Epen.txt',samplesh+'-R0top.txt',samplesh+'-Cvtfall.txt',samplesh+'-Crs.txt',samplesh+'-Csatsc.txt',\
                                   samplesh+'-Cd.txt',samplesh+'-G.txt',samplesh+'-sTI.txt',samplesh+'-Gpicmea.txt',samplesh+'-Gstd.txt']
    
    PPE2='2ndtuningstep_PhyDynParam_5thPPE_'
    ef = "-"+PPE2+"fldmean_ANN.ps"
    results_=read_ICONPPE_add_2dvar(fn,nsimu,noutput,"",ef,yrs)
    results_[:,2]=(results_[:,2]+pressure_addi)*pressure_fact
    results_[:,3]=results_[:,3]*clivi_fact
    results_[:,4]=results_[:,4]*clivi_fact
    varPhyDyn_NewParam_5thPPE=read_parametersICONPPE_2ndtuningstep(fn,nsimu,nparamPhyDyn_NewParam_2ndTun)
    return varPhyDyn_NewParam_5thPPE,results_

def load_addivar_ppes(): 
    noutput=4
    #1st tuning step
    #1st PPE Paper: PPE1
    filenames,nsimu,endfile,yrs=Definitions()
    var1stPPE=read_parametersICONPPE(filenames,nsimu,nparam)
    startfile=""
    results1stPPE=read_ICONPPE_add_2dvar(filenames,nsimu,noutput, startfile,endfile,yrs)

    #2nd PPE: PPE2
    filenames2ndPPE,nsimu2,endfile2,yrs2=Definitions2()
    var2ndPPE=read_parametersICONPPE(filenames2ndPPE,nsimu2,nparam)
    results2ndPPE=read_ICONPPE_add_2dvar(filenames2ndPPE,nsimu2,noutput,startfile,endfile2,yrs2)

    nparamMoreCloudParam, startfileMoreCloudParam=iniDefMorecloudparam()

    # PPE MoreCloudParam: PPE3
    nsimuMoreCloudParam, endfileMoreCloudParam, filenamesMoreCloudParam,yrsM=Definitions_Morecloudparam()
    varMoreCloudParam=read_parametersICONPPE(filenamesMoreCloudParam,nsimuMoreCloudParam,nparamMoreCloudParam)
    resultsMoreCloudParam=read_ICONPPE_add_2dvar(filenamesMoreCloudParam,nsimuMoreCloudParam,noutput,startfileMoreCloudParam,endfileMoreCloudParam,yrsM)

    # PPE MoreCloudParam 2: PPE4
    nsimuMoreCloudParam2, endfileMoreCloudParam2, filenamesMoreCloudParam2,yrsM2= Definitions_Morecloudparam2()
    varMoreCloudParam2=read_parametersICONPPE(filenamesMoreCloudParam2,nsimuMoreCloudParam2,nparamMoreCloudParam)
    resultsMoreCloudParam2=read_ICONPPE_add_2dvar(filenamesMoreCloudParam2,nsimuMoreCloudParam2,noutput,startfileMoreCloudParam,endfileMoreCloudParam2,yrsM2)

    #2nd tuning step: PPE5 
    varPhyDyn_NewParam_2tun,resultsPhyDyn_NewParam_2tun=results_phydyn_NewParam_2tun_add_2dvar()
    varPhyDyn_NewParam_5thPPE_2tun,results_5thPPE_2tun=results_phydyn_5thPPE_2ndTuningStep_add_2dvar()

    return var1stPPE, results1stPPE,var2ndPPE, results2ndPPE, varMoreCloudParam, resultsMoreCloudParam,\
     varMoreCloudParam2, resultsMoreCloudParam2, varPhyDyn_NewParam_2tun,resultsPhyDyn_NewParam_2tun,\
      varPhyDyn_NewParam_5thPPE_2tun,results_5thPPE_2tun