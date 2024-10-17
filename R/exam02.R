resno <- c(101, 102, 103, 104, 105)
rname <- c('ANDREA', 'NY', 'YANIS', 'CLEVETH', 'ASHIYA')
rage <- c('51', '23', '52', '76', '98')

resident <- data.frame(resno, rname, rage)
install.packages("readxl")
library(readxl)

df_exam <- read_excel("C:/RPAWork/workspace/R/csv_exam.csv")
df_exam2 <- read_excel("C:/RPAWork/workspace/python/_종목_하락순_정렬.xlsx")
df_exam3 <- read_excel("C:/RPAWork/workspace/R/Data/excel_exam.xlsx")
print(apply(df_exam3,2,mean))

df_exam4 <- read.csv("C:/RPAWork/workspace/R/Data/csv_exam.txt", header=TRUE, skip=1)
print(df_exam4)


