cd data
mkdir d02_intermediate
mkdir d03_cleaned_data
bash datacleaning.py
bash mergedata.py
bash create_ddb.py
gnome-terminal -e [streamlit run app/app.py]
uvicorn app.api:app --reload
