import io

from pandas import read_csv
import requests

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
                'cyclopropane' : 'C75194',
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


if __name__ == '__main__':

    for key, value in Fluids_ID.items():

        try:
            print(f"\nTesting {key} - {value}")
            source_link = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
                           + str(value)
                           + '&Type=' + "IsoTherm"
                           + '&Digits=' + "5"
                           + '&PLow=' + "10"
                           + '&PHigh=' + "11"
                           + '&PInc=' + "1"
                           + '&T=' + "200"
                           + "RefState=DEF&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=Pa*s&STUnit=N%2Fm")
            text = (source_link)
            print(text)
            response = requests.get(source_link).text
            response_type = type(requests)
            #print(f"Response type = {response_type}")
            #print(f"Response text = {text}")
            print("Here")
            data = read_csv(io.StringIO(response), delimiter='\t')
            print("Here2")

            #print(f"Formatted data = {data}")
            #print()
            #print(type(data))
            print(data.loc[0])
            if "Exception" in data.loc[0]:
                print(f"Data at loc[0] = {data.loc[0]}")
                raise Exception

        except:
            if "Range" in response:

                print(response)
                print(source_link)