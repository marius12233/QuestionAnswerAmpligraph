import pandas as pd

def merge_csv(pattern_path, dep_path, dest_path):
    df_pattern = pd.read_csv(pattern_path, names=["subj","rel","obj"])
    df_dep = pd.read_csv(dep_path)
    print("========= DEP ========")
    print(df_dep.head())
    print("========= PATTERN ========")
    print(df_pattern.head())
    df_dest=pd.concat([df_pattern, df_dep], ignore_index=True, sort=False)
    df_dest.to_csv(dest_path, index=False)

if __name__=="__main__":
    print("Merging csv...")
    merge_csv("Triple/pattern_triples.csv", "Triple/dep_triples.csv","Triple/complete_triples.csv")
