# this script has functions that are called to load the reference datasets


import numpy as np
import iris
import netCDF4
from netCDF4 import Dataset



#----------Reference satellite measurements for all 5 outputs 

# reference data for TOA incoming and outgoing radiation: CERES data : https://ceres-tool.larc.nasa.gov/ord-tool/srbavg
def References_outputs():
    datafile='CERES_EBAF-TOA_Ed4.1_Subset_CLIM01-CLIM12.nc'
    file = Dataset('./REFERENCE_DATA/'+datafile, "r", format="NETCDF4")

    '''
    ref_TOASW=[np.min(file['gsolar_clim'][:]-file['gtoa_sw_all_clim'][:]), np.max(file['gsolar_clim'][:]-file['gtoa_sw_all_clim'][:])]   #m/W^2 
    ref_TOALW=[np.min(file['gtoa_lw_all_clim'][:]),np.max(file['gtoa_lw_all_clim'][:])] #m/W^2
    ref_netTOA=[0,1]      #W/m^2
    ref_wvp= [24.3,24.5]  #kg/m^2
    ref_Cl=[np.min(file['gcldarea_total_daynight_clim'][:]),np.max(file['gcldarea_total_daynight_clim'][:])]  #%
    '''

    ref_TOASW=file['gsolar_clim'][:]-file['gtoa_sw_all_clim'][:] #m/W^2 
    ref_TOALW=-file['gtoa_lw_all_clim'][:] #m/W^2
    ref_Cl=file['gcldarea_total_daynight_clim'][:] #%

    ref_netTOA=[0,1]      #W/m^2

    #reference ERA Interim for prw
    filebase='/work/bd0854/DATA/ESMValTool2/OBS/Tier3/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_prw_'
    ref_wvp=[]
    for year in np.arange(1980,1989):
        datafile=filebase+str(year)+'01-'+str(year)+'12.nc'
        cube = iris.load_cube(datafile,'atmosphere_mass_content_of_water_vapor')
        grid_areas = iris.analysis.cartography.area_weights(cube)
        average = cube.collapsed(['longitude', 'latitude'], iris.analysis.MEAN, weights=grid_areas)
        #print(average.data)
        ref_wvp.append(np.mean(average.data)) #kg/m^2

    refs= [ref_TOASW, ref_TOALW, ref_netTOA, ref_Cl,  ref_wvp]

    ref_mean=np.zeros(5)
    ref_std=np.zeros(5)

    for ii in np.arange(0,5):
        ref_mean[ii]=np.mean(refs[ii])
        ref_std[ii]=np.std(refs[ii])
        if ii ==2:
            ref_mean[ii]=(refs[ii][0]+refs[ii][1])/2
            ref_std[ii]=(refs[ii][1]-refs[ii][0])/3 #for a Gaussian distribution 99% in 3 std
    return ref_mean, ref_std

def References_Dynoutputs():

    #ERA5
    ERA5_ua_60N_10hPa_198001_198912=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_1_Amon_ua_198001-198912_60N_10hPa_fldmean.nc')['ua'])
    ERA5_ua_60S_10hPa_198001_198912=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_1_Amon_ua_198001-198912_60S_10hPa_fldmean.nc')['ua'])
    ERA5_tauu_NAO_198001_198912=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/tauu_ERA5_198001-198912_unstruc_NAO.nc')['tauu'])
    ERA5_tauu_SOO_198001_198912=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/tauu_ERA5_198001-198912_unstruc_SOO.nc')['tauu'])

    #MERRA2
    MERRA2_ua_1980_1989_60N_10hPa=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_ua_198001-198912_60N_10hPa_fldmean.nc')['ua'])
    MERRA2_ua_1980_1989_60S_10hPa=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_ua_198001-198912_60S_10hPa_fldmean.nc')['ua'])
    MERRA2_tauu_NAO=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_tauu_198001-198912_unstruc_NAO.nc')['tauu'])
    MERRA2_tauu_SOO=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_tauu_198001-198912_unstruc_SOO.nc')['tauu'])

    #ERA-Interim
    ERAInterim_ua_1980_1989_60N_10hPa=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_ua_198001-198912_60N_10hPa.nc')['ua'])
    ERAInterim_ua_1980_1989_60S_10hPa=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_ua_198001-198912_60S_10hPa.nc')['ua'])
    ERAInterim_tauu_NAO=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_tauu_198001-198912_unstruc_NAO.nc')['tauu'])
    ERAInterim_tauu_SOO=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_tauu_198001-198912_unstruc_SOO.nc')['tauu'])

    refsERA5= [ERA5_ua_60N_10hPa_198001_198912,ERA5_ua_60S_10hPa_198001_198912,ERA5_tauu_NAO_198001_198912,ERA5_tauu_SOO_198001_198912]
    refsMERRA2= [MERRA2_ua_1980_1989_60N_10hPa,MERRA2_ua_1980_1989_60S_10hPa,MERRA2_tauu_NAO,MERRA2_tauu_SOO]
    refsERAInterim= [ERAInterim_ua_1980_1989_60N_10hPa,ERAInterim_ua_1980_1989_60S_10hPa,ERAInterim_tauu_NAO,ERAInterim_tauu_SOO]

    return refsERA5, refsMERRA2, refsERAInterim

