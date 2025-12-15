
#Function
cell_viability_percent<- function(mean_healthy, mean_toxic, experiment_data){
  answer<- ((experiment_data- mean_toxic)/ (mean_healthy- mean_toxic))* 100
  return(answer)
}

#Controls
blank<- c(66, 65, 65)
healthy<- c(28738, 24715, 30261)
toxic<- c(13087, 10615, 12752)

#Blanked Controls
blank_mean<- mean(blank)
b_blank<- blank- blank_mean
b_healthy<- healthy- blank_mean
b_toxic<- toxic- blank_mean

#means 
healthy_mean<- mean(b_healthy)
toxic_mean<- mean(b_toxic)


#Trials
new_100<- c(38576, 35485, 38397)
new_50<- c(28825, 33041, 39753)
old_100<- c(19673, 23230, 25401)
old_50<- c(21609, 27072, 32033)
tega_100<- c(21483, 25850, 19889)
tega_50<- c(33366, 24087, 23926)

new_on<- c(15768, 14846, 18930)
old_on<- c(17937, 20507, 20205)
tega_on<- c(18353, 21477, 21033)

#Blanked Trials
b_new_100<- new_100- blank_mean
b_new_50<- new_50- blank_mean
b_old_100<- old_100- blank_mean
b_old_50<- old_50- blank_mean 
b_tega_100<- tega_100- blank_mean
b_tega_50<- tega_50- blank_mean

b_new_on<- new_on- blank_mean
b_old_on<- old_on- blank_mean
b_tega_on<- tega_on- blank_mean

#Viability 
v_healthy<- cell_viability_percent(healthy_mean, toxic_mean, healthy)
v_toxic<- cell_viability_percent(healthy_mean, toxic_mean, toxic)
v_new_100<- cell_viability_percent(healthy_mean, toxic_mean, b_new_100) 
v_new_50<- cell_viability_percent(healthy_mean, toxic_mean, b_new_50)
v_old_100<- cell_viability_percent(healthy_mean, toxic_mean, b_old_100)
v_old_50<- cell_viability_percent(healthy_mean, toxic_mean, b_old_50)
v_tega_100<- cell_viability_percent(healthy_mean, toxic_mean, b_tega_100)
v_tega_50<- cell_viability_percent(healthy_mean, toxic_mean, b_tega_50)

#v_new_on<- cell_viability_percent(healthy_mean, toxic_mean, b_new_on)
#v_old_on<- cell_viability_percent(healthy_mean, toxic_mean, b_old_on)
#v_tega_on<- cell_viability_percent(healthy_mean, toxic_mean, b_tega_on)

#Data
library(car)
viability<- data.frame(value= c(v_new_100, v_new_50, v_old_100, v_old_50, v_tega_100, v_tega_50, v_healthy, v_toxic), group= rep(c("New_Mesh_100", "New_Mesh_50", "Old_Mesh_100", "Old_Mesh_50", "Tegaderm_100", "Tegaderm_50", "Healthy", "Toxic"), each= 3))

alpha<- c(0.01)

#Normality
normality_healthy<-shapiro.test(healthy) #p-value: 0.5137
normality_toxic<-shapiro.test(toxic) #p-value: 0.2392
normality_v_new_100<-shapiro.test(v_new_100) #p-value: 0.9855
normality_v_new_50<-shapiro.test(v_new_50) #p-value: 0.7496
normality_v_old_100<-shapiro.test(v_old_100) #p-value: 0.7349
normality_v_old_50<-shapiro.test(v_old_50) #p-value: 0.9469
normality_v_tega_100<-shapiro.test(v_tega_100) #p-value: 0.4989
normality_v_tega_50<-shapiro.test(v_tega_50) #p-value: 0.02845

#normality_v_new_on<-shapiro.test(v_new_on) #p-value: 0.4143
#normality_v_old_on<-shapiro.test(v_old_on) #p-value: 0.2057
#normality_v_tega_on<-shapiro.test(v_tega_on) #p-value: 0.2516

#Variance
leveneTest(value~group, data= viability) #p-value: 0.8407

#Unpaired T-test
t_new_100<- t.test(v_new_100, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.996
t_new_50<- t.test(v_new_50, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.9124
t_old_100<- t.test(v_old_100, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.04565 
t_old_50<- t.test(v_old_50, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.386
t_tega_100<- t.test(v_tega_100, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.04203
t_tega_50<- t.test(v_tega_50, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.4115  

#t_new_on<- t.test(v_new_on, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.002585
#t_old_on<- t.test(v_old_on, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.00513
#t_tega_on<- t.test(v_tega_on, v_healthy, alternative= "less", var.equal= TRUE) #p-value: 0.008066 

#T-test p-value
p_value<- c(t_new_100$p.value, t_new_50$p.value, t_old_100$p.value, t_old_50$p.value, t_tega_100$p.value, t_tega_50$p.value)
new_p_values<- p.adjust(p_value, method= "bonferroni")


################
# Install if not already installed
# install.packages("ggplot2")
library(ggplot2)
library(dplyr)

# Compute means for each group
group_means <- viability %>%
  group_by(group) %>%
  summarise(mean_value = mean(value))

# Create x-axis labels: group name + mean
mean_labels <- paste0(group_means$group, "\nMean: ", round(group_means$mean_value,1))

# Scatter plot with jittered points, mean, SD bars, and mean in x-axis
ggplot(viability, aes(x = group, y = value)) +
  geom_jitter(width = 0.2, size = 3, alpha = 0.7, color = "blue") +  # individual replicates
  stat_summary(fun = mean, geom = "point", shape = 18, size = 5, color = "red") +  # mean point
  stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1),
               geom = "errorbar", width = 0.2, color = "black") +  # SD bars
  scale_x_discrete(labels = mean_labels) +  # x-axis labels with mean
  labs(title = "Cell Viability",
       x = "",
       y = "Viability (%)") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.5, color = "black"),
    axis.text.y = element_text(color = "black"),
    plot.title = element_text(hjust = 0.5, face = "bold")
  )

