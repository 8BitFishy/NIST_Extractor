import os
from pandas import isna, read_excel, concat, read_csv
from time import ctime


Fluids_ID =    {
                'argon' : 'C7440371',
                'nitrogen' : 'C7727379',
                'helium' : 'C7440597',
                'pentane' : 'C109660',
                'water' : 'C7732185',
                'hydrogen' :'C1333740',
                'parahydrogen' : 'B5000001',
                'deuterium' : 'C778239',
                'oxygen' : 'C7782447',
                'fluorine' : 'C7782414',
                'carbon_monoxide' :  'C630080',
                'carbon_dioxide' : 'C124389',
                'dinitrogen_monoxide' : 'C10024972',
                'deuteriu_oxide' : 'C7789200',
                'methanol' : 'C67561',
                'methane' : 'C74828',
                'ethane' : 'C74840',
                'ethene' : 'C74851',
                'propane' : 'C74986',
                'propene' : 'C115071',
                'propyne' : 'C74997',
                'cyclopropane' : 'C7519',
                'butane' : 'C106978',
                'isobutane' : 'C75285',
                'II_Methylbutane' : 'C78784',
                'II_II_Dimethylpropane' : 'C463821',
                'hexane' : 'C110543',
                'II_methylpentane' : 'C107835',
                'cyclohexane' : 'C110827',
                'heptane' : 'C142825',
                'octane' : 'C111659',
                'nonane' : 'C111842',
                'decane' : 'C124185',
                'dodecane' : 'C112403',
                'neon' : 'C7440019',
                'krypton' : 'C7439909',
                'xenon' : 'C7440633',
                'ammonia' : 'C7664417',
                'nitrogen_trifluoride' : 'C7783542',
                'trichlorofluoromethane_R11' : 'C75694',
                'dichlorodifluoromethane_R12' : 'C75718',
                'chlorotrifluoromethane_R13' : 'C75729',
                'tetrafluoromethane_R14' : 'C75730',
                'dichlorofluoromethane_R21' : 'C75434',
                'methane_chlorodifluoro_R22' : 'C75456',
                'trifluoromethane_R23' : 'C75467',
                'methane_difluoro_R32' : 'C75105',
                'fluoromethane_R41' : 'C593533',
                'I_I_II_trichloro_I_II_II_trifluoroethane_R113' : 'C76131',
                'I_II_dichloro_I_II_II_tetrafluoroethane_R114' : 'C76142',
                'chloropentafluoroethane_R115' : 'C76153',
                'hexafluoroethane_R116' : 'C76164',
                'ethane_II_II_dichloro_I_I_I_trifluoro_R123' : 'C306832',
                'ethane_I_chloro_I_II_II_II_tetrafluoro_R124' : 'C2837890',
                'ethane_pentafluoro_R125' : 'C354336',
                'ethane_I_I_I_II_tetrafluoro_R134a' : 'C811972',
                'I_I_dichloro_I_fluoroethane_R141b' : 'C1717006',
                'I_Chloro_I_I_difluoroethane_R142b' : 'C75683',
                'ethane_I_I_I_trifluoro_R143a' : 'C420462',
                'ethane_I_I_difluoro_R152a' : 'C75376',
                'octafluoropropane_R218' : 'C76197',
                'I_I_I_II_III_III_III_heptafluoropropane_R227ea' : 'C431890',
                'I_I_I_II_III_III_hexafluoropropane_R236ea' : 'C431630',
                'I_I_I_III_III_III_hexafluoropropane_R236fa' : 'C690391',
                'I_I_II_II_III_pentafluoropropane_R245ca' : 'C679867',
                'I_I_I_III_III_pentafluoropropane_R245fa' : 'C460731',
                'octafluorocyclobutane_RC318' : 'C115253',
                'benzene' : 'C71432',
                'toluene' : 'C108883',
                'decafluorobutane' : 'C355259',
                'dodecafluoropentane' : 'C678262',
                'sulfur_dioxide' : 'C7446095',
                'hydrogen_sulfide' : 'C7783064',
                'sulfur_hexafluoride' : 'C2551624',
                'carbonyl_sulfide' : 'C463581',
                }

def Read_Params_CSV():
    log = ""
    filename = "NIST Extractor Config File.xlsx"
    try:
        params = read_excel("NIST Extractor Config File.xlsx").drop(columns=["Unnamed: 2", "Unnamed: 3"])
        for index, row in params.iterrows():
            if isna(row["Unit"]) and index != 0 and index != 8:
                log += f'{ctime()} - Error - Please ensure the config file has values against all required fields: {os.getcwd()}\\{filename}\n'
                log += f"{ctime()} - Params used:\n{params["Unit"].loc[0:15].to_string(index=False)}\n"
                print(log)
                return log

        return params

    except:
        log += f'Error - Could not find config file, please ensure file is named and located in the directory as shown: {os.getcwd()}\\{filename}\n'
        print(log)
        return log


