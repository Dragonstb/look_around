from pathlib import Path
from run import run_gen
import pandas as pd
from dev_tools.sample_gen import SampleGen as SG


def create_dev_project(size: int, name: str, parent: Path):
    prj = run_gen.create_project_folders(name, parent)
    sg = SG()
    cols = []
    file_data = []
    successes = 0
    train_dir = Path(prj.root_dir, prj.train_dir).absolute()
    print('writing to '+str(train_dir))

    for _ in range(size):
        # generate labeled sample
        sg.new_req(print_ranking=False, print_req=False)
        # extract data from sample
        html = sg.get_req()
        rating = sg.get_rating()
        id = prj.create_sample_id()
        sub_path = Path(id['path'] + '-raw.html')
        sub_dir = Path(train_dir, id['dir'])

        # write html file to disc
        full_path = Path(train_dir, sub_path)
        sub_dir.mkdir(exist_ok=True, parents=True)
        try:
            with open(full_path, 'wt', ) as file:
                file.write(html)
                ok = True
        except BaseException as be:
            print(be)
            ok = False

        # add to data collection if wtiting has succeeded
        if ok:
            dic = {
                'raw file': str(sub_path),
                'origin': 'req_gen',
                'rating': rating,
                'labeled by': 'alg_cat'
            }
            df = pd.DataFrame(dic, index=[id['id']])
            file_data.append(df)
            successes += 1

    print(f'wrote {successes} out of {size} files successfully')
    if len(file_data) > 0:
        file_data = pd.concat(file_data)
        file_data.to_csv(Path(prj.train_dir, 'document_index.csv'), index=True)
        print(file_data)
