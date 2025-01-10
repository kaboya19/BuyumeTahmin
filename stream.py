import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import os
st.set_page_config(page_title="Türkiye Büyüme Tahmini",layout="wide")
tabs=["Çeyreklik Tahmin","Yıllık Tahmin"]
page=st.sidebar.radio("Sekmeler",tabs)
import streamlit as st
from datetime import datetime
dark_mode_enabled = st.sidebar.checkbox("Dark Mod Uyumlu Tema")
cari=pd.read_csv("cari.csv",index_col=0)
sonuç=pd.read_csv("sonuç.csv",index_col=0)
yıllık=pd.read_csv("yıllık.csv",index_col=0)
yıllık=yıllık.loc["2023-09-30":]

cariyıl=pd.read_csv("cariyıl.csv",index_col=0)
gunluk=np.round(cari["Tahmin"].iloc[-1],2)
yıl=np.round(yıllık["Tahmin"].iloc[-1],2)

ham=pd.read_excel("veri3.xlsx",index_col=0)
arındırılmış=pd.read_excel("veri2.xlsx",index_col=0)
arındırılmış.loc["2024-12-31"]=((gunluk/100)+1)*arındırılmış.loc["2024-09-30"]

ham_yıllık=(((arındırılmış.loc["2024-12-31"]*1.071)/ham.loc["2023-12-31"])-1)*100
ham_yıllık=ham_yıllık.values[0]
ham_yıllık=np.round(ham_yıllık,2)


st.markdown(
    """
    <style>
    .title {
        font-size: 36px;  
        font-family: 'Freestyle Script', Courier !important;  
        color: red !important;  
        text-align: center;  
    }
    </style>
    <h1 class="title">Hazırlayan: Bora Kaya</h1>
    """, 
    unsafe_allow_html=True)