#Ref tuned ICON-A 2.6.4

def ICON_aes_refdata():
    factPsl=0.01
    pressure_addi=1000
    pressure_fact=100
    tauufact=1000
    aes_glo_psl=(11.0486+pressure_addi)*pressure_fact*factPsl
    aes_SOO_tauu=144.8539*1e-3
    aes_NAO_tauu=-2.6838*1e-3
    aes_60N_1000hPa_ua=0.0737
    aes_60S_1000hPa_ua=5.1414
    aes_60N_10hPa_ua=4.6258
    aes_60S_10hPa_ua=24.2116
    return pressure_addi,pressure_fact,tauufact,aes_glo_psl,aes_SOO_tauu,aes_NAO_tauu,aes_60N_1000hPa_ua,aes_60S_1000hPa_ua,aes_60N_10hPa_ua,aes_60S_10hPa_ua
    

def Ref_clt():
    #ESACCI
    #clt
    #mean
    datafile='REFERENCE_DATA/OBS_ESACCI-CLOUD_sat_AVHRR-AMPM-fv3.0_Amon_clt_198001-198912_fldmean_timavg.nc'
    file = Dataset('./'+datafile, "r", format="NETCDF4")
    ref_Clt_ESACCI=file['clt'][:][0][0][0] #%
    #print('ref_Clt_ESACCI',ref_Clt_ESACCI)
    #std
    datafile='REFERENCE_DATA/OBS_ESACCI-CLOUD_sat_AVHRR-AMPM-fv3.0_Amon_clt_198001-198912_fldmean_timstd.nc'
    file = Dataset('./'+datafile, "r", format="NETCDF4")
    ref_Clt_ESACCI_std=file['clt'][:][0][0][0] #%
    #print('ref_Clt_ESACCI_std',ref_Clt_ESACCI_std)

    #CLARA_AVHRR
    #clt
    #mean
    ref_Clt_CLARA_AVHRR=np.mean(netCDF4.Dataset('REFERENCE_DATA/CLARA-AVHRR/test1986-1995/OBS_CLARA-AVHRR_sat_V002_01_Amon_clt_1986-1995_fldmean_timavg.nc')['clt'])# in %

    #std
    datafile='REFERENCE_DATA/OBS_CLARA-AVHRR_sat_V002_01_Amon_clt_198201-199112_fldmean_timstd.nc'
    file = Dataset('./'+datafile, "r", format="NETCDF4")
    ref_Clt_CLARA_AVHRR_std=file['clt'][:][0][0][0] #%
    #print('ref_Clt_CLARA_AVHRR_std',ref_Clt_CLARA_AVHRR_std)
    return ref_Clt_ESACCI, ref_Clt_ESACCI_std, ref_Clt_CLARA_AVHRR, ref_Clt_CLARA_AVHRR_std


def Ref_prw():
    #prw
    datafile= 'REFERENCE_DATA/OBS6_ESACCI-WATERVAPOUR_sat_CDR2-L3-COMBI-05deg-fv3.1_Amon_prw_198001-198912_fldmean_timavg.nc' #'REFERENCE_DATA/OBS6_ESACCI-WATERVAPOUR_sat_CDR2-L3-COMBI-05deg-fv3.1_Amon_prw_198001-198912_fldmean.nc'
    file = Dataset('./'+datafile, "r", format="NETCDF4")
    ref_Prw_ESACCI=file['prw'][:][0][0][0] #%
    #print('ref_Prw_ESACCI',ref_Prw_ESACCI)

    #ERA5
    #prw
    #mean
    datafile='REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_v1_Amon_prw_198001-198912_fldmean_timavg.nc'
    file = Dataset('./'+datafile, "r", format="NETCDF4")
    ref_Prw_ERA5=file['prw'][:][0][0][0] #%
    #print('ref_Prw_ERA5',ref_Prw_ERA5)
    #std
    datafile='REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_v1_Amon_prw_198001-198912_fldmean_timstd.nc'
    file = Dataset('./'+datafile, "r", format="NETCDF4")
    ref_Prw_ERA5_std=file['prw'][:][0][0][0] #%
    #print('ref_Prw_ERA5_std',ref_Prw_ERA5_std)
    return ref_Prw_ESACCI, ref_Prw_ERA5, ref_Prw_ERA5_std
    


