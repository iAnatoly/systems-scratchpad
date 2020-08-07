import readability
from pprint import pprint


def wcm(text):
    results = readability.getmeasures(text, lang='en')
    grades = results['readability grades']
    print(text, grades['ARI']) #, grades['GunningFogIndex'])
    # pprint(results)
    return 0

wcm('voice')
wcm('communications')
wcm('elevate')
wcm('elevateportal')


