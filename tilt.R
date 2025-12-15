
#Trials
zero<- c(0.0000002, 0.0001, 0.0)
fifteen<- c(13.650, 13.787, 14.220)
thirty<- c(30.505, 29.993, 29.887)
fourty_five<- c(46.030, 46.607, 46.599)
sixty<- c(62.210, 62.442, 61.911)
ninety<- c(91.131, 91.701, 91.176)


zero_1<- c(0.0000002, 0.0001, 0.0)
fifteen_1<- c(14.392, 14.286, 14.682)
thirty_1<- c(30.018, 30.022, 30.453)
fourty_five_1<- c(45.647, 45.401, 45.902)
sixty_1<- c(62.925, 62.530, 62.065)
ninety_1<- c(91.533, 91.765, 91.476)


zero_2<- c(0.0000002, 0.0001, 0.0)
fifteen_2<- c(13.508, 13.791, 14.560)
thirty_2<- c(30.533, 29.818, 30.159)
fourty_five_2<- c(45.585, 46.328, 46.496)
sixty_2<- c(61.843, 62.219, 61.742)
ninety_2<- c(90.940, 91.609, 90.715)


zero_mean<- mean(zero)
fifteen_mean<- mean(fifteen)
thirty_mean<- mean(thirty)
fourty_five_mean<- mean(fourty_five)
sixty_mean<- mean(sixty)
ninety_mean<- mean(ninety)


zero_1_mean<- mean(zero_1)
fifteen_1_mean<- mean(fifteen_1)
thirty_1_mean<- mean(thirty_1)
fourty_five_1_mean<- mean(fourty_five_1)
sixty_1_mean<- mean(sixty_1)
ninety_1_mean<- mean(ninety_1)


zero_2_mean<- mean(zero_2)
fifteen_2_mean<- mean(fifteen_2)
thirty_2_mean<- mean(thirty_2)
fourty_five_2_mean<- mean(fourty_five_2)
sixty_2_mean<- mean(sixty_2)
ninety_2_mean<- mean(ninety_2)


zero_sd<- sd(zero)
fifteen_sd<- sd(fifteen)
thirty_sd<- sd(thirty)
fourty_five_sd<- sd(fourty_five)
sixty_sd<- sd(sixty)
ninety_sd<- sd(ninety)


zero_1_sd<- sd(zero_1)
fiften_1_sd<- sd(fifteen_1)
thirty_1_sd<- sd(thirty_1)
fourty_five_1_sd<- sd(fourty_five_1)
sixty_1_sd<- sd(sixty_1)
ninety_1_sd<- sd(ninety_1)


zero_2_sd<- sd(zero_2)
fifteen_2_sd<- sd(fifteen_2)
thirty_2_sd<- sd(thirty_2)
fourty_five_2_sd<- sd(fourty_five_2)
sixty_2_sd<- sd(sixty_2)
ninety_2_sd<- sd(ninety_2)

#Total Data
o0<- c(zero_mean, zero_1_mean, zero_2_mean)
o15<- c(fifteen_mean, fifteen_1_mean, fifteen_2_mean)
o30<- c(thirty_mean, thirty_1_mean, thirty_2_mean)
o45<- c(fourty_five_mean, fourty_five_1_mean, fourty_five_2_mean)
o60<- c(sixty_mean, sixty_1_mean, sixty_2_mean)
o90<- c(ninety_mean, ninety_1_mean, ninety_2_mean)

angles<- c(0, 15, 30, 45, 60, 90)
angles_total<- rep(angles, each= 3) 
angles_measured<- c(o0, o15, o30, o45, o60, o90)

#Putting them into a data frame
v<- data.frame(rbind(o0, o15, o30, o45, o60, o90))
colnames(v)<- c("Trial #1", "Trial #2", "Trial #3")
rownames(v)<- c("0-deg", "15-deg", "30-deg", "45-deg", "60-deg", "90-deg")


