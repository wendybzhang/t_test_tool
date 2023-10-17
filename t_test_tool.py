import streamlit as st
import numpy as np
from scipy.stats import t, ttest_ind_from_stats

def t_test_from_stats(mean1, mean2, std1, std2, nobs1, nobs2):
    # Calculate the t statistic and degree of freedom using the given statistics
    t_stat, df = ttest_ind_from_stats(mean1, std1, nobs1, mean2, std2, nobs2, equal_var=False)
    
    # Calculate the critical value for 95% confidence interval
    crit_value = t.ppf(0.975, df)
    
    # Calculate the standard error
    se = np.sqrt((std1**2/nobs1) + (std2**2/nobs2))
    
    # Calculate the confidence interval
    moe = crit_value * se
    ci_low, ci_high = (mean1 - mean2) - moe, (mean1 - mean2) + moe
    
    return t_stat, df, ci_low, ci_high

def main():
    st.title("双样本T检验计算器")
    
    mean1 = st.number_input("请输入第一组的均值:", value=0.0)
    nobs1 = st.number_input("请输入第一组的观测值数量:", value=30)
    std1 = st.number_input("请输入第一组的标准偏差:", value=1.0)

    mean2 = st.number_input("请输入第二组的均值:", value=0.0)
    nobs2 = st.number_input("请输入第二组的观测值数量:", value=30)
    std2 = st.number_input("请输入第二组的标准偏差:", value=1.0)

    if st.button("计算"):
        t_stat, df, ci_low, ci_high = t_test_from_stats(mean1, mean2, std1, std2, nobs1, nobs2)
        
        st.write(f"T 统计量: {t_stat:.2f}")
        st.write(f"自由度: {df:.2f}")
        st.write(f"均值差异的95%置信区间: ({ci_low:.2f}, {ci_high:.2f})")
        
if __name__ == "__main__":
    main()
