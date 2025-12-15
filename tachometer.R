
#--Trials
rpm_00<- c(00.0, 00.0, 00.0)
rpm_10<- c(10.0, 10.1, 09.9)
rpm_15<- c(15.0, 15.0, 14.8)
rpm_20<- c(20.0, 20.0, 20.5)
rpm_25<- c(25.0, 25.2, 25.0)
rpm_30<- c(29.5, 29.3, 29.2)
rpm_35<- c(34.6, 34.7, 34.9)
rpm_40<- c(40.6, 40.0, 39.2)
rpm_45<- c(44.5, 45.0, 44.2)
rpm_50<- c(49.2, 50.5, 49.8)
rpm_55<- c(54.0, 55.0, 53.4)
rpm_60<- c(59.8, 59.3, 60.7)
rpms<- c(0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
rpm_actual<- rep(rpms, each= 3)
rpm_measured<- c(rpm_00, rpm_10, rpm_15, rpm_20, rpm_25, rpm_30, rpm_35, rpm_40, rpm_45, rpm_50, rpm_55, rpm_60)
  
#Putting them into a data frame
v<- data.frame(rbind(rpm_00, rpm_10, rpm_15, rpm_20, rpm_25, rpm_30, rpm_35, rpm_40, rpm_45, rpm_50, rpm_55, rpm_60))
colnames(v)<- c("Trial #1", "Trial #2", "Trial #3")
rownames(v)<- c("RPM 00", "RPM 10", "RPM 15", "RPM20", "RPM 25", "RPM 30", "RPM 35", "RPM 40", "RPM 45", "RPM 50", "RPM 55", "RPM 60")


#Statistical Analysis
v$mean<- rowMeans(v[, 1:3]) #mean
v$sd<- apply(v[, 1:3], 1, sd) #standard deviation
v$std_err<- v$sd/ sqrt(length(rpm_30)) #standard error
v$per_err<- abs((v$mean- rpms)/ rpms) #percent error


linear_fit<- lm(rpm_measured ~ rpm_actual) #get the linear fit
summarizing<- summary(linear_fit)

## Transfer
write_xlsx(
  list(
    "RPM_Data" = v,
  ),
  "rpm_analysis.xlsx"
)


library(ggplot2)
library(ggplot2)

# Data frame for plotting
df_plot <- data.frame(
  rpm_set = rpms,
  mean    = v$mean,
  sd      = v$sd
)

# Linear fit predictions
fit_line <- data.frame(
  rpm_set = rpms,
  pred = predict(linear_fit, newdata = data.frame(rpm_actual = rpms))
)

# Poster-ready plot
ggplot() +
  
  # Raw measured points (red)
  geom_jitter(data=df_plot, aes(x=rpm_set, y=mean),
              width=0.2, height=0, color="#FF0000", size=3, alpha=0.7) +
  
  # Linear fit (red line)
  geom_line(data=fit_line, aes(x=rpm_set, y=pred),
            color="#FF0000", size=1.5) +
  
  # Mean points (black) with error bars
  geom_point(data=df_plot, aes(x=rpm_set, y=mean),
             color="black", size=4) +
  geom_errorbar(data=df_plot,
                aes(x=rpm_set, ymin=mean - sd, ymax=mean + sd),
                width=1, color="black", size=1.2) +
  
  # Labels
  labs(
    title = "Measured RPM vs Set RPM",
    x = "Set RPM",
    y = "Measured RPM"
  ) +
  
  # Minimal, poster-friendly theme
  theme_minimal(base_size = 16) +
  theme(
    text = element_text(family = "Times New Roman", face = "bold"),
    plot.title = element_text(size=26, hjust=0.5),
    axis.title = element_text(size=22),
    axis.text = element_text(size=18)
  )

