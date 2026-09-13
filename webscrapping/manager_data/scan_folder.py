from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

def get_all_files() :
    '''Сканируем папку и возвращаем список файлов'''
    if not RESULTS_DIR.exists() :
        RESULTS_DIR.mkdir(parents=True,exist_ok=True)
    files = [file.stem for file in RESULTS_DIR.glob("*-dictionarys.json") ]
    return files

if __name__ == "__main__" :
    print(get_all_files())



                
                
                