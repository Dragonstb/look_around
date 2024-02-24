from pathlib import Path
from look_around.run import run_gen
import pandas as pd
from look_around.dev_tools.sample_gen import SampleGen as SG
from look_around.doc_process import html_cleaning, stops_removal, stemming, vocab_extraction
from sklearn.model_selection import train_test_split


def create_dev_project(size: int, name: str, parent: Path):
    prj = run_gen.create_project_folders(name, parent)
    sg = SG()
    cols = []
    file_data = []
    docs = []
    successes = 0
    train_dir = Path(prj.root_dir, prj.train_dir).absolute()
    print('writing to '+str(train_dir))

    for _ in range(size):
        lang = 'english'
        # generate labeled sample
        sg.new_req(print_ranking=False, print_req=False)

        # extract data from sample
        html = sg.get_req()
        rating = sg.get_rating()
        id = prj.create_sample_id()
        raw_sub_path = Path(id['path'] + '-raw.html')
        prep_sub_path = Path(id['path'] + '-cleaned.txt')
        sub_dir = Path(train_dir, id['dir'])

        # write html file to disc
        full_path = Path(train_dir, raw_sub_path)
        sub_dir.mkdir(exist_ok=True, parents=True)
        try:
            with open(full_path, 'wt') as file:
                file.write(html)
                ok = True
        except BaseException as be:
            print(be)
            ok = False

        # generate preprocessed and prepared document
        prepared = html_cleaning.clean_html(html)
        prepared = stops_removal.remove_stop_words(prepared, lang=lang)
        prepared = stemming.stem(prepared, lang=lang)
        full_path = Path(train_dir, prep_sub_path)
        try:
            with open(full_path, 'wt') as file:
                file.write(prepared)
                docs.append(prepared)
        except BaseException as be:
            print(be)
            prep_sub_path = pd.NA  # write NA instead of the sub path

        # add to data collection if writing has succeeded
        if ok:
            dic = {
                'raw file': str(raw_sub_path),
                'prepared file': str(prep_sub_path),
                'origin': 'req_gen',
                'language': lang,
                'rating': rating,
                'labeled by': 'alg_cat'
            }
            df = pd.DataFrame(dic, index=[id['id']])
            file_data.append(df)
            successes += 1

    print(f'wrote {successes} out of {size} files successfully')

    if len(file_data) < 1:
        return

    # concat to single data frame
    file_data = pd.concat(file_data)

    # determine two vocabulary
    print('number of docs: '+str(len(docs)))
    vocab1 = vocab_extraction.extract_vocab(docs, min_df=3)
    vocab2 = vocab_extraction.extract_vocab(docs, min_df=3, ngram_range=(2, 2))

    # split to training data and test data
    clean = file_data.dropna()
    train, test = train_test_split(
        clean.index, test_size=0.2, stratify=clean['rating'])
    file_data.loc[train, 'usage'] = 'train'
    file_data.loc[test, 'usage'] = 'test'

    # out
    file_data.to_csv(Path(prj.train_dir, 'document_index.csv'), index=True)
    print()
    print(file_data)

    prj.write_vocab(vocab1, 'vocab_monograms')
    print()
    print('monogram vocabulary:')
    print(vocab1)
    prj.write_vocab(vocab2, 'vocab_bigrams')
    print()
    print('bigram vocabulary:')
    print(vocab2)