#plot variability with the years of reference values for the prw

def clt_esacci_per_years():
    clt_esacci_per_year=[]
    years_clt_esacci=np.arange(1982,1992)
    for yr in years_clt_esacci:
        datafile='REFERENCE_DATA/OBS_ESACCI-CLOUD_sat_AVHRR-AMPM-fv3.0_Amon_clt_'+str(yr)+'_fldmean_timavg.nc'
        file = Dataset('./'+datafile, "r", format="NETCDF4")
        cltt=file['clt'][:][0][0][0] #%
        clt_esacci_per_year.append(cltt)
    #print(clt_esacci_per_year)
    return years_clt_esacci,clt_esacci_per_year

    #/!\ year 1985 had a nan value on month 02, february, so I calculated the mean on 1985 without the month of february OBS_CLARA-AVHRR_sat_V002_01_Amon_clt_1985_remove_nan_1985-02-15
def clt_claraavhrr_per_years():
    clt_claraavhrr_per_year=[]
    years_clt_claraavhrr=np.arange(1982,1992) 
    for yr in years_clt_claraavhrr:
        datafile='REFERENCE_DATA/OBS_CLARA-AVHRR_sat_V002_01_Amon_clt_'+str(yr)+'_fldmean_timavg.nc'
        file = Dataset('./'+datafile, "r", format="NETCDF4")
        cltt=file['clt'][:][0][0][0] #%
        clt_claraavhrr_per_year.append(cltt)
    #print(clt_claraavhrr_per_year)
    return years_clt_claraavhrr,clt_claraavhrr_per_year

def prw_era5_per_years():
    prw_era5_per_year=[]
    years_prw_era5=np.arange(1980,1992)
    for yr in years_prw_era5:
        datafile='REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_v1_Amon_prw_'+str(yr)+'_fldmean_timavg.nc'
        file = Dataset('./'+datafile, "r", format="NETCDF4")
        cltt=file['prw'][:][0][0][0] #%
        prw_era5_per_year.append(cltt)
    #print(prw_era5_per_year)
    return years_prw_era5,prw_era5_per_year



def era5_data():
    ERA5_glo_tauu=np.mean(netCDF4.Dataset('REFERENCE_DATA/tauumean_ERA.nc')['tauu'])*1000
    ERA5_NAO_tauu=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/tauumean_ERA5_NAO.nc')['tauu'])
    ERA5_SOO_tauu=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/tauumean_ERA5_SOO.nc')['tauu'])
    ERA5_60N_10hPa_ua=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/ERA5_ua_60N_10hPa.nc')['ua'])
    ERA5_60N_1000hPa_ua=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/ERA5_ua_60N_1000hPa.nc')['ua'])
    ERA5_60S_10hPa_ua=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/ERA5_ua_60S_10hPa.nc')['ua'])
    ERA5_60S_1000hPa_ua=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/ERA5_ua_60S_1000hPa.nc')['ua'])
    #all ref values for the 2nd tuning step
    ref2tun_mean=np.zeros(9)
    ref_mean, ref_std=References_outputs()
    ref2tun_mean[0:5]=ref_mean #physics variables
    ref2tun_mean[5:]=[ERA5_NAO_tauu,ERA5_SOO_tauu,ERA5_60N_10hPa_ua,ERA5_60S_10hPa_ua] #dynamics variables
    return ref2tun_mean
    