if page=="Çeyreklik Tahmin":
    tarih=datetime.today().strftime("%d.%m.%Y")

    st.markdown(
        """
        <style>
            /* Ana başlık stili */
            .main-title {
                font-size: 36px; /* Yazı boyutunu büyüt */
                font-weight: bold; /* Kalın yazı */
                color: black; /* Yazı rengi siyah */
                text-align: center; /* Ortala */
                margin-top: 20px; /* Üst boşluk */
                margin-bottom: 20px; /* Alt boşluk */
            }
        </style>
        <h1 class="main-title">Çeyreklik Büyüme Tahmini</h1>
        """,
        unsafe_allow_html=True
    )

    if dark_mode_enabled:
        st.markdown(
        """
        <style>
            /* Özel stil ayarları */
            .black-text {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            .red-text {
                color: red;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
        st.markdown(
        f'''
        <div style="display: flex;">
            <p class="inline-text white-text" style="margin-right: 1px;">Çeyreklik Büyüme Tahmini(4.Çeyrek)</p>
            <p class="inline-text red-text">%{gunluk} ({tarih})</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
        st.markdown(
        f'''
        <div style="display: flex;">
            <p class="inline-text white-text" style="margin-right: 1px;">Yıllık Büyüme Tahmini(4.Çeyrek)</p>
            <p class="inline-text red-text">%{yıl} ({tarih})</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
        
    else:
        st.markdown(
        """
        <style>
            /* Özel stil ayarları */
            .black-text {
                color: black;
                font-size: 24px;
                font-weight: bold;
            }
            .red-text {
                color: red;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
        st.markdown(
        f'''
        <div style="display: flex;">
            <p class="inline-text black-text" style="margin-right: 1px;">Çeyreklik Büyüme Tahmini(4.Çeyrek):</p>
            <p class="inline-text red-text">%{gunluk} ({tarih})</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
        st.markdown(
        f'''
        <div style="display: flex;">
            <p class="inline-text black-text" style="margin-right: 1px;">Yıllık Büyüme Tahmini(4.Çeyrek,Mevsimsellikten Arındırılmış)</p>
            <p class="inline-text red-text">%{yıl} ({tarih})</p>
        </div>
        ''',
        unsafe_allow_html=True
    )
        
        st.markdown(
        f'''
        <div style="display: flex;">
            <p class="inline-text black-text" style="margin-right: 1px;">Yıllık Büyüme Tahmini(4.Çeyrek,Ham)</p>
            <p class="inline-text red-text">%{ham_yıllık} ({tarih})</p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    




    def tarih_ceyrek(tarih):
        yil = tarih.year
        ay = tarih.month
        if ay <= 3:
            return f"{yil}Q1"
        elif ay <= 6:
            return f"{yil}Q2"
        elif ay <= 9:
            return f"{yil}Q3"
        else:
            return f"{yil}Q4"
        
    tarihler = [tarih_ceyrek(t) for t in pd.to_datetime(sonuç.index)]
    formatted_dates = tarihler

    fig0= go.Figure()
    if dark_mode_enabled:
        fig0.add_trace(go.Scatter(x=sonuç.index,y=sonuç["Ortalama"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=4),marker=dict(size=8,color="white")))
        fig0.add_trace(go.Scatter(x=sonuç.index[:-1],y=sonuç["Büyüme"][:-1],mode='lines+markers',name="Büyüme",line=dict(color='orange', width=4),marker=dict(size=8,color="white")))
        fig0.update_layout(
            xaxis=dict(
                tickvals=sonuç.index,  # Original datetime index
                ticktext=formatted_dates,  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="white")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="white")
            ),
            font=dict(family="Arial", size=14, color="white")
        )
        st.plotly_chart(fig0)

    else:
        fig0.add_trace(go.Scatter(x=sonuç.index,y=sonuç["Ortalama"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=4),marker=dict(size=8,color="black")))
        fig0.add_trace(go.Scatter(x=sonuç.index[:-1],y=sonuç["Büyüme"][:-1],mode='lines+markers',name="Büyüme",line=dict(color='orange', width=4),marker=dict(size=8,color="black")))
        fig0.update_layout(
            xaxis=dict(
                tickvals=sonuç.index,  # Original datetime index
                ticktext=formatted_dates,  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )
        st.plotly_chart(fig0)

        st.markdown(
        """
        <style>
            /* Ana başlık stili */
            .main-title {
                font-size: 36px; /* Yazı boyutunu büyüt */
                font-weight: bold; /* Kalın yazı */
                color: black; /* Yazı rengi siyah */
                text-align: center; /* Ortala */
                margin-top: 20px; /* Üst boşluk */
                margin-bottom: 20px; /* Alt boşluk */
            }
        </style>
        <h1 class="main-title">2024 4.Çeyrek Büyüme Tahmini</h1>
        """,
        unsafe_allow_html=True
    )
        


    formatted_dates = pd.to_datetime(cari.index).strftime('%d.%m.%Y')


    fig1= go.Figure()
    if dark_mode_enabled:
        fig1.add_trace(go.Scatter(x=cari.index,y=cari["Tahmin"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=6),marker=dict(size=8,color="white")))
        fig1.add_trace(go.Scatter(
            x=cari.index,
            y=cari["Üst"],
            mode='lines',
            line=dict(color='rgba(1,1,1,1)'),
            showlegend=False
        ))
        

        fig1.add_trace(go.Scatter(
            x=cari.index,
            y=cari["Alt"],
            mode='lines',
            fill='tonexty',  # Fill between this trace and the previous one
            fillcolor='rgba(255,165,1,0.3)',  # Semi-transparent orange color
            line=dict(color='rgba(1,1,1,1)'),
            name='Güven Aralığı'
        ))
        fig1.update_traces(line=dict(width=5)) 
        fig1.update_layout(
            xaxis=dict(
                tickvals=cari.index,  # Original datetime index
                ticktext=formatted_dates,  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="white")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="white")
            ),
            font=dict(family="Arial", size=14, color="white")
        )
        st.plotly_chart(fig1)

    else:
        fig1.add_trace(go.Scatter(x=cari.index,y=cari["Tahmin"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=6),marker=dict(size=8,color="black")))
        fig1.add_trace(go.Scatter(
            x=cari.index,
            y=cari["Üst"],
            mode='lines',
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False
        ))
        

        fig1.add_trace(go.Scatter(
            x=cari.index,
            y=cari["Alt"],
            mode='lines',
            fill='tonexty',  # Fill between this trace and the previous one
            fillcolor='rgba(255,165,1,0.3)',  # Semi-transparent orange color
            line=dict(color='rgba(0,0,0,0)'),
            name='Güven Aralığı'
        ))
        fig1.update_traces(line=dict(width=5)) 
        fig1.update_layout(
            xaxis=dict(
                tickvals=cari.index,  # Original datetime index
                ticktext=formatted_dates,  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )
        st.plotly_chart(fig1)

if page=="Yıllık Tahmin":
    tip=st.sidebar.selectbox("Tip:", ["Mevsimsellikten Arındırılmış","Ham"])
    if tip=="Mevsimsellikten Arındırılmış":

        st.markdown(
            """
            <style>
                /* Ana başlık stili */
                .main-title {
                    font-size: 36px; /* Yazı boyutunu büyüt */
                    font-weight: bold; /* Kalın yazı */
                    color: black; /* Yazı rengi siyah */
                    text-align: center; /* Ortala */
                    margin-top: 20px; /* Üst boşluk */
                    margin-bottom: 20px; /* Alt boşluk */
                }
            </style>
            <h1 class="main-title">Yıllık Büyüme Tahmini</h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <style>
                /* Ana başlık stili */
                .main-title {
                    font-size: 4px; /* Yazı boyutunu küçült */
                    color: black; /* Yazı rengi siyah */
                    text-align: center; /* Ortala */
                    margin-top: 5px; /* Üst boşluk */
                    margin-bottom: 5px; /* Alt boşluk */
                }
            </style>
            <h3 class="main-title">*Mevsim ve takvim etkilerinden arındırılmıştır.</h3>
            """,
            unsafe_allow_html=True
        )




        def tarih_ceyrek(tarih):
            yil = tarih.year
            ay = tarih.month
            if ay <= 3:
                return f"{yil}Q1"
            elif ay <= 6:
                return f"{yil}Q2"
            elif ay <= 9:
                return f"{yil}Q3"
            else:
                return f"{yil}Q4"
            
        tarihler = [tarih_ceyrek(t) for t in pd.to_datetime(yıllık.index)]
        formatted_dates = tarihler

        fig2= go.Figure()
        if dark_mode_enabled:
            fig2.add_trace(go.Scatter(x=yıllık.index,y=yıllık["Tahmin"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=4),marker=dict(size=8,color="white")))
            fig2.add_trace(go.Scatter(x=yıllık.index[:-1],y=yıllık["Büyüme"][:-1],mode='lines+markers',name="Büyüme",line=dict(color='orange', width=4),marker=dict(size=8,color="white")))
            fig2.update_layout(
                xaxis=dict(
                    tickvals=yıllık.index,  # Original datetime index
                    ticktext=formatted_dates,  # Custom formatted labels
                    tickfont=dict(size=14, family="Arial Black", color="white")
                ),
                yaxis=dict(
                    tickfont=dict(size=14, family="Arial Black", color="white")
                ),
                font=dict(family="Arial", size=14, color="white")
            )
            
            st.plotly_chart(fig2)

        else:
            fig2.add_trace(go.Scatter(x=yıllık.index,y=yıllık["Tahmin"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=4),marker=dict(size=8,color="black")))
            fig2.add_trace(go.Scatter(x=yıllık.index[:-1],y=yıllık["Büyüme"][:-1],mode='lines+markers',name="Büyüme",line=dict(color='orange', width=4),marker=dict(size=8,color="black")))
            fig2.update_layout(
                xaxis=dict(
                    tickvals=yıllık.index,  # Original datetime index
                    ticktext=formatted_dates,  # Custom formatted labels
                    tickfont=dict(size=14, family="Arial Black", color="black")
                ),
                yaxis=dict(
                    tickfont=dict(size=14, family="Arial Black", color="black")
                ),
                font=dict(family="Arial", size=14, color="black")
            )
            st.plotly_chart(fig2)



        st.markdown(
            """
            <style>
                /* Ana başlık stili */
                .main-title {
                    font-size: 36px; /* Yazı boyutunu büyüt */
                    font-weight: bold; /* Kalın yazı */
                    color: black; /* Yazı rengi siyah */
                    text-align: center; /* Ortala */
                    margin-top: 20px; /* Üst boşluk */
                    margin-bottom: 20px; /* Alt boşluk */
                }
            </style>
            <h1 class="main-title">2024 4.Çeyrek Yıllık Büyüme Tahmini</h1>
            """,
            unsafe_allow_html=True
        )
            


        formatted_dates = pd.to_datetime(cariyıl.index).strftime('%d.%m.%Y')


        fig3= go.Figure()
        if dark_mode_enabled:
            fig3.add_trace(go.Scatter(x=cariyıl.index,y=cariyıl["Tahmin"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=6),marker=dict(size=8,color="white")))
            fig3.update_layout(
                xaxis=dict(
                    tickvals=cariyıl.index,  # Original datetime index
                    ticktext=formatted_dates,  # Custom formatted labels
                    tickfont=dict(size=14, family="Arial Black", color="white")
                ),
                yaxis=dict(
                    tickfont=dict(size=14, family="Arial Black", color="white")
                ),
                font=dict(family="Arial", size=14, color="white")
            )
            fig3.add_trace(go.Scatter(
                x=cariyıl.index,
                y=cariyıl["Üst"],
                mode='lines',
                line=dict(color='rgba(1,1,1,1)'),
                showlegend=False
            ))
            

            fig3.add_trace(go.Scatter(
                x=cariyıl.index,
                y=cariyıl["Alt"],
                mode='lines',
                fill='tonexty',  # Fill between this trace and the previous one
                fillcolor='rgba(255,165,1,0.3)',  # Semi-transparent orange color
                line=dict(color='rgba(1,1,1,1)'),
                name='Güven Aralığı'
            ))
            fig3.update_traces(line=dict(width=5)) 

        else:
            fig3.add_trace(go.Scatter(x=cariyıl.index,y=cariyıl["Tahmin"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=6),marker=dict(size=8,color="black")))
            fig3.add_trace(go.Scatter(
                x=cariyıl.index,
                y=cariyıl["Üst"],
                mode='lines',
                line=dict(color='rgba(0,0,0,0)'),
                showlegend=False
            ))
            

            fig3.add_trace(go.Scatter(
                x=cariyıl.index,
                y=cariyıl["Alt"],
                mode='lines',
                fill='tonexty',  # Fill between this trace and the previous one
                fillcolor='rgba(255,165,1,0.3)',  # Semi-transparent orange color
                line=dict(color='rgba(0,0,0,0)'),
                name='Güven Aralığı'
            ))
            fig3.update_traces(line=dict(width=5)) 
            fig3.update_layout(
                xaxis=dict(
                    tickvals=cariyıl.index,  # Original datetime index
                    ticktext=formatted_dates,  # Custom formatted labels
                    tickfont=dict(size=14, family="Arial Black", color="black")
                ),
                yaxis=dict(
                    tickfont=dict(size=14, family="Arial Black", color="black")
                ),
                font=dict(family="Arial", size=14, color="black")
            )
            st.plotly_chart(fig3)

    
    if tip=="Ham":
        ham=pd.read_csv("ham.csv",index_col=0)
        ham.index=pd.to_datetime(ham.index)
        formatted_dates = pd.to_datetime(ham.index).strftime('%d.%m.%Y')
        st.markdown(
            """
            <style>
                /* Ana başlık stili */
                .main-title {
                    font-size: 36px; /* Yazı boyutunu büyüt */
                    font-weight: bold; /* Kalın yazı */
                    color: black; /* Yazı rengi siyah */
                    text-align: center; /* Ortala */
                    margin-top: 20px; /* Üst boşluk */
                    margin-bottom: 20px; /* Alt boşluk */
                }
            </style>
            <h1 class="main-title">2024 4.Çeyrek Yıllık Ham Büyüme Tahmini</h1>
            """,
            unsafe_allow_html=True
        )
        figham= go.Figure()

        figham.add_trace(go.Scatter(x=ham.index,y=ham["Tahmin"],mode='lines+markers',name="Tahmin",line=dict(color='red', width=6),marker=dict(size=8,color="black")))
        figham.add_trace(go.Scatter(
            x=ham.index,
            y=ham["Üst"],
            mode='lines',
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False
        ))
        

        figham.add_trace(go.Scatter(
            x=ham.index,
            y=ham["Alt"],
            mode='lines',
            fill='tonexty',  # Fill between this trace and the previous one
            fillcolor='rgba(255,165,1,0.3)',  # Semi-transparent orange color
            line=dict(color='rgba(0,0,0,0)'),
            name='Güven Aralığı'
        ))
        figham.update_traces(line=dict(width=5)) 
        figham.update_layout(
            xaxis=dict(
                tickvals=ham.index,  # Original datetime index
                ticktext=formatted_dates,  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )
        st.plotly_chart(figham)
