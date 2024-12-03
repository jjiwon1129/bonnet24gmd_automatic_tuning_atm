#!/usr/bin/env python
# %%
# this script conducts a hyperparameter tuning analysis
# and estimates the Sobol indices

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import qmc

#homemade function file
import importlib
import ppe_loading_functions #as functions
importlib.reload(ppe_loading_functions)
import ref_data_functions #as functions
importlib.reload(ref_data_functions)

from pylab import cm
import netCDF4
import numpy as np
from netCDF4 import Dataset

#HM
import pickle
from sklearn.gaussian_process.kernels import RBF, Matern
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn import preprocessing
from sklearn.model_selection import KFold, cross_val_score
import random
import gc
gc.set_threshold(0)

# %%
var1stPPE, results1stPPE,var2ndPPE, results2ndPPE, varMoreCloudParam, resultsMoreCloudParam,\
 varMoreCloudParam2, resultsMoreCloudParam2, varPhyDyn_NewParam_2tun,resultsPhyDyn_NewParam_2tun,\
 varPhyDyn_NewParam_5thPPE_2tun,results_5thPPE_2tun=\
ppe_loading_functions.load_all_ppes()

# %%
#Ref tuned ICON-A 2.6.4
pressure_addi,pressure_fact,tauufact,aes_glo_psl,aes_SOO_tauu,aes_NAO_tauu,aes_60N_1000hPa_ua,aes_60S_1000hPa_ua,\
aes_60N_10hPa_ua,aes_60S_10hPa_ua=ref_data_functions.ICON_aes_refdata()

# %%
#Physics Ref
ref_mean, ref_std=ref_data_functions.References_outputs()
#Dynamics Ref
refsERA5, refsMERRA2, refsERAInterim=ref_data_functions.References_Dynoutputs()

#all ref values for Physics and Dynamic variables
ref2tun_mean=np.zeros(9)
ref2tun_mean[0:5]=ref_mean #physics variables
ref2tun_mean[5:]=[refsERA5[0],refsERA5[1],refsERA5[2],refsERA5[3]] #dynamics variables
#ref_mean
print(ref2tun_mean)

#all std for Physics and Dynamic variables: not used yet in the HM flow

# %%
ref_Clt_ESACCI, ref_Clt_ESACCI_std, ref_Clt_CLARA_AVHRR, ref_Clt_CLARA_AVHRR_std=ref_data_functions.Ref_clt()
ref_Prw_ESACCI, ref_Prw_ERA5, ref_Prw_ERA5_std=ref_data_functions.Ref_prw()

# %%
years_clt_esacci,clt_esacci_per_year=ref_data_functions.clt_esacci_per_years()
years_clt_claraavhrr,clt_claraavhrr_per_year=ref_data_functions.clt_claraavhrr_per_years()
years_prw_era5,prw_era5_per_year=ref_data_functions.prw_era5_per_years()

# %% [markdown]
# # Emulator training and performance

# %%
#Physics parameters then needs HM
#bounds enlarged for HM
#Emid_bounds = [2e-5, 3e-4] #not in the PhyDyn PPEs
iEpen_bounds = [2e-4, 6e-4] # default value used before is 3.0e-4
iR0top_bounds = [5e-1, 9e-1] # default value used before is 0.8
iCprcon_bounds = [0.00015 , 0.00035] # default value used before is 2.5e-4
iCvtfall_bounds = [0.2 , 4] # default value used before is 2.5
boundsPhy=[iEpen_bounds,iR0top_bounds,iCprcon_bounds,iCvtfall_bounds]
#additional physics parameters
crs_bounds = [0.75*0.968,0.99] #default value used before is 0.968 in src/configure_model/echam_cov_config.f90
csatsc_bounds = [0.7*0.5,0.7*1.5] #default value used before is 0.7 in src/configure_model/echam_cov_config.f90

#Dynamic parameters (same in all notebooks) 
iCd_bounds = [ 0.001, 0.09 ] #default value used in 1st tuning step 0.05 gkwake  = CdCdCd
iG_bounds = [ 0.002, 0.28 ] #default value used in 1st tuning step 0.05 gkdrag  = GGG
isTI_bounds = [ 0.647, 1.079 ] #[ 0.1, 2 ]  # NEW FOR 3rd PhyDyn PPE 0.87/8,0.87*8-> 7 too large, so down to 2 max [ 0.647, 1.079 ] #default value used in 1st tuning step 0.87 rmscon  = sTIsTIsTI
bounds_Dyn2PPE=[iCd_bounds,iG_bounds,isTI_bounds]
#additional dynamic parameters
igpicmea_bounds =[20,60] #[5,320] # NEW FOR 3rd PhyDyn PPE [40/8,40*8] [20,60]#40*0.5,40*1.5 default value used before 40 in src/configure_model/mo_echam_sso_config.f90
igstd_bounds = [5,15] #[1.25,80] # NEW FOR 3rd PhyDyn PPE 10/8,10*8 #[5,15]#10*0.5,10*1.5 default value used before 10 in src/configure_model/mo_echam_sso_config.f90
#iemiss_lev_bounds = [10]#[23:38]#10*0.5,10*1.5 /!\ need to take integers ! default value used before 10 # can use any levels such as 5,6,7,8,9,10,11,12,13,14,15?