def ref_addi_var_ERA5():
    ERA5_ts=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_1_Amon_ts_199001-199112_timavg_fldmean.nc')['ts'])-273.15 #in C
    #ERA5_ta=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_v1_Amon_ta_198001-198912_timavg_fldmean_plev100000.nc')['ta'])-273.15 #in C
    ERA5_pr=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_v1_Amon_pr_198001-198912_timavg_fldmean.nc')['pr'])*86400 #in mm/day
    ERA5_psl=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_1_day_psl_1980-1989_timavg_fldmean.nc')['psl']) #in Pa
    ERA5_clivi=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA5/OBS6_ERA5_reanaly_v1_Amon_clivi_198001-198901_timavg_fldmean.nc')['clivi']) #kg/m2
    return ERA5_ts, ERA5_pr, ERA5_psl,ERA5_clivi

def ref_addi_var_ERAInterim():
    ERAInterim_ts=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_ts_1980-1989_timavg_fldmean.nc')['ts'])-273.15 #in C
    ERAInterim_pr=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_pr_1980-1989_timavg_fldmean.nc')['pr'])*86400 #in kg/m2
    ERAInterim_psl=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_psl_198001-198901_timavg_fldmean.nc')['psl']) #in hPa
    ERAInterim_clivi=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_clivi_1980-1989_timavg_fldmean.nc')['clivi']) #in kg/m2
    ERAInterim_clwvi=np.mean(netCDF4.Dataset('REFERENCE_DATA/ERA-Interim/OBS6_ERA-Interim_reanaly_1_Amon_clwvi_1980-1989_timavg_fldmean.nc')['clwvi']) #in kg/m2
    return ERAInterim_ts, ERAInterim_pr, ERAInterim_psl, ERAInterim_clivi, ERAInterim_clwvi

def icon_aes_validation():
    icon_aes_ts=np.mean(netCDF4.Dataset('REFERENCE_DATA/icon-aes/mag0217_amip_atm_2d_ml_1980-1988_fldmean_timavg.nc')['ts'])-273.15 #in C
    icon_aes_pr=np.mean(netCDF4.Dataset('REFERENCE_DATA/icon-aes/mag0217_amip_atm_2d_ml_1980-1988_fldmean_timavg.nc')['pr'])*86400 #in mm/day
    icon_aes_psl=np.mean(netCDF4.Dataset('REFERENCE_DATA/icon-aes/mag0217_amip_atm_2d_ml_1980-1988_fldmean_timavg.nc')['psl']) #in Pa
    icon_aes_clivi=np.mean(netCDF4.Dataset('REFERENCE_DATA/icon-aes/mag0217_amip_atm_2d_ml_1980-1988_fldmean_timavg.nc')['clivi']) #in kg/m2
    icon_aes_cllvi=np.mean(netCDF4.Dataset('REFERENCE_DATA/icon-aes/mag0217_amip_atm_2d_ml_1980-1988_fldmean_timavg.nc')['cllvi']) #in kg/m2
    icon_aes_hfss=np.mean(netCDF4.Dataset('REFERENCE_DATA/icon-aes/mag0217_amip_atm_2d_ml_1980-1988_fldmean_timavg.nc')['hfss']) #in W m-2
    icon_aes_hfls=np.mean(netCDF4.Dataset('REFERENCE_DATA/icon-aes/mag0217_amip_atm_2d_ml_1980-1988_fldmean_timavg.nc')['hfls']) #in W m-2
    return icon_aes_ts, icon_aes_pr, icon_aes_psl, icon_aes_clivi, icon_aes_cllvi, icon_aes_hfss, icon_aes_hfls

def MERRA2_validation():
    merra2_ts=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_ts_1980-1989_timavg_fldmean.nc')['ts'])-273.15 #in C
    merra2_pr=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_pr_1980-1989_timavg_fldmean.nc')['pr'])*86400 #in kg/m2
    merra2_psl=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_psl_1980-1989_timavg_fldmean.nc')['psl']) #in Pa
    merra2_clivi=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_clivi_1980-1989_timavg_fldmean.nc')['clivi']) #in kg/m2
    merra2_clwvi=np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_clwvi_1980-1989_timavg_fldmean.nc')['clwvi']) #in kg/m2
    merra2_hfss=-np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_hfss_1980-1989_timavg_fldmean.nc')['hfss']) #in W m-2
    merra2_hfls=-np.mean(netCDF4.Dataset('REFERENCE_DATA/MERRA2/OBS6_MERRA2_reanaly_5.12.4_Amon_hfls_1980-1989_timavg_fldmean.nc')['hfls']) #in W m-2
    return merra2_ts, merra2_pr, merra2_psl, merra2_clivi, merra2_clwvi, merra2_hfss, merra2_hfls