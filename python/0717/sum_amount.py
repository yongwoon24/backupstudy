import pandas as pd
file_name = '20240717_코스피_종목_거래량순_정렬.xlsx'
file_path = 'C:\\RPAWork\\workspace\\python\\' + file_name
sheet_Name = 'Sheet1'

df_read = pd.read_excel(file_path, sheet_name=sheet_Name)
column_name = '거래량' 

df_read[column_name] = df_read[column_name].replace({',': ''}, regex=True).astype(int)
column_sum = df_read[column_name].sum()
#print(f"{column_name} 열의 합계: {column_sum}")
df_write = pd.DataFrame([column_sum], columns=['총 거래량'])
df_write.to_excel(file_name[0:8]+'_거래량_총합.xlsx', index=False)