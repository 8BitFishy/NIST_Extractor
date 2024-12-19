import pandas as pd
import openpyxl

Fluids_ID = {
    'argon': 'C7440371',
    'nitrogen': 'C7727379',
    'helium': 'C7440597',
    'pentane': 'C109660',
    'water': 'C7732185',
    'hydrogen': 'C1333740',
    'parahydrogen': 'B5000001',
    'deuterium': 'C778239',
    'oxygen': 'C7782447',
    'fluorine': 'C7782414',
    'carbon_monoxide': 'C630080',
    'carbon_dioxide': 'C124389',
    'dinitrogen_monoxide': 'C10024972',
    'deuteriu_oxide': 'C7789200',
    'methanol': 'C67561',
    'methane': 'C74828',
    'ethane': 'C74840',
    'ethene': 'C74851',
    'propane': 'C74986',
    'propene': 'C115071',
    'propyne': 'C74997',
    'cyclopropane': 'C7519',
    'butane': 'C106978',
    'isobutane': 'C75285',
    'II_Methylbutane': 'C78784',
    'II_II_Dimethylpropane': 'C463821',
    'hexane': 'C110543',
    'II_methylpentane': 'C107835',
    'cyclohexane': 'C110827',
    'heptane': 'C142825',
    'octane': 'C111659',
    'nonane': 'C111842',
    'decane': 'C124185',
    'dodecane': 'C112403',
    'neon': 'C7440019',
    'krypton': 'C7439909',
    'xenon': 'C7440633',
    'ammonia': 'C7664417',
    'nitrogen_trifluoride': 'C7783542',
    'trichlorofluoromethane_R11': 'C75694',
    'dichlorodifluoromethane_R12': 'C75718',
    'chlorotrifluoromethane_R13': 'C75729',
    'tetrafluoromethane_R14': 'C75730',
    'dichlorofluoromethane_R21': 'C75434',
    'methane_chlorodifluoro_R22': 'C75456',
    'trifluoromethane_R23': 'C75467',
    'methane_difluoro_R32': 'C75105',
    'fluoromethane_R41': 'C593533',
    'I_I_II_trichloro_I_II_II_trifluoroethane_R113': 'C76131',
    'I_II_dichloro_I_II_II_tetrafluoroethane_R114': 'C76142',
    'chloropentafluoroethane_R115': 'C76153',
    'hexafluoroethane_R116': 'C76164',
    'ethane_II_II_dichloro_I_I_I_trifluoro_R123': 'C306832',
    'ethane_I_chloro_I_II_II_II_tetrafluoro_R124': 'C2837890',
    'ethane_pentafluoro_R125': 'C354336',
    'ethane_I_I_I_II_tetrafluoro_R134a': 'C811972',
    'I_I_dichloro_I_fluoroethane_R141b': 'C1717006',
    'I_Chloro_I_I_difluoroethane_R142b': 'C75683',
    'ethane_I_I_I_trifluoro_R143a': 'C420462',
    'ethane_I_I_difluoro_R152a': 'C75376',
    'octafluoropropane_R218': 'C76197',
    'I_I_I_II_III_III_III_heptafluoropropane_R227ea': 'C431890',
    'I_I_I_II_III_III_hexafluoropropane_R236ea': 'C431630',
    'I_I_I_III_III_III_hexafluoropropane_R236fa': 'C690391',
    'I_I_II_II_III_pentafluoropropane_R245ca': 'C679867',
    'I_I_I_III_III_pentafluoropropane_R245fa': 'C460731',
    'octafluorocyclobutane_RC318': 'C115253',
    'benzene': 'C71432',
    'toluene': 'C108883',
    'decafluorobutane': 'C355259',
    'dodecafluoropentane': 'C678262',
    'sulfur_dioxide': 'C7446095',
    'hydrogen_sulfide': 'C7783064',
    'sulfur_hexafluoride': 'C2551624',
    'carbonyl_sulfide': 'C463581',
}


