matrix(c(1:6))

matrix (c(1:10), nrow =2)

matrix (c(1:10), ncol =2)

matrix(c(1:10), ncol=2, byrow = T)

x1 = c(5,40, 50:52)
x2 <- c(30, 6:9)
x2
m5 <- cbind(x1, x2)
m5*3

m6 <- matrix(c(1,"hong", 150,
               2, "lee", 250,
               3, "kim", 350), 3, by=T)

m6

df_matdata <- data.frame(m6)
df_matdata

df_vector <- data.frame(hakbun=c(1:3), name=c('kim', 'lee', 'park'))
df_vector

write.csv(df_vector, file = 'test.csv')
saveRDS(df_vector, file = 'test.rds')

readRDS('test.rds')