boundsPhyDyn=[iEpen_bounds,iR0top_bounds,iCprcon_bounds,iCvtfall_bounds,iCd_bounds,iG_bounds,isTI_bounds]
boundsPhyDyn_newParam=[iEpen_bounds,iR0top_bounds,iCvtfall_bounds,crs_bounds,csatsc_bounds,iCd_bounds,iG_bounds,isTI_bounds,igpicmea_bounds,igstd_bounds]#,iemiss_lev_bounds]


# %%
# train the GP on the training sample - only phy parameters
def score_1st_tuning_step(varr,resultss):
            
    randsamples={}

    kernel = 1 * Matern(length_scale=1.0)#, nu=1.5) #RBF(length_scale=1.0, length_scale_bounds=(1e-5, 1e5)) #np.array([1.0,1.0,1.0])) #length_scale=10) # ,1.0,1.0,1.0]))#, length_scale_bounds=(1e-2, 1e2))
    gaussian_process_multi = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=100)#,alpha=1e-5, n_restarts_optimizer=20)

    #scale data https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#sklearn.preprocessing.StandardScaler
    scaler_var1_2tun = preprocessing.StandardScaler().fit(varr,)
    scaled_var1_2tun = scaler_var1_2tun.transform(varr)

    Ntot=59 # total size of the sample
    sizeRes_60=np.arange(20,59,4) #[10,15,20,25,30,35,40,45,50,55]
    Nrand=20 # number of times we pick a sample of a given size
    score_isize_60=np.zeros((np.size(sizeRes_60),Nrand))
    #score_isize_60_max=np.zeros((np.size(sizeRes_60)))
    #score_isize_60_min=np.zeros((np.size(sizeRes_60)))
    score_isize_60_mean=np.zeros((np.size(sizeRes_60)))
    score_isize_60_std=np.zeros((np.size(sizeRes_60)))

    indSi=0
    for Sizz in sizeRes_60:
        print('\n ------------------------------------------------------ starting size '+str(Sizz)+ '\n')
        indsam={}
        for irand in np.arange(0,Nrand):
            RandSamp=random.sample(range(1,Ntot),Sizz)
            indsam[irand]=RandSamp
            scaled_var1_2tun = scaler_var1_2tun.transform(varr[RandSamp])
            gaussian_process_multi.fit(scaled_var1_2tun, resultss[RandSamp]) #results_dyn_2tun_psltauuNAOSSO #results_all_2tun) #
            gaussian_process_multi.kernel_

            score=cross_val_score(gaussian_process_multi, scaled_var1_2tun, resultss[RandSamp])
            score_isize_60[indSi,irand]=np.mean(score)
            
            randsamples[Sizz]=indsam
            #score_isize_60_min[indSi]=np.min(score_isize_60[indSi,:])
            #score_isize_60_max[indSi]=np.max(score_isize_60[indSi,:])
            score_isize_60_mean[indSi]=np.mean(score_isize_60[indSi,:])
            score_isize_60_std[indSi]=np.std(score_isize_60[indSi,:])

        indSi+=1
    return sizeRes_60,score_isize_60_mean,score_isize_60_std,Nrand
#duration approx 1min10 (5min33sec)

# %%

print('\n------------------------------------------------------------ PPE1, PPE2 start \n')

#to comment once done
varr=np.concatenate((var1stPPE,var2ndPPE),axis=0)
resultss=np.concatenate((results1stPPE,results2ndPPE),axis=0) #phy
sizeRes_60_1stt,score_isize_60_mean_1stt,score_isize_60_std_1stt,Nrand_1stt=score_1st_tuning_step(varr,resultss)

#approx 12 # 14min30sec

# %%
# save to dictionary the parameter values for the PPEs
namefile = 'Perf_withSize_PPE1_2_n20.pkl'
#namefile = 'Perf_withSize_PPE1_2.pkl'


#to comment once done
perf_PPE1_2 = dict()
perf_PPE1_2['sizeRes_60_1stt']=sizeRes_60_1stt
perf_PPE1_2['score_isize_60_mean_1stt']=score_isize_60_mean_1stt
perf_PPE1_2['score_isize_60_std_1stt']=score_isize_60_std_1stt
perf_PPE1_2['Nrand_1stt']=Nrand_1stt
with open(namefile, 'wb') as f:
    pickle.dump(perf_PPE1_2, f)

