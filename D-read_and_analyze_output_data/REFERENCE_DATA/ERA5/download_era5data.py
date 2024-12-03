import cdsapi

# Initialize the client
c = cdsapi.Client()

# Request monthly averaged data for skin temperature (surface temperature)
c.retrieve(
    'reanalysis-era5-land-monthly-means',
    {
        'product_type': 'reanalysis',
        'variable': 'skin_temperature',
        'year': [str(year) for year in range(1980, 1990)],
        'month': [f"{month:02d}" for month in range(1, 13)],
        'time': '00:00',
        'format': 'netcdf',
    },
    'era5_skin_temperature_1980_1989.nc'
)
