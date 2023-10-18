import streamlit as st
import numpy as np
from scipy import stats

def t_test(x1, x2, n1, n2, s1, s2):
    F = max(s1, s2) / min(s1, s2)
    Fp = 1 - stats.f.cdf(F, n1-1, n2-1)
    
    results = []
    
    if Fp > 0.05:
        sc = np.sqrt((1/n1 + 1/n2) * ((n1-1)*s1 + (n2-1)*s2) / (n1 + n2 - 2))
        t = abs(x2 - x1) / sc
        df = n1 + n2 - 2
        p = 2 * (1 - stats.t.cdf(t, df))
        if p < 0.05:
            min_x1_x2 = x1 - x2 - stats.t.ppf(0.975, df) * sc
            max_x1_x2 = x1 - x2 + stats.t.ppf(0.975, df) * sc
            results.append(f"AB两组通过方差齐性检验(方差相等)，且AB两组均值具有显著差异，p值 = {p}；AB两组差异的95%置信区间delta落在：[{min_x1_x2}, {max_x1_x2}]")
        else:
            results.append(f"AB两组通过方差齐性检验(方差相等)，但是AB两组没有显著差异，p值 = {p}")
    else:
        sc2 = np.sqrt(s1/n1 + s2/n2)
        t2 = abs(x2 - x1) / sc2
        df2 = (s1/n1 + s2/n2)**2 / (((s1/n1)**2) / (n1-1) + ((s2/n2)**2) / (n2-1))
        p2 = 2 * (1 - stats.t.cdf(t2, df2))
        if p2 < 0.05:
            results.append(f"AB两组没有通过方差齐性检验(方差不等)，F检验的p值 = {Fp}；下面是使用welch-T检验的结果：")
            min_x1_x2_2 = x1 - x2 - stats.t.ppf(0.975, df2) * sc2
            max_x1_x2_2 = x1 - x2 + stats.t.ppf(0.975, df2) * sc2
            results.append(f"AB两组均值具有显著差异，p值 = {p2}; AB两组差异的95%置信区间delta落在：[{min_x1_x2_2}, {max_x1_x2_2}]")
        else:
            results.append(f"AB两组没有通过方差齐性检验，F检验的p值 = {Fp}；下面是使用welch-T检验的结果：")
            results.append(f"AB两组均值没有显著差异，p值 = {p2}")
    
    for r in results:
        st.write(r)

def main():
    st.title("Two-Sample T-test Calculator with Variance Check")
    
    x1 = st.number_input("A组均值:", value=0.0)
    n1 = st.number_input("A组样本量:", value=30)
    s1 = st.number_input("A组方差:", value=1.0)

    x2 = st.number_input("B组均值:", value=0.0)
    n2 = st.number_input("B组样本量:", value=30)
    s2 = st.number_input("B组方差:", value=1.0)

    if st.button("C计算 "):
        t_test(x1, x2, n1, n2, s1, s2)

if __name__ == "__main__":
    main()
