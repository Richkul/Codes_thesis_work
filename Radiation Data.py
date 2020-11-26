def Planes(latitude):
    ''' 
    Creates the five planes for the solar irradiance on equator facing tilted surfaces. 

    - latitude: the latitude value as an float for the single point data request (required)
    '''

    planes = [0.0, -15.0, 0.0, 15.0, 90.0]
    for index in range(1,4):
        planes[index] = planes[index] + abs(round(latitude*2) / 2)

    if latitude > 75.0:
        planes[3] = -999

    if latitude < -75.0:
        planes[1] = -999

    return planes

def SI_Tilted_Surfaces(latitude, longitude, ghi, dhi, albedo, community, option="SI_EF"):
    '''
    Creates the solar irradiance for equator facing tilted set of surfaces for a specific a point location. 

    - latitude: the latitude value as an float for the single point data request (required)
    - longitude: the longitude value as an float for the single point data request (required)
    - ghi: the insolation incident on a horizontal surface (ALLSKY_SFC_SW_DWN) as a list of 12 float vales in kW-hr/m^2/day (required)
    - dhi: the diffuse radiation on a horizontal surface (DIFF) as a list of 12 float vales in kW-hr/m^2/day (required)
    - albedo: the surface albedo (SRF_ALB) as a list of 12 float vales (required)
    - community: the user community (required)
    '''

    middle_day = [17, 16, 16, 15, 15, 11, 17, 16, 15, 15, 14, 10]

    planes = Planes(latitude)
    months = list(range(1,13))

    Data = [] 
    for plane in planes:
        if plane != -999:
            Lists = [] 
            for month in months:
                Lists.append(Tilt_Value(1999, month, middle_day[month-1], latitude, longitude, ghi[month-1], dhi[month-1], albedo[month-1], plane))
            Lists.append(Average_List(Lists))
            Data.append(Lists)
        else:
            Data.append([-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999])

    Irradiance = []
    Angle = []
    Orientation = []
    Tracker = []
    for month in months:
        irradiance, angle, orientation = Optimal_Value(1999, month, middle_day[month-1], latitude, longitude, ghi[month-1], dhi[month-1], albedo[month-1])
        tracker = Tracker_Value(1999, month, middle_day[month-1], latitude, longitude, ghi[month-1], dhi[month-1], albedo[month-1])
        Irradiance.append(irradiance)
        Angle.append(angle)
        Orientation.append(orientation)
        Tracker.append(tracker)

    Irradiance.append(Average_List(Irradiance))
    Average_Angle = round(Average_List(Angle)*2)/2
    Angle.append(Average_Angle)
    Orientation.append(Angle_Orientation(Average_Angle))
    Tracker.append(Average_List(Tracker))

    Data.append(Irradiance)
    Data.append(Angle)
    Data.append(Orientation)
    Data.append(Tracker)

    SI_Names = ['{}_TILTED_SURFACE_HORIZONTAL', '{}_TILTED_SURFACE_LAT_MINUS15', '{}_TILTED_SURFACE_LATITUDE', '{}_TILTED_SURFACE_LAT_PLUS15', '{}_TILTED_SURFACE_VERTICAL', '{}_OPTIMAL', '{}_OPTIMAL_ANG', '{}_OPTIMAL_ANG_ORT', '{}_TRACKER']
    Parameters = [SI_Name.format(option) for SI_Name in SI_Names]

    Dictionary = {}
    for Parameter in Parameters:
        if Parameter == '{}_OPTIMAL_ANG_ORT'.format(option):
            Dictionary[Parameter] = Data[Parameters.index(Parameter)]
        else:
            if community == "AG": # Unit conversion for AG 
                if not Parameter.endswith("_OPTIMAL_ANG_ORT") and not Parameter.endswith("_OPTIMAL_ANG"):
                    eachlist = []
                    for each in Data[Parameters.index(Parameter)]:
                        if each == -999:
                            eachlist.append(-999)
                        else:
                            eachlist.append(round(each * 3.6, 2))

                        Dictionary[Parameter] = eachlist

                else:
                    Dictionary[Parameter] = Data[Parameters.index(Parameter)]

            else:
                Dictionary[Parameter] = [round(elem, 2) for elem in Data[Parameters.index(Parameter)]] 

    return Dictionary