def getNIST(params, units, Digits="5"):
    Tlow = params["Tlow"]
    Thigh = params["Thigh"]
    deltaT = params["deltaT"]
    Plow = params["Plow"]
    Phigh = params["Phigh"]
    deltaP = params["deltaP"]
    fluid_id = Fluids_ID[params["fluid_id"]]

    # collated_data = pd.DataFrame()
    data_list = []
    loading_bar = []

    if Tlow == Thigh:
        temp_count = 1

    else:
        temp_count = int((float(Thigh) - float(Tlow)) / float(deltaT)) + 1

    print(f"Temperature point count = {temp_count}")
    for i in range(temp_count):
        loading_bar.append("_")

    for i in range(temp_count):
        loading_bar[i] = "X"
        print("".join(loading_bar), end="")

        Temp = str(float(Tlow) + (float(deltaT) * i))
        # print(f"i = {i}/{temp_count}")
        # print(f"\nFluid_id = {fluid_id}, Temp = {Temp}, Plow = {Plow}, Phigh = {Phigh}, deltaP = {deltaP}")

        try:
            data = getFromNIST_isoTherm(fluid_id, Temp, Plow, Phigh, deltaP)
            data_list.append(data)
            # if collated_data.empty:
            # collated_data = data
            # else:
            # print("Dataframe not empty")
            # collated_data.add(data)
            print("", end="\r")

        except:
            print("Please, specify parameters correctly")
    collated_data = pd.concat(data_list)
    print(collated_data)
    return collated_data


def get_Units(params):
    units_selected =[]
    default_units = ["K", "bar", "kg%2Fm3", "kJ%2Fkg", "m%2Fs", "Pa*s", "N%2Fm"]
    print()
    print(len(params.index))
    print()
    for i in range(1, 8):
        print(params.loc[i])
        if params.loc[i]["Unit"] != "":
            units_selected.append(params.loc[i]["Unit"].replace("/", "%2F").replace("^", ""))
        else:
            units_selected.append(default_units[i])

    print(f"units selected: {units_selected}")

    '''
    temperature = params.loc[1]["Unit"]
    pressure = params.loc[2]["Unit"]
    density = params.loc[3]["Unit"]
    energy = params.loc[4]["Unit"]
    velocity = params.loc[5]["Unit"]
    viscosity = params.loc[6]["Unit"]
    surface_tension = params.loc[7]["Unit"]

    if temperature == "°C":
        units["TempUnits"] = "C"
    elif temperature == "°F":
        units["TempUnits"] = "F"
    else:
        units["TempUnits"] = temperature

    units["PresUnits"] = pressure

    if density == "mol/l":
        units["DensityUnits"] = "mol%2Fl"

        mol/l
        mol / m ^ 3
        g / ml
        kg / m ^ 3
        lb - mole / ft ^ 3

    temperature:
    K
    C
    F
    R

    Pressure:
    MPa
    bar
    atm
    psia

    Density:
    mol%2Fm3
    g%2Fml
    kg%2Fm3
    lb-mole%2Fft3
    lbm%2Fft3

    Energy
    kJ%2Fmol
    kJ%2Fkg
    kcal%2Fmol
    Btu%2Flb-mole
    kcal%2Fg
    Btu%2Flbm

    Velocity
    m%2fs
    ft%2Fs
    mph

    Viscosity
    uPa*s
    Pa*s
    cP
    lbm%2Fft*s

    surface tension
    N%2Fm
    dyn%2Fcm
    lb%2Fft
    lb%2Fin


'''

    return units_selected


def get_Conditions():

    conditions = {
        "fluid_id": input("Enter fluid name: ").lower().strip(),
        "Tlow": input("Enter lower temperature in kelvin: "),
        "Thigh": input("Enter higher temperature in kelvin: "),
        "deltaT": input("Enter temperature increment: "),
        "Plow": input("Enter lower pressure bound: "),
        "Phigh": input("Enter higher pressure bound: "),
        "deltaP": input("Enter pressure increment: ")
    }

    return params


def getFromNIST_isoTherm(fluid_id='', Temp='', Plow='', Phigh='', deltaP='1',
                         TypeOfData='IsoTherm', TempUnits='K', PresUnits='bar',
                         DensityUnits='kg%2Fm3', EnergyUnits='kJ%2Fkg', VelocityUnits='m%2Fs', ViscosityUnits='Pa*s',
                         Surface_tension='N%2Fm', Digits='5'):
    request = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
               + fluid_id + '&Type=' + TypeOfData + '&Digits=' + Digits + '&PLow=' + Plow
               + '&PHigh=' + Phigh + '&PInc=' + deltaP + '&T=' + Temp
               + '&RefState=DEF&TUnit=' + TempUnits + '&PUnit=' + PresUnits
               + '&DUnit=' + DensityUnits + '&HUnit=' + EnergyUnits + '&WUnit=' + VelocityUnits
               + '&VisUnit=' + ViscosityUnits + '&STUnit=' + Surface_tension)
    data = pd.read_csv(request, delimiter='\t')

    return data


if __name__ == '__main__':
    params = pd.read_excel("NIST Extractor Config File.xlsx")
    print(params)
    units = get_Units(params)
    '''
    #collated_data = getNIST(params, units)
    collated_data.to_csv(f"{params["fluid_id"]} data.csv", index=False)
    '''