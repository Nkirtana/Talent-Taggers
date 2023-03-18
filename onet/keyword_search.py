from .OnetWebService import OnetWebService

import pandas as pd
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.abspath(os.path.join(basedir, os.pardir))
skill_path = os.path.join(parent_path, 'skilldb', 'all_skills.csv')
print(skill_path)


class Onet:

    @staticmethod
    def update_skills_csv():
        username = 'research_on_resume_k'
        password = '5249vbi'
        onet_ws = OnetWebService(username, password)

        vinfo = onet_ws.call('about')
        # check_for_error(vinfo)
        if 'error' in vinfo:
            return 'Error: {}'.format(vinfo['error'])

        print("Connected to O*NET Web Services version " + str(vinfo['api_version']))
        print("")

        # kwquery = get_user_input('Keyword search query')
        kwquery = 'sort=name'
        kwresults = onet_ws.call('mnm/careers/',
                                 ('keyword', kwquery),
                                 ('start', 1),
                                 ('end', 1000))

        codes = []
        # total = kwresults['total']

        if 'career' in kwresults:
            for career in kwresults['career']:
                codes.append(career['code'])

        head_tech = []
        # abilities = []
        skills = []
        personalities = []
        # Only run on few codes for testing, it will take long time for this to run
        for code in codes:
            head_tech.append(onet_ws.call('mnm/careers/' + code + '/technology'))
            # abilities.append(onet_ws.call('mnm/careers/'+code+'/abilities'))
            skills.append(onet_ws.call('mnm/careers/' + code + '/skills'))
            personalities.append(onet_ws.call('mnm/careers/' + code + '/personality'))

        technology = []
        remaining = []
        for tech in head_tech:
            if 'category' in tech:
                for example in tech['category']:
                    if 'example' in example:
                        for t in example['example']:
                            if 'name' in t:
                                technology.append(t['name'])
                    else:
                        remaining.append(example)

        personality = []
        for p in personalities:
            if 'work_styles' in p:
                for i in p['work_styles']['element']:
                    personality.append(i['name'])

        personality = list(set(personality))

        # skills
        skill = []
        for s in skills:
            if 'group' in s:
                for i in s['group']:
                    skill.append(i['title']['name'])

        skill = list(set(skill))

        # Appending all skills together in a single list
        final_list = technology + skill + personality

        # Reading existing skills csv
        skill_csv = pd.read_csv(skill_path)
        skill_csv_list = skill_csv['skill_name'].tolist()
        len_skills_csv = len(skill_csv_list)

        # Check Onet skills in existing file; if not add them
        for i in final_list:
            if i not in skill_csv_list:
                skill_csv_list.append(i)

        # Checking if any updation in existing skills file and replace
        if len_skills_csv != len(skill_csv_list):
            # Renaming the previous skills db and saving it for future reference
            current_time = datetime.datetime.now()
            time_stamp = current_time.timestamp()
            os.rename(skill_path, os.path.join(parent_path, 'skilldb', str(time_stamp)+'.csv'))

            df = pd.DataFrame(skill_csv_list, columns=['skill_name'])
            df.to_csv(skill_path, index=False)
            return 'File has been successfully updated'
        else:
            return 'File up-to-date!'
