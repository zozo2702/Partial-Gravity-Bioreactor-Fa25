library(ggplot2)
library(patchwork)

# -------------------
# RPM Data Preparation
# -------------------
rpm_df <- data.frame(
  rpm_actual = rep(rpms, each = 3),
  rpm_measured = c(rpm_00, rpm_10, rpm_15, rpm_20, rpm_25, rpm_30,
                   rpm_35, rpm_40, rpm_45, rpm_50, rpm_55, rpm_60)
)

rpm_stats <- data.frame(
  rpm_set = rpms,
  mean = sapply(list(rpm_00, rpm_10, rpm_15, rpm_20, rpm_25, rpm_30,
                     rpm_35, rpm_40, rpm_45, rpm_50, rpm_55, rpm_60), mean),
  sd = sapply(list(rpm_00, rpm_10, rpm_15, rpm_20, rpm_25, rpm_30,
                   rpm_35, rpm_40, rpm_45, rpm_50, rpm_55, rpm_60), sd)
)

rpm_fit <- lm(rpm_measured ~ rpm_actual, data = rpm_df)
rpm_eq <- paste0("y = ", round(coef(rpm_fit)[2], 2), "x + ", round(coef(rpm_fit)[1], 2),
                 "\nR² = ", round(summary(rpm_fit)$r.squared, 3))

# -------------------
# Tilt Data Preparation
# -------------------
tilt_df <- data.frame(
  angle_actual = rep(angles, each = 3),
  angle_measured = c(o0, o15, o30, o45, o60, o90)
)

tilt_stats <- data.frame(
  angle_set = angles,
  mean = sapply(list(o0, o15, o30, o45, o60, o90), mean),
  sd = sapply(list(o0, o15, o30, o45, o60, o90), sd)
)

tilt_fit <- lm(angle_measured ~ angle_actual, data = tilt_df)
tilt_eq <- paste0("y = ", round(coef(tilt_fit)[2], 2), "x + ", round(coef(tilt_fit)[1], 2),
                  "\nR² = ", round(summary(tilt_fit)$r.squared, 3))

# -------------------
# Plot RPM
# -------------------
p_rpm <- ggplot(rpm_stats, aes(x = rpm_set, y = mean)) +
  geom_point(color = "black", size = 2) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), width = 2) +
  geom_abline(intercept = coef(rpm_fit)[1], slope = coef(rpm_fit)[2], color = "red", size = 1) +
  annotate("text", x = max(rpms)*0.05, y = max(rpm_stats$mean)*0.95, label = rpm_eq, color = "black", fontface = "bold", hjust = 0) +
  labs(x = "RPM", y = "Measured RPM") +
  theme_minimal(base_size = 14) +
  theme(
    axis.title = element_text(face = "bold"),
    plot.title = element_text(face = "bold")
  ) +
  ggtitle("(A) RPM Accuracy")

# -------------------
# Plot Tilt
# -------------------
p_tilt <- ggplot(tilt_stats, aes(x = angle_set, y = mean)) +
  geom_point(color = "black", size = 2) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), width = 1.5) +
  geom_abline(intercept = coef(tilt_fit)[1], slope = coef(tilt_fit)[2], color = "red", size = 1) +
  annotate("text", x = max(angles)*0.05, y = max(tilt_stats$mean)*0.95, label = tilt_eq, color = "black", fontface = "bold", hjust = 0) +
  labs(x = "Tilt (°)", y = "Measured Angle (°)") +
  theme_minimal(base_size = 14) +
  theme(
    axis.title = element_text(face = "bold"),
    plot.title = element_text(face = "bold")
  ) +
  ggtitle("(B) Tilt Accuracy")

# -------------------
# Combine plots side-by-side
# -------------------
combined_plot <- p_rpm + p_tilt + plot_layout(ncol = 2, widths = c(1, 1))
combined_plot