def Generate_NIST_Refs(params):

    units_selected =[]
    default_units = ["K", "bar", "kg%2Fm3", "kJ%2Fkg", "m%2Fs", "Pa*s", "N%2Fm"]
    units_selected.append(Fluids_ID[params["Unit"].loc[0]])
    for i in range(1, 8):
        #print(params.loc[i])
        if params.loc[i]["Unit"] != "":
            units_selected.append(params.loc[i]["Unit"].replace("/", "%2F").replace("^", ""))
        else:
            units_selected.append(default_units[i])
    for i in range(8, 16):
        units_selected.append(params.loc[i]["Unit"])

    params["NIST Refs"] = units_selected

    return params


def getNIST(params):
    log = ""
    Tlow = params["Unit"].loc[13]
    Thigh = params["Unit"].loc[14]
    deltaT = params["Unit"].loc[15]
    data_list = []
    loading_bar = []

    if Tlow == Thigh:
        temp_count = 1

    else:
        temp_count = int((float(Thigh)-float(Tlow))/float(deltaT)) + 1
    log += f"Generating data for {params["Unit"].loc[0]}:\n"
    log += f"{temp_count} temperature point(s) from {params["Unit"].loc[13]} {params["Unit"].loc[1]} to {params["Unit"].loc[14]} {params["Unit"].loc[1]}\n"
    log += f"{int((float(params["Unit"].loc[11])-float(params["Unit"].loc[10]))/float(params["Unit"].loc[12])) + 1} pressure point(s) from {params["Unit"].loc[10]} {params["Unit"].loc[2]} to {params["Unit"].loc[11]} {params["Unit"].loc[2]}\n"
    log += f"Using units:\n{params["Unit"].loc[1:7].to_string(index=False)}\n"
    print(log)

    for i in range(temp_count):
        loading_bar.append("_")

    for i in range(temp_count):
        loading_bar[i] = "X"
        print("".join(loading_bar), end="")

        Temp = str(float(Tlow) + (float(deltaT)*i))

        try:
            data = getFromNIST_isoTherm(params, Temp)
            if type(data) == str:
                raise Exception

            data_list.append(data)
            print("", end="\r")

        except:
            log += "Error - Please specify parameters correctly\n"
            if type(data) == str:
                log += f"Source link used: {data}\n"
            print(log)
            return log

    collated_data = concat(data_list)

    return collated_data


def getFromNIST_isoTherm(params, Temp, TypeOfData="IsoTherm", Digits = '5'):

    source_link = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
                   + str(params["NIST Refs"].loc[0])
                   + '&Type='+ str(TypeOfData)
                   + '&Digits='+ str(Digits)
                   + '&PLow=' + str(params["NIST Refs"].loc[10])
                   + '&PHigh=' + str(params["NIST Refs"].loc[11])
                   + '&PInc=' + str(params["NIST Refs"].loc[12])
                   + '&T=' + str(Temp)
                   + '&RefState=DEF&TUnit='+ str(params["NIST Refs"].loc[1])
                   + '&PUnit=' + str(params["NIST Refs"].loc[2])
                   + '&DUnit='+ str(params["NIST Refs"].loc[3])
                   + '&HUnit='+ str(params["NIST Refs"].loc[4])
                   + '&WUnit='+ str(params["NIST Refs"].loc[5])
                   + '&VisUnit='+ str(params["NIST Refs"].loc[6])
                   + '&STUnit=' + str(params["NIST Refs"].loc[7]))

    try:
        request  = (source_link)
        data = read_csv(request, delimiter='\t')
        source_links = []
        for i in range(len(data)):
            source_links.append(source_link)
        data["Source"] = source_links
        return data

    except:
        return source_link

def Generate_CSV(collated_data, params):
    log = ""
    i=0
    if os.path.isfile(f"{params["Unit"].loc[0]} data.csv"):
        while True:
            i+=1
            if not os.path.isfile(f"{params["Unit"].loc[0]} data {i}.csv"):
                filename = f"{params["Unit"].loc[0]} data {i}.csv"
                break
            else:
                pass
    else:
        filename = f"{params["Unit"].loc[0]} data.csv"
    collated_data.to_csv(filename, index=False)
    log += f"File generated: {os.getcwd()}\\{filename}\n"
    print(log)
    return log


if __name__ == '__main__':
    with open("Log.txt", "a") as log_file:

        log_file.write(f"\n{ctime()} - Starting script\n")
        log_file.write(f"{ctime()} - Reading config file\n")
        params = Read_Params_CSV()

        if type(params) == str:
            log_file.write(f"{params} ")
            exit()

        else:
            params = Generate_NIST_Refs(params)
            collated_data = getNIST(params)
            log_file.write(f"{ctime()} - Downloading data from NIST\n")

            if type(collated_data) == str:
                log_file.write(f"{ctime()} - {collated_data} ")
                exit()

            else:
                log = Generate_CSV(collated_data, params)
                log_file.write(f"{ctime()} - {log}")