print('\n------------------------------------------------------------ PPE1, PPE2 done')
# to uncomment when previously saved %%
'''
#namefile = 'Perf_withSize_PPE1_2_n20.pkl'
#namefile = 'Perf_withSize_PPE1_2.pkl'

with open(namefile, 'rb') as f:
    perf_PPE1_2_loaded = pickle.load(f)


sizeRes_60_1stt=perf_PPE1_2_loaded['sizeRes_60_1stt']
score_isize_60_mean_1stt=perf_PPE1_2_loaded['score_isize_60_mean_1stt']
score_isize_60_std_1stt=perf_PPE1_2_loaded['score_isize_60_std_1stt']
Nrand_1stt=perf_PPE1_2_loaded['Nrand_1stt']
'''
# %%
#to comment once done

print('\n------------------------------------------------------------ PPE3, PPE4 start')
varr=np.concatenate((varMoreCloudParam,varMoreCloudParam2),axis=0)
resultss=np.concatenate((resultsMoreCloudParam,resultsMoreCloudParam2),axis=0) #phy
sizeRes_60_1stt_More,score_isize_60_mean_1stt_More,score_isize_60_std_1stt_More,Nrand_1stt_More=score_1st_tuning_step(varr,resultss)


# %%
# save to dictionary the parameter values for the PPEs
namefile = 'Perf_withSize_PPE3_4_n20.pkl'
#namefile = 'Perf_withSize_PPE3_4.pkl'


#to comment once done
perf_PPE3_4 = dict()
perf_PPE3_4['sizeRes_60_1stt_More']=sizeRes_60_1stt_More
perf_PPE3_4['score_isize_60_mean_1stt_More']=score_isize_60_mean_1stt_More
perf_PPE3_4['score_isize_60_std_1stt_More']=score_isize_60_std_1stt_More
perf_PPE3_4['Nrand_1stt_More']=Nrand_1stt_More
with open(namefile, 'wb') as f:
    pickle.dump(perf_PPE3_4, f)

print('\n------------------------------------------------------------ PPE3, PPE4 done')

# to uncomment when previously saved
'''
namefile = 'Perf_withSize_PPE3_4_n20.pkl'

with open(namefile, 'rb') as f:
    perf_PPE3_4_loaded = pickle.load(f)

sizeRes_60_1stt_More=perf_PPE3_4_loaded['sizeRes_60_1stt_More']
score_isize_60_mean_1stt_More=perf_PPE3_4_loaded['score_isize_60_mean_1stt_More']
score_isize_60_std_1stt_More=perf_PPE3_4_loaded['score_isize_60_std_1stt_More']
Nrand_1stt_More=perf_PPE3_4_loaded['Nrand_1stt_More']
'''

# %%
labelPhy=["training on $PPE_1$ and $PPE_2$, 6 parameters","training on $PPE_3$ and $PPE_4$, 7 parameters"]
colors=['r','c']
inddRealistic=np.where(abs(score_isize_60_mean_1stt[:])<1e3)[0] #remove runs that had a bug
inddRealistic_More=np.where(abs(score_isize_60_mean_1stt_More[:])<1e3)[0] #remove runs that had a bug

print(inddRealistic)
plt.subplots()
sizefont=20
plt.rc('font', size=sizefont) 
plt.rcParams['figure.figsize'] = [10, 7]

alp=0.2
iplot=0
plt.plot(sizeRes_60_1stt[inddRealistic],score_isize_60_mean_1stt[inddRealistic],'-',color=colors[iplot],label=labelPhy[iplot])
plt.fill_between(sizeRes_60_1stt[inddRealistic],score_isize_60_mean_1stt[inddRealistic]-score_isize_60_std_1stt[inddRealistic],\
                     score_isize_60_mean_1stt[inddRealistic]+score_isize_60_std_1stt[inddRealistic],\
                        color=colors[iplot],alpha=alp)

iplot=1
plt.plot(sizeRes_60_1stt_More[inddRealistic_More],score_isize_60_mean_1stt_More[inddRealistic_More],'-',color=colors[iplot],label=labelPhy[iplot])
plt.fill_between(sizeRes_60_1stt[inddRealistic_More],score_isize_60_mean_1stt_More[inddRealistic_More]-\
                     score_isize_60_std_1stt_More[inddRealistic_More],score_isize_60_mean_1stt_More[inddRealistic_More]+\
                        score_isize_60_std_1stt_More[inddRealistic_More],color=colors[iplot],alpha=alp)

plt.xlim(22,57)
plt.ylim(-0.1,0.9)
#plt.ylim(-0.5,1)
plt.legend(loc='lower right')
plt.ylabel(r'$R^2$-score of the GP emulator')
plt.xlabel('Size of ICON-A PPE used for training')
plt.yticks(np.arange(-0.1,0.9,0.1))
#plt.yticks(np.arange(-0.5,1.1,0.1))
plt.grid()
plt.savefig("PaperFig/Performance_Emulator_wrt_size_ICON_PPE_1st_tuning_Step_test.png")
