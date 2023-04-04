import pandas as pd
import os
import datetime

def updateSkills():
        ##REading skills obtained from guided BERTopic
        basedir = os.path.abspath(os.path.dirname(__file__))
        guided_skill_path = os.path.join(basedir, 'Data', 'guided_skills.csv')
        skill_path = os.path.join(basedir, 'skilldb', 'all_skills.csv')

        df_guided = pd.read_csv(guided_skill_path,index_col=False)

        ##Filtering Skills
        df_guided = df_guided[df_guided['YesOrNo']=='Y']
        df_guided.reset_index()
        guided_skill_list = df_guided['skill'].tolist()

        ##REading static db skills

        df_skills = pd.read_csv(skill_path,index_col=False)

        skill_csv_list = df_skills['skill_name'].tolist()
        len_skills_csv = len(skill_csv_list)

        # Check Guided Topic modeling skills in existing file; if not add them
        for i in guided_skill_list:
            if i not in skill_csv_list:
                        skill_csv_list.append(i)

        # Checking if any updation in existing skills file and replace
        if len_skills_csv != len(skill_csv_list):
                    # Renaming the previous skills db and saving it for future reference
                    current_time = datetime.datetime.now()
                    time_stamp = current_time.timestamp()
                    os.rename(skill_path, os.path.join(basedir, 'skilldb', str(time_stamp)+'.csv'))

                    df = pd.DataFrame(skill_csv_list, columns=['skill_name'])
                    df.to_csv(skill_path, index=False)
                    return 'File has been successfully updated'
        else:
                    return 'File up-to-date!'


updateSkills()