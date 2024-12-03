load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begin

print ("pltdir: "+pltdir)
print ("quelle: "+quelle)

  datfil = pltdir+"/busy_atm_phy.nc"
  varfil = quelle+"/VARS.txt"
print("varfil "+varfil)
  varnumbers=stringtoint(systemfunc("wc -l " +varfil))   ;-- KMF
;  varnumbers=stringtoint(systemfunc("wc -l " +varfil+ "|cut -f1 -d' '"))
;print(varnumbers)
   maxnumber=varnumbers

 Vmean  = new((/maxnumber/),double)
 Vmin  = new((/maxnumber/),double)
 Vmax  = new((/maxnumber/),double)
 Vname  = new((/maxnumber/),string)
 Vstring  = new((/maxnumber/),string)
 Vunit  = new((/maxnumber/),string)
 Vdef  = new((/maxnumber/),string)

    
 strs = asciiread(varfil,-1,"string")
 delim = ","
 nfields = str_fields_count(strs(0), delim)   ; Count the fields separated
; print(nfields)                               ; by one or more spaces.

 field = 1
 Varname = str_get_field(strs, field, delim)
; print(Varname)                           
 field = 2
 Factor = stringtofloat(str_get_field(strs, field, delim))
 print("Factor "+Factor)              
 field = 3
 Offset = stringtofloat(str_get_field(strs, field, delim))
 print("Offset " +Offset)              
 field = 4
 Var_unit = str_get_field(strs, field, delim)
; print(Var_unit)   
 field = 5
 Var_def = str_get_field(strs, field, delim)
; print(Var_def)   


  GridInfoFileName = systemfunc("echo $GrdInfoFile")
  print("GridInfoFileName: "+GridInfoFileName)

  GridInfoFile= addfile( GridInfoFileName, "r" )

  rad2deg = 45./atan(1.)            ; radians to degrees

  x = GridInfoFile->clon *rad2deg   ; cell center, lon
  y = GridInfoFile->clat *rad2deg   ; cell center, lat
  cArea = GridInfoFile->cell_area   ; area of grid cell


  File    = addfile (datfil , "r")  
print("datfil "+ datfil)
print("coucou Varname:")
;printVarSummary(File)
  i=-1
  do k=0,varnumbers-1
    if (isfilevar(File,Varname(k))) then
print(k+" "+Varname(k))
print(File->$Varname(k)$(0,:))
        i = i+1
        Var = File->$Varname(k)$(0,:) ;(time,ncells)
        Var=(Var*Factor(k))+Offset(k)
        Vmean(i)=dim_avg(Var*cArea)/dim_avg(cArea)
        Vmin(i)=min(Var)
        Vmax(i)=max(Var)
        Vname(i)=Varname(k)
        Vunit(i)=Var_unit(k)
        Vdef(i)=Var_def(k)
;print("RESULT  "+Varname(k)+"   "+Vname(i)+" def  "+Vdef(i))
;print("      min: "+min(Var)+ "      max: "+max(Var))
    end if
  end do

NoVar=i
print("number of vars: "+NoVar)



 alist = [/Vname(:NoVar), Vmin(:NoVar), Vmean(:NoVar), Vmax(:NoVar), Vunit(:NoVar), Vdef(:NoVar)/]
 fname = "busy_table.txt"
 header = (/"---------------------------------------------------------------------------------------------------", \
            "      name          min      fldmean          max     unit    description", \
            "---------------------------------------------------------------------------------------------------"/)
 hlist = [/header/]
 write_table(fname, "w", hlist, "%s")
 write_table(fname, "a", alist, "%10s%12.4f%12.4f%12.4f%8s%-40s")
exit
  
end
