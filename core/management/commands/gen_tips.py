from django.core.management.base import BaseCommand, CommandError
from core.models import TipOfDay

import json
import os


def write_json(intRange,strFileName):
    # creates a json file in format
    # {int number: Tip #number}
    with open('{}.py'.format(strFileName),'w') as f:
        f.write('listDictTips = [\n')
        for i in range(intRange-1):
            f.write(
                '{\'text\':' + "\'Tip {}\',\n".format(i)
                + '\'day_number\':{},\n'.format(i)
                + '},\n'
            )
        f.write(
                '{\'text\':' + "\'Tip {}\',\n".format(i)
                + '\'day_number\':{},\n'.format(i)
                + '}\n]'
        )

#write_json(366,'tips')

class Command(BaseCommand):
    'creates tip objects'
    def handle(self,**options):
        from .tips import listDictTips
        for jsonTip in listDictTips:
            TipOfDay.objects.create(**jsonTip)