#Statistical Analysis
v$mean<- rowMeans(v[, 1:3]) #mean
v$sd<- apply(v[, 1:3], 1, sd) #standard deviation
v$std_err<- v$sd/ sqrt(3) #standard error
v$per_err<- abs((v$mean- angles)/ angles) #percent error


linear_fit<- lm(angles_measured ~ angles_total) #get the linear fit
summarizing<- summary(linear_fit)

library(ggplot2)
library(dplyr)

# -------------------------
# RAW TRIAL SETS
# -------------------------

set0  <- list(c(0.0000002, 0.0001, 0.0),
              c(0.0000002, 0.0001, 0.0),
              c(0.0000002, 0.0001, 0.0))

set15 <- list(c(13.650, 13.787, 14.220),
              c(14.392, 14.286, 14.682),
              c(13.508, 13.791, 14.560))

set30 <- list(c(30.505, 29.993, 29.887),
              c(30.018, 30.022, 30.453),
              c(30.533, 29.818, 30.159))

set45 <- list(c(46.030, 46.607, 46.599),
              c(45.647, 45.401, 45.902),
              c(45.585, 46.328, 46.496))

set60 <- list(c(62.210, 62.442, 61.911),
              c(62.925, 62.530, 62.065),
              c(61.843, 62.219, 61.742))

set90 <- list(c(91.131, 91.701, 91.176),
              c(91.533, 91.765, 91.476),
              c(90.940, 91.609, 90.715))

all_sets <- list(set0, set15, set30, set45, set60, set90)
angles   <- c(0, 15, 30, 45, 60, 90)

# ----------------------------------------
# Build full raw dataframe of all readings
# ----------------------------------------

angles_measured <- unlist(all_sets)
angles_total    <- rep(angles, each=9)  # 3 trials × 3 repeats = 9

df <- data.frame(
  Actual   = angles_total,
  Measured = angles_measured
)

# ----------------------------------------
# Summary statistics (mean & SD per angle)
# ----------------------------------------

summary_df <- df %>%
  group_by(Actual) %>%
  summarise(
    Mean = mean(Measured),
    SD   = sd(Measured)
  )

# ----------------------------------------
# Regression
# ----------------------------------------

linear_fit <- lm(Measured ~ Actual, data=df)
coef_vals  <- coef(linear_fit)

slope  <- round(coef_vals[2], 4)
interc <- round(coef_vals[1], 4)
r2     <- round(summary(linear_fit)$r.squared, 4)

eq_label <- paste0("y = ", slope, "x + ", interc)
r2_label <- paste0("R² = ", r2)

# ----------------------------------------
# FINAL PLOT
# ----------------------------------------
library(ggplot2)
library(ggplot2)

ggplot() +
  
  # Raw data points (red)
  geom_jitter(data=df, aes(x=Actual, y=Measured),
              width=0.2, height=0, color="#FF0000", size=3, alpha=0.7) +
  
  # Linear fit (red line)
  geom_smooth(data=df,
              aes(x=Actual, y=Measured),
              method="lm", se=FALSE,
              color="#FF0000", size=1.5) +
  
  # Mean points (black) with error bars
  geom_point(data=summary_df,
             aes(x=Actual, y=Mean),
             color="black", size=4) +
  geom_errorbar(data=summary_df,
                aes(x=Actual, ymin=Mean-SD, ymax=Mean+SD),
                width=0.3, color="black", size=1.2) +
  
  # Annotation for equation and R²
  annotate("label",
           x = min(df$Actual), 
           y = max(df$Measured),
           label = paste0(eq_label, "\n", r2_label),
           hjust = 0, vjust = 1,
           size = 5, fontface="bold", fill="white", color="black") +
  
  # Labels with degree symbol
  labs(title="Measured vs Actual Angle",
       x="Actual Angle (\u00B0)",
       y="Measured Angle (\u00B0)") +
  
  # Poster-ready theme
  theme_minimal(base_size = 16) +
  theme(
    plot.title = element_text(size=20, face="bold", hjust=0.5),
    axis.title = element_text(size=18, face="bold"),
    axis.text = element_text(size=14)
  )
